"""
inference.py — CADET-AR video inference module.
Runs inference only (never retrains, never needs original datasets).
Functions adapted verbatim from notebook video-combined_3.ipynb (cells 2, 4, 5, 16),
using deploy_config.json instead of Kaggle paths/globals.
No Streamlit imports in this file.
"""

import os
import json
import time
from pathlib import Path
from contextlib import nullcontext

import cv2
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as Fn
import torchvision.transforms.functional as TF
from torchvision.models import efficientnet_b1

# ── Global configuration & environment setup ─────────────────────────────────

_ROOT = Path(__file__).parent
_CONFIG_PATH = _ROOT / "models" / "deploy_config.json"

with open(_CONFIG_PATH, "r") as _f:
    DEPLOY_CONFIG = json.load(f"{_f.read()}") if False else json.load(open(_CONFIG_PATH))

# Thread count
if hasattr(os, "cpu_count") and os.cpu_count():
    torch.set_num_threads(os.cpu_count())

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

_MEAN = torch.tensor(IMAGENET_MEAN).view(1, 1, 3, 1, 1)
_STD = torch.tensor(IMAGENET_STD).view(1, 1, 3, 1, 1)

_VALID_MIN = torch.tensor([(0.0 - m) / s for m, s in zip(IMAGENET_MEAN, IMAGENET_STD)]).view(3, 1, 1).to(DEVICE)
_VALID_MAX = torch.tensor([(1.0 - m) / s for m, s in zip(IMAGENET_MEAN, IMAGENET_STD)]).view(3, 1, 1).to(DEVICE)

# Haar Cascades from OpenCV
_CASCADE_FILES = ["haarcascade_frontalface_default.xml", "haarcascade_frontalface_alt2.xml"]
_FACE_CASCADES = [cv2.CascadeClassifier(cv2.data.haarcascades + f) for f in _CASCADE_FILES]
_FACE_CASCADES = [c for c in _FACE_CASCADES if not c.empty()]


# ── Cell 2: Face detection, squaring, and frame reading ───────────────────────

def _detect_face_box(frame_bgr):
    h, w = frame_bgr.shape[:2]
    scale = 640.0 / max(h, w) if max(h, w) > 640 else 1.0
    small = cv2.resize(frame_bgr, None, fx=scale, fy=scale) if scale < 1.0 else frame_bgr
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    for cascade, min_neighbors in zip(_FACE_CASCADES, (5, 4)):   # 2nd cascade only if the 1st finds nothing
        faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=min_neighbors, minSize=(40, 40))
        if len(faces) > 0:
            x, y, fw, fh = max(faces, key=lambda b: b[2] * b[3])
            return x / scale, y / scale, fw / scale, fh / scale
    return None


def _video_face_square(frames_bgr, margin=1.3, face_detect_every=4, face_min_detect_rate=0.25):
    """One stable square crop per clip (median centre, largest accepted size); outlier boxes (false
    positives) are rejected first. Returns (x0, y0, x1, y1, detected_flag, detect_rate)."""
    h, w = frames_bgr[0].shape[:2]
    tried = frames_bgr[::max(1, face_detect_every)]
    boxes = [bx for bx in (_detect_face_box(f) for f in tried) if bx is not None]
    if len(boxes) >= 3:
        cxs = np.array([x + fw / 2 for x, y, fw, fh in boxes])
        cys = np.array([y + fh / 2 for x, y, fw, fh in boxes])
        szs = np.array([max(fw, fh) for x, y, fw, fh in boxes])
        mcx, mcy, msz = np.median(cxs), np.median(cys), np.median(szs)
        keep = (np.abs(cxs - mcx) < 0.5 * msz) & (np.abs(cys - mcy) < 0.5 * msz) & (szs > 0.5 * msz) & (szs < 2.0 * msz)
        boxes = [b for b, k in zip(boxes, keep) if k]
    detect_rate = len(boxes) / max(len(tried), 1)
    if boxes and detect_rate >= face_min_detect_rate:
        cx = float(np.median([x + fw / 2 for x, y, fw, fh in boxes]))
        cy = float(np.median([y + fh / 2 for x, y, fw, fh in boxes]))
        size = max(max(fw, fh) for x, y, fw, fh in boxes) * margin
        detected = True
    else:                                      # fallback: central square
        cx, cy, size, detected = w / 2, h / 2, 0.7 * min(h, w), False
    size = min(size, h, w)
    x0 = int(np.clip(cx - size / 2, 0, w - size))
    y0 = int(np.clip(cy - size / 2, 0, h - size))
    return x0, y0, int(x0 + size), int(y0 + size), detected, detect_rate


def _read_pool_frames(v_path, frame_pool_size=32):
    cap = cv2.VideoCapture(str(v_path))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_s = total_frames / fps if fps > 0 else 0.0

    if total_frames >= frame_pool_size:
        indices = np.linspace(0, total_frames - 1, frame_pool_size, dtype=int)
    else:
        indices = np.arange(max(total_frames, 1))
    target_indices = set(int(i) for i in indices)
    frames, curr_frame = [], 0
    while cap.isOpened() and len(frames) < len(target_indices):
        ret, frame = cap.read()
        if not ret:
            break
        if curr_frame in target_indices:
            frames.append(frame)
        curr_frame += 1
    cap.release()
    meta = {
        "duration_s": duration_s,
        "fps": fps,
        "width": w,
        "height": h,
        "frame_count": total_frames,
    }
    return frames, indices, meta


# ── Cell 4: Model architecture ────────────────────────────────────────────────

class TemporalAttentionPooling(nn.Module):
    """Optional (ablation-only) alternative to mean pooling."""
    def __init__(self, input_dim):
        super().__init__()
        self.attn = nn.Sequential(
            nn.Linear(input_dim, input_dim // 2),
            nn.Tanh(),
            nn.Linear(input_dim // 2, 1),
        )

    def forward(self, x):
        scores = self.attn(x)
        weights = torch.softmax(scores, dim=1)
        pooled = torch.sum(weights * x, dim=1)
        return pooled, weights.squeeze(-1)


class FFPPDeepfakeDetectorV2(nn.Module):
    def __init__(self, lstm_hidden_size=512, num_layers=2, bidirectional=False,
                 dropout=0.3, use_attention=False):
        super().__init__()
        # Pretrained weights disabled (weights=None); checkpoints supply weights
        base_model = efficientnet_b1(weights=None)
        self.feature_extractor = nn.Sequential(*list(base_model.children())[:-1])  # [stages, avgpool]
        self.feature_dim = 1280
        self.dropout_cnn = nn.Dropout(p=dropout)
        self.flatten = nn.Flatten()

        # Projection: 1280 -> 512
        self.projection = nn.Sequential(
            nn.Linear(self.feature_dim, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
        )

        # Temporal model: 2-layer UNIDIRECTIONAL LSTM by default
        self.bidirectional = bidirectional
        self.use_attention = use_attention
        self.lstm = nn.LSTM(
            input_size=512,
            hidden_size=lstm_hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
            dropout=(dropout if num_layers > 1 else 0.0),
        )
        lstm_out_dim = lstm_hidden_size * (2 if bidirectional else 1)

        self.temporal_pool = TemporalAttentionPooling(lstm_out_dim) if use_attention else None

        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(lstm_out_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(256, 1),
        )

        self.last_attention_weights = None

    def forward(self, x):
        batch_size, seq_len, c, h, w = x.shape
        x = x.view(batch_size * seq_len, c, h, w)
        features = self.feature_extractor(x)
        features = self.flatten(features)
        features = self.dropout_cnn(features)
        features = self.projection(features)
        features = features.view(batch_size, seq_len, -1)
        lstm_out, _ = self.lstm(features)

        if self.use_attention:
            pooled, attn_weights = self.temporal_pool(lstm_out)
            self.last_attention_weights = attn_weights.detach()
        else:
            pooled = torch.mean(lstm_out, dim=1)
            self.last_attention_weights = None

        out = self.classifier(pooled)
        out = out.squeeze(1)
        return out


# ── Cell 5: FGSM attack helpers ───────────────────────────────────────────────

def _prepare_model_for_attack(model):
    prev = {m: m.training for m in model.modules()}
    model.eval()
    for m in model.modules():
        if isinstance(m, (nn.LSTM, nn.GRU, nn.RNN)):
            m.train()
            m._stored_dropout = m.dropout
            m.dropout = 0.0
    return prev


def _restore_model_modes(model, prev):
    for m in model.modules():
        if m in prev:
            m.train(prev[m])
        if isinstance(m, (nn.LSTM, nn.GRU, nn.RNN)) and hasattr(m, "_stored_dropout"):
            m.dropout = m._stored_dropout
            del m._stored_dropout


def _norm_bounds(device):
    mean, std = _MEAN.to(device), _STD.to(device)
    return (0.0 - mean) / std, (1.0 - mean) / std


def _eps_normalized(eps, device):
    if not torch.is_tensor(eps):
        eps = torch.tensor(float(eps))
    return eps.to(device).float() / _STD.to(device)


def fgsm_grad(model, videos, labels, use_amp=False, label_source="true"):
    prev = _prepare_model_for_attack(model)
    try:
        x = videos.detach().clone().requires_grad_(True)
        ctx = torch.amp.autocast("cuda") if (use_amp and videos.is_cuda) else nullcontext()
        with ctx:
            logits = model(x)
        logits = logits.float()
        if label_source == "pred":
            y = (logits.detach() > 0).float()
        elif label_source == "flipped":
            y = 1.0 - labels.float()
        else:
            y = labels.float()
        loss = Fn.binary_cross_entropy_with_logits(logits, y, reduction="sum")
        if use_amp and videos.is_cuda:
            scale = 1024.0
            grad = torch.autograd.grad(loss * scale, x)[0] / scale
        else:
            grad = torch.autograd.grad(loss, x)[0]
    finally:
        _restore_model_modes(model, prev)
    grad = torch.nan_to_num(grad, nan=0.0, posinf=0.0, neginf=0.0)
    return grad.detach(), logits.detach()


def fgsm_apply(x0, grad, eps):
    vmin, vmax = _norm_bounds(x0.device)
    eps_n = _eps_normalized(eps, x0.device)
    with torch.no_grad():
        x_adv = x0.detach() + eps_n * torch.sign(grad)
        x_adv = torch.max(torch.min(x_adv, vmax), vmin)
    return x_adv.detach()


def fgsm_attack(model, videos, labels, epsilon, use_amp=False, label_source="true", return_info=False):
    grad, logits = fgsm_grad(model, videos, labels, use_amp=use_amp, label_source=label_source)
    x_adv = fgsm_apply(videos, grad, epsilon)
    if return_info:
        return x_adv, {"grad": grad, "logits": logits}
    return x_adv


# ── Cell 16: Grad-CAM ─────────────────────────────────────────────────────────

class VideoGradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.gradients = None
        self.activations = None
        self.handles = [
            target_layer.register_forward_hook(self._save_act),
            target_layer.register_full_backward_hook(self._save_grad),
        ]

    def _save_act(self, module, inp, out):
        self.activations = out.detach()

    def _save_grad(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()

    def remove(self):
        for h in self.handles:
            h.remove()

    def heatmaps(self, video_tensor):
        """video_tensor: [1, T, 3, H, W] -> (P(fake) uncalibrated, per-frame heatmaps [T, h, w])."""
        prev = _prepare_model_for_attack(self.model)
        try:
            x = video_tensor.clone().detach().requires_grad_(True)
            logits = self.model(x)
            prob = torch.sigmoid(logits.float()).item()
            self.model.zero_grad()
            logits.sum().backward()
            weights = self.gradients.mean(dim=(2, 3), keepdim=True)
            cams = Fn.relu((weights * self.activations).sum(dim=1))
            maps = []
            for cam in cams:
                cam = cam - cam.min()
                maps.append((cam / (cam.max() + 1e-7)).cpu().numpy())
        finally:
            _restore_model_modes(self.model, prev)
            self.model.zero_grad(set_to_none=True)
        return prob, np.array(maps)


def _cam_maps(model, video):
    cam = VideoGradCAM(model, model.feature_extractor[0][-1])
    try:
        return cam.heatmaps(video)
    finally:
        cam.remove()


def _overlay(frame_norm, heat):
    img = np.clip(np.array(IMAGENET_STD) * frame_norm + np.array(IMAGENET_MEAN), 0, 1)
    img8 = (img * 255).astype(np.uint8)
    h = cv2.resize(heat, (img8.shape[1], img8.shape[0]))
    colour = cv2.cvtColor(cv2.applyColorMap(np.uint8(255 * h), cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
    return img, cv2.addWeighted(img8, 0.6, colour, 0.4, 0)


# ── Model Registry (loaded once, strictly verified) ──────────────────────────

_LOADED_MODELS = {}


def load_model(name: str = "fgsm"):
    """Load model checkpoint with strict=True and eval() mode."""
    if name in _LOADED_MODELS:
        return _LOADED_MODELS[name]

    ckpt_path = _ROOT / "models" / f"best_{name}_model.pth"
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Model checkpoint not found: {ckpt_path}")

    model = FFPPDeepfakeDetectorV2()
    ckpt = torch.load(str(ckpt_path), map_location=DEVICE, weights_only=False)
    incompatible = model.load_state_dict(ckpt["model_state_dict"], strict=True)
    if incompatible.missing_keys or incompatible.unexpected_keys:
        print(f"Warning: checkpoint {name} keys mismatch: missing={incompatible.missing_keys}, unexpected={incompatible.unexpected_keys}")

    model.to(DEVICE)
    model.eval()
    _LOADED_MODELS[name] = model
    return model


# ── Preprocessing & Main Inference Routine ────────────────────────────────────

def analyze_video(path: str, model: str = "fgsm", with_stress: bool = False, progress_cb=None) -> dict:
    """Analyse a video file for deepfake traces.

    Matches training evaluation:
    1. Read 32 frames uniformly with OpenCV.
    2. Haar cascade face detection every 4th frame, median center/size, margin 1.3.
    3. Square crop resized to 256x256 INTER_AREA, JPEG encoded at 95 and decoded.
    4. Middle frame of 16 bins chosen.
    5. Resize to 224x224, to_tensor, ImageNet normalize, clamp.
    6. EfficientNet-B1 + LSTM forward pass with torch.no_grad().
    7. Grad-CAM on 6 frames.
    8. Optional FGSM stress test at eps=1/255.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Video not found: {path}")

    stages = []

    def _mark(stage_name, start_t):
        ms = (time.time() - start_t) * 1000.0
        stages.append({"name": stage_name, "ms": ms})
        if progress_cb is not None:
            progress_cb(stage_name, ms)

    # 1. Ingest
    t_start = time.time()
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read video file: {path}")
    _mark("ingest", t_start)

    # 2. Frame sampling
    t_start = time.time()
    pool_frames, pool_indices, meta = _read_pool_frames(path, DEPLOY_CONFIG["frame_pool_size"])
    if not pool_frames:
        raise ValueError(f"Could not read any frames from: {path}")
    _mark("frame_sampling", t_start)

    # 3. Face detection
    t_start = time.time()
    margin = DEPLOY_CONFIG.get("face_margin", 1.3)
    x0, y0, x1, y1, detected, rate = _video_face_square(pool_frames, margin=margin)
    _mark("face_detection", t_start)

    # 4. Crop & Normalise
    t_start = time.time()
    cs = DEPLOY_CONFIG["face_crop_size"]  # 256
    seq_len = DEPLOY_CONFIG["seq_len"]    # 16
    img_size = DEPLOY_CONFIG["img_size"]  # 224

    # Crop and JPEG Q95 encode/decode roundtrip
    jpeg_crops = []
    for fr in pool_frames:
        crop = cv2.resize(fr[y0:y1, x0:x1], (cs, cs), interpolation=cv2.INTER_AREA)
        _, enc = cv2.imencode(".jpg", crop, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        dec = cv2.imdecode(enc, cv2.IMREAD_COLOR)
        jpeg_crops.append(dec)

    # Split 32 into 16 bins and take middle frame
    n_avail = len(jpeg_crops)
    bounds = np.linspace(0, n_avail, seq_len + 1).astype(int)
    selected_indices = [(bounds[i] + bounds[i + 1] - 1) // 2 for i in range(seq_len)]
    selected_crops_bgr = [jpeg_crops[i] for i in selected_indices]
    selected_frame_indices = [int(pool_indices[i]) for i in selected_indices]

    # Convert to RGB arrays for UI display
    selected_crops_rgb = [cv2.cvtColor(c, cv2.COLOR_BGR2RGB) for c in selected_crops_bgr]

    # PyTorch transforms
    processed_tensors = []
    for crop_bgr in selected_crops_bgr:
        img_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        pil_img = TF.resize(pil_img, (img_size, img_size))
        tensor = TF.to_tensor(pil_img).to(DEVICE)
        tensor = TF.normalize(tensor, mean=IMAGENET_MEAN, std=IMAGENET_STD)
        tensor = torch.max(torch.min(tensor, _VALID_MAX), _VALID_MIN)
        processed_tensors.append(tensor)

    video_tensor = torch.stack(processed_tensors).unsqueeze(0)  # [1, 16, 3, 224, 224]
    _mark("crop_normalise", t_start)

    # 5. Feature extraction & 6. Temporal model
    # Load model
    selected_model_name = "fgsm" if model.lower().startswith("fgsm") else "clean"
    mdl = load_model(selected_model_name)

    t_start = time.time()
    with torch.no_grad():
        b, s, c, h, w = video_tensor.shape
        x_reshaped = video_tensor.view(b * s, c, h, w)
        features = mdl.feature_extractor(x_reshaped)
        features = mdl.flatten(features)
        features = mdl.dropout_cnn(features)
        features = mdl.projection(features)
    _mark("feature_extraction", t_start)

    t_start = time.time()
    with torch.no_grad():
        features_seq = features.view(b, s, -1)
        lstm_out, _ = mdl.lstm(features_seq)
        if mdl.use_attention:
            pooled, _ = mdl.temporal_pool(lstm_out)
        else:
            pooled = torch.mean(lstm_out, dim=1)
        raw_logit = mdl.classifier(pooled).squeeze(1).item()
    _mark("temporal_model", t_start)

    # 7. Calibration
    t_start = time.time()
    T_val = DEPLOY_CONFIG[f"{selected_model_name}_T"]
    thr_val = DEPLOY_CONFIG[f"{selected_model_name}_threshold"]
    p_fake = float(torch.sigmoid(torch.tensor(raw_logit / T_val)).item())

    # Verdict determination
    # Inconclusive when |probability - threshold| < 0.08 or fallback crop used
    used_fallback_crop = not detected
    INCONCLUSIVE_MARGIN = 0.08
    if abs(p_fake - thr_val) < INCONCLUSIVE_MARGIN or used_fallback_crop:
        verdict = "inconclusive"
    elif p_fake >= thr_val:
        verdict = "manipulated"
    else:
        verdict = "authentic"
    _mark("calibration", t_start)

    # 8. Explainability (Grad-CAM on 6 evenly spaced frames)
    t_start = time.time()
    cam_indices = list(np.linspace(0, seq_len - 1, 6, dtype=int))
    _, all_maps = _cam_maps(mdl, video_tensor)
    cam_maps = [all_maps[i] for i in cam_indices]
    cam_frames_rgb = [selected_crops_rgb[i] for i in cam_indices]
    _mark("explainability", t_start)

    # 9. Stress test (optional)
    stress_info = None
    if with_stress:
        t_start = time.time()
        eps = 1.0 / 255.0
        # Load both models
        clean_mdl = load_model("clean")
        fgsm_mdl = load_model("fgsm")

        # Attack against selected model using label_source="pred"
        adv_tensor = fgsm_attack(mdl, video_tensor, None, eps, label_source="pred")

        with torch.no_grad():
            cl_clean_p = float(torch.sigmoid(torch.tensor(clean_mdl(video_tensor).item() / DEPLOY_CONFIG["clean_T"])).item())
            cl_adv_p = float(torch.sigmoid(torch.tensor(clean_mdl(adv_tensor).item() / DEPLOY_CONFIG["clean_T"])).item())

            fg_clean_p = float(torch.sigmoid(torch.tensor(fgsm_mdl(video_tensor).item() / DEPLOY_CONFIG["fgsm_T"])).item())
            fg_adv_p = float(torch.sigmoid(torch.tensor(fgsm_mdl(adv_tensor).item() / DEPLOY_CONFIG["fgsm_T"])).item())

        stress_info = {
            "eps": eps,
            "models": {
                "clean": {"clean_prob": cl_clean_p, "attacked_prob": cl_adv_p},
                "fgsm": {"clean_prob": fg_clean_p, "attacked_prob": fg_adv_p},
            },
        }
        _mark("stress_test", t_start)

    # Prepare first frame with drawn box for UI
    first_frame_bgr = pool_frames[0].copy()
    cv2.rectangle(first_frame_bgr, (x0, y0), (x1, y1), (0, 90, 196), 2)
    first_frame_rgb = cv2.cvtColor(first_frame_bgr, cv2.COLOR_BGR2RGB)

    return {
        "verdict": verdict,
        "probability": p_fake,
        "raw_logit": raw_logit,
        "threshold": thr_val,
        "T": T_val,
        "stages": stages,
        "evidence": {
            "frames": selected_crops_rgb,
            "frame_indices": selected_frame_indices,
            "face_detect_rate": rate,
            "used_fallback_crop": used_fallback_crop,
            "detected_box": [x0, y0, x1, y1],
            "first_frame_rgb": first_frame_rgb,
            "video_meta": meta,
        },
        "explain": {
            "gradcam": cam_maps,
            "cam_frames": cam_frames_rgb,
            "cam_frame_indices": cam_indices,
        },
        "stress": stress_info,
        "model": {
            "name": "FGSM-trained" if selected_model_name == "fgsm" else "Clean-trained",
            "version": "v9",
            "trained_on": "FaceForensics++ C23 · Celeb-DF · UADFV",
        },
    }
