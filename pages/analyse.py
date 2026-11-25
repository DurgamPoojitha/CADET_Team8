"""
pages/analyse.py — CADET-AR analysis page.
Runs live inference using inference.py, best_{model}_model.pth checkpoints,
and deploy_config.json.
Sample clips load instantly from samples/cached_results.json with stage replay.
Comprehensive edge-case and error handling without traceback leakage.
"""

import os
import io
import time
import base64
import tempfile
import datetime
import traceback
from pathlib import Path

import cv2
import numpy as np
import streamlit as st
from PIL import Image

_ROOT = Path(__file__).parent.parent
_ERROR_LOG = _ROOT / "error.log"

# ── Inference Engine Connection ──────────────────────────────────────────────
_INFERENCE_AVAILABLE = False
_INFERENCE_ERR = None

try:
    from inference import analyze_video
    _INFERENCE_AVAILABLE = True
except Exception as _e:
    _INFERENCE_AVAILABLE = False
    _INFERENCE_ERR = str(_e)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _case_id() -> str:
    now = datetime.datetime.now()
    suffix = f"{now.microsecond % 100:02d}"
    return f"CADET-AR · CASE {now.strftime('%Y-%m%d')}-{suffix}"


def _fmt_ms(ms: float) -> str:
    return f"{ms:.0f} ms"


def _log_error(context: str, exc: Exception):
    """Write full traceback to local error.log only."""
    with open(_ERROR_LOG, "a") as f:
        f.write(f"\n--- [{datetime.datetime.now()}] ERROR in {context} ---\n")
        f.write(traceback.format_exc())
        f.write("\n")


def _render_gauge(prob: float, threshold: float, verdict: str):
    """Render a horizontal probability gauge with threshold marker."""
    pct = max(0, min(100, int(prob * 100)))
    thr_pct = max(0, min(100, int(threshold * 100)))
    if verdict == "manipulated":
        fill_color = "var(--accent)"
    elif verdict == "authentic":
        fill_color = "var(--authentic)"
    else:
        fill_color = "var(--inconclusive)"

    st.markdown(f"""
<div class="gauge-wrap">
  <div style="display:flex;justify-content:space-between;margin-bottom:.2rem">
    <span>P(fake) = <strong style="font-family:var(--mono);color:var(--ink)">{prob:.4f}</strong></span>
    <span>threshold = <strong style="font-family:var(--mono);color:var(--ink)">{threshold:.4f}</strong></span>
  </div>
  <div class="gauge-bar-bg">
    <div class="gauge-bar-fill" style="width:{pct}%;background:{fill_color}"></div>
    <div class="gauge-marker" style="left:{thr_pct}%;"></div>
  </div>
  <div style="display:flex;justify-content:space-between">
    <span>0.000 — Authentic</span>
    <span>Manipulated — 1.000</span>
  </div>
</div>
""", unsafe_allow_html=True)


def _render_verdict(verdict: str, prob: float, threshold: float, used_fallback: bool):
    cls = f"verdict-{verdict}"
    label = {
        "manipulated": "MANIPULATED",
        "authentic":   "AUTHENTIC",
        "inconclusive": "INCONCLUSIVE",
    }[verdict]
    reason = ""
    if verdict == "inconclusive":
        margin = abs(prob - threshold)
        if used_fallback:
            reason = "No reliable face sequence found (central square fallback used)."
        else:
            reason = f"|P(fake) − threshold| = {margin:.4f} < 0.08 margin of uncertainty."

    st.markdown(f"""
<div class="{cls}">
  {label}
</div>
<div class="verdict-sub">
  P(fake) = {prob:.4f} &nbsp;·&nbsp; threshold = {threshold:.4f}
  {"&nbsp;·&nbsp; " + reason if reason else ""}
</div>
""", unsafe_allow_html=True)
    st.markdown('<div style="margin:.6rem 0"></div>', unsafe_allow_html=True)


def _render_frame_sheet(frames: list, indices: list):
    """Render 16 sampled frames in an 8x2 grid."""
    n = len(frames)
    cols_per_row = 8
    rows = (n + cols_per_row - 1) // cols_per_row
    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            fi = r * cols_per_row + c
            if fi >= n:
                break
            with cols[c]:
                st.image(frames[fi], use_container_width=True)
                idx_str = f"#{indices[fi]}" if fi < len(indices) else f"#{fi}"
                st.markdown(f'<div class="frame-num">{idx_str}</div>', unsafe_allow_html=True)


def _render_heatmap_sheet(frames: list, heatmaps: list, indices: list, overlay: bool):
    """Render Grad-CAM contact sheet (6 evenly spaced frames)."""
    n = len(heatmaps)
    cols = st.columns(n)
    for i, col in enumerate(cols):
        with col:
            frame = frames[i] if i < len(frames) else frames[-1]
            if overlay:
                h_map = heatmaps[i]
                if isinstance(h_map, np.ndarray):
                    h_resized = cv2.resize(h_map, (frame.shape[1], frame.shape[0]))
                    colour = cv2.applyColorMap(np.uint8(255 * h_resized), cv2.COLORMAP_JET)
                    colour_rgb = cv2.cvtColor(colour, cv2.COLOR_BGR2RGB)
                    blended = cv2.addWeighted(frame, 0.6, colour_rgb, 0.4, 0)
                    st.image(blended, use_container_width=True)
                else:
                    st.image(h_map, use_container_width=True)
            else:
                st.image(frame, use_container_width=True)
            idx_str = f"#{indices[i]}" if i < len(indices) else f"#{i}"
            st.markdown(f'<div class="frame-num">{idx_str}</div>', unsafe_allow_html=True)


def _arr_to_base64_img(arr: np.ndarray) -> str:
    """Convert RGB numpy array to base64 jpeg data URL."""
    im = Image.fromarray(arr)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


def _generate_html_report(case_id: str, result: dict) -> str:
    """Generate a clean standalone HTML report."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    verdict = result["verdict"].upper()
    prob = result["probability"]
    thr = result["threshold"]
    model_name = result["model"]["name"]

    crops_b64 = [_arr_to_base64_img(f) for f in result["evidence"]["frames"][:16]]
    indices = result["evidence"]["frame_indices"][:16]

    cam_frames = result["explain"]["cam_frames"]
    cam_maps = result["explain"]["gradcam"]
    cam_b64 = []
    for f, h in zip(cam_frames, cam_maps):
        if isinstance(h, np.ndarray):
            h_res = cv2.resize(h, (f.shape[1], f.shape[0]))
            colour = cv2.cvtColor(cv2.applyColorMap(np.uint8(255 * h_res), cv2.COLORMAP_JET), cv2.COLOR_BGR2RGB)
            blended = cv2.addWeighted(f, 0.6, colour, 0.4, 0)
            cam_b64.append(_arr_to_base64_img(blended))
        else:
            cam_b64.append(_arr_to_base64_img(h))

    crop_html = "".join(
        f"<div style='display:inline-block;margin:4px;text-align:center'>"
        f"<img src='{src}' width='90' style='border:1px solid #ccc;border-radius:2px'><br>"
        f"<span style='font-family:monospace;font-size:10px;color:#666'>#{indices[i]}</span></div>"
        for i, src in enumerate(crops_b64)
    )

    cam_html = "".join(
        f"<div style='display:inline-block;margin:4px;text-align:center'>"
        f"<img src='{src}' width='110' style='border:1px solid #ccc;border-radius:2px'></div>"
        for src in cam_b64
    )

    color_hex = "#C45A00" if verdict == "MANIPULATED" else ("#3D6B4F" if verdict == "AUTHENTIC" else "#6B6057")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{case_id} — Report</title>
<style>
  body {{ font-family: 'Georgia', serif; margin: 40px auto; max-width: 800px; color: #1A1612; background: #FAF7F2; line-height: 1.5; }}
  h1 {{ font-size: 24px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }}
  .rule {{ border-top: 1px solid #C8BFB0; margin: 15px 0; }}
  .badge {{ display: inline-block; padding: 10px 20px; font-weight: bold; font-size: 18px; border: 2px solid {color_hex}; color: {color_hex}; border-radius: 2px; }}
  .meta {{ font-family: monospace; font-size: 12px; color: #666; margin: 10px 0; }}
  .sec-title {{ font-family: monospace; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #888; margin-top: 25px; }}

</style>
</head>
<body>
  <h1>CADET-AR · Forensic Analysis Report</h1>
  <div class="meta">{case_id} &nbsp;|&nbsp; Generated: {now_str} &nbsp;|&nbsp; Model: {model_name}</div>
  <div class="rule"></div>

  <div style="margin: 20px 0;">
    <div class="badge">{verdict}</div>
    <div style="margin-top: 8px; font-family: monospace; font-size: 13px;">
      Calibrated P(fake) = <strong>{prob:.4f}</strong> &nbsp;|&nbsp; Threshold = <strong>{thr:.4f}</strong>
    </div>
  </div>

  <div class="sec-title">Sampled Face Crops (16 frames)</div>
  <div style="margin-top: 8px;">{crop_html}</div>

  <div class="sec-title">Grad-CAM Heatmaps (6 keyframes)</div>
  <div style="margin-top: 8px;">{cam_html}</div>

  <div class="rule"></div>
  <div class="meta" style="font-size: 10px; color: #999;">
    CADET-AR &nbsp;·&nbsp; EfficientNet-B1 + LSTM &nbsp;·&nbsp; Team 8 &nbsp;·&nbsp; Amrita School of Engineering
  </div>
</body>
</html>"""


# ── Load cached sample result ────────────────────────────────────────────────

@st.cache_data(ttl=600)
def _load_cached_results():
    p = _ROOT / "samples" / "cached_results.json"
    if p.exists():
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


# ── Main Render Routine ──────────────────────────────────────────────────────

def render():
    tab_video, tab_image = st.tabs(["Video", "Image"])

    with tab_image:
        st.markdown('<p class="label-sc">Image analysis</p>', unsafe_allow_html=True)
        st.info(
            "**Coming soon.** Image-mode deepfake detection is under development "
            "by a teammate and will be integrated here using the same result schema.",
            icon=None,
        )

    with tab_video:
        # ── Model selector ───────────────────────────────────────────────────
        st.markdown('<p class="label-sc">Model</p>', unsafe_allow_html=True)
        model_choice = st.radio(
            "Select detector",
            options=["FGSM-trained (default)", "Clean-trained"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )
        model_key = "fgsm" if model_choice.startswith("FGSM") else "clean"
        descriptions = {
            "fgsm": (
                "**FGSM-trained** — adversarially trained with single-step FGSM perturbations "
                "(ε = 4/255). Retains clean accuracy while substantially hardening against FGSM attacks."
            ),
            "clean": (
                "**Clean-trained** — trained on standard unperturbed crops. "
                "Achieves highest clean-input AUC (0.9745)."
            ),
        }
        st.caption(descriptions[model_key])

        st.markdown('<hr style="margin:.5rem 0 1rem">', unsafe_allow_html=True)

        # ── Stress-test toggle ───────────────────────────────────────────────
        with st.expander("⚙ Advanced options"):
            with_stress = st.checkbox(
                "Enable stress test (FGSM attack on clip — adds extra time)",
                value=False,
                help="Applies a single-step FGSM perturbation (ε = 1/255) using the model's own prediction "
                     "as target. Shows clean vs attacked probability for BOTH models.",
            )

        # ── STEP 1: Input ────────────────────────────────────────────────────
        st.markdown('<div class="step-num">Step 1</div>', unsafe_allow_html=True)
        st.markdown("### Input")

        input_mode = st.radio(
            "Source",
            ["Choose a sample clip", "Upload a clip"],
            horizontal=True,
            label_visibility="collapsed",
        )

        video_path = None
        video_name = None
        temp_file_to_clean = None
        is_sample_mode = False
        sample_ground_truth = None

        samples_dir = _ROOT / "samples"
        cached_dict = _load_cached_results()

        if input_mode == "Choose a sample clip":
            is_sample_mode = True
            sample_files = sorted(list(samples_dir.glob("*.mp4")) + list(samples_dir.glob("*.avi")) + list(samples_dir.glob("*.mov")))
            if not sample_files:
                st.warning("No sample clips found in `samples/` directory.")
                return
            else:
                st.markdown("<p style='font-size:0.85rem;color:var(--ink-muted);margin-bottom:0.5rem;'>Select from pre-computed test clips:</p>", unsafe_allow_html=True)
                sample_cols = st.columns(len(sample_files))
                selected_sample = st.session_state.get("selected_sample", sample_files[0].name)

                for idx, sfile in enumerate(sample_files):
                    with sample_cols[idx]:
                        thumb_path = samples_dir / "cache" / sfile.stem / "fgsm" / "face_box.jpg"
                        gt = cached_dict.get(sfile.name, {}).get("ground_truth", "fake" if "fake" in sfile.name else "real")
                        gt_color = "#3D6B4F" if gt == "real" else "#C45A00"

                        if thumb_path.exists():
                            st.image(str(thumb_path), use_container_width=True)

                        st.markdown(
                            f"<div style='text-align:center;font-size:0.75rem;font-family:var(--mono);'>"
                            f"<strong>{sfile.name}</strong><br>"
                            f"<span style='display:inline-block;padding:1px 6px;margin-top:2px;border-radius:2px;background:{gt_color}1A;color:{gt_color};font-weight:700;font-size:0.68rem;'>"
                            f"Ground truth: {gt.upper()}</span></div>",
                            unsafe_allow_html=True
                        )
                        btn_label = "Selected" if selected_sample == sfile.name else "Select"
                        if st.button(btn_label, key=f"sel_{sfile.name}", use_container_width=True):
                            st.session_state["selected_sample"] = sfile.name
                            selected_sample = sfile.name
                            st.rerun()

                video_name = selected_sample
                video_path = str(samples_dir / selected_sample)
                sample_ground_truth = cached_dict.get(video_name, {}).get("ground_truth", "fake" if "fake" in video_name else "real")

                st.markdown("""
<div style="background:#EDE8DF;border-left:3px solid #1A1612;padding:0.4rem 0.8rem;margin:0.8rem 0;font-family:var(--mono);font-size:0.8rem;">
  ⚡ <strong>SAMPLE MODE:</strong> Pre-computed result loads instantly. Stored stage timings are replayed below.
</div>
""", unsafe_allow_html=True)

        else:
            # Upload mode
            is_sample_mode = False
            uploaded = st.file_uploader(
                "Upload video",
                type=["mp4", "mov", "avi"],
                label_visibility="collapsed",
                help="Max 50 MB · Max 30 s · MP4, MOV, AVI",
            )
            if uploaded is not None:
                video_name = uploaded.name
                size_mb = len(uploaded.getvalue()) / 1e6

                # Edge case: file over 50 MB
                if size_mb > 50.0:
                    st.markdown(f"""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>File Size Exceeded:</strong> Uploaded video is {size_mb:.1f} MB. Maximum allowed size is 50.0 MB.
</div>
""", unsafe_allow_html=True)
                    return

                # Write to temp file safely
                suffix = Path(uploaded.name).suffix.lower()
                if suffix not in [".mp4", ".mov", ".avi"]:
                    st.markdown("""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Unsupported Format:</strong> Please upload an MP4, MOV, or AVI video file.
</div>
""", unsafe_allow_html=True)
                    return

                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                tfile.write(uploaded.getvalue())
                tfile.flush()
                tfile.close()
                video_path = tfile.name
                temp_file_to_clean = tfile.name

                st.markdown("""
<div style="background:#F0F4F8;border-left:3px solid #00558F;padding:0.4rem 0.8rem;margin:0.8rem 0;font-family:var(--mono);font-size:0.8rem;color:#00335A;">
  🔴 <strong>LIVE INFERENCE MODE:</strong> Uploaded video will be processed directly through the EfficientNet-B1 + LSTM model pipeline.
</div>
""", unsafe_allow_html=True)

        # Empty state handling
        if not video_path:
            st.markdown("""
<div style="background:#F9F7F2;border:1px dashed #C8BFB0;padding:2rem;text-align:center;border-radius:2px;margin:1rem 0;">
  <p style="font-family:var(--serif);font-size:1.1rem;margin-bottom:0.4rem;color:var(--ink);">Awaiting Video Input</p>
  <p style="font-family:var(--sans);font-size:0.85rem;color:var(--ink-muted);margin:0;">
    Select one of the sample benchmark clips above for instant evaluation, or switch to upload mode to submit an MP4/MOV clip for live inference.
  </p>
</div>
""", unsafe_allow_html=True)
            return

        # Pre-verify video integrity & duration before deep processing
        try:
            test_cap = cv2.VideoCapture(video_path)
            if not test_cap.isOpened():
                st.markdown("""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Unreadable Video:</strong> Could not open the video file. It may be corrupt or encoded in an unsupported codec.
</div>
""", unsafe_allow_html=True)
                if temp_file_to_clean and os.path.exists(temp_file_to_clean):
                    os.remove(temp_file_to_clean)
                return

            frame_count = int(test_cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = test_cap.get(cv2.CAP_PROP_FPS) or 25.0
            test_cap.release()

            if frame_count <= 0:
                st.markdown("""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Empty Clip:</strong> Video contains 0 readable frames.
</div>
""", unsafe_allow_html=True)
                if temp_file_to_clean and os.path.exists(temp_file_to_clean):
                    os.remove(temp_file_to_clean)
                return

            duration_s = frame_count / fps if fps > 0 else 0
            if duration_s > 30.0:
                st.markdown(f"""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Duration Limit Exceeded:</strong> Clip duration is {duration_s:.1f} s. Maximum allowed duration is 30.0 s.
</div>
""", unsafe_allow_html=True)
                if temp_file_to_clean and os.path.exists(temp_file_to_clean):
                    os.remove(temp_file_to_clean)
                return
        except Exception as e_check:
            _log_error("Video verification check", e_check)
            st.markdown(f"""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Corrupt Video File:</strong> Failed to verify video properties: {e_check}
</div>
""", unsafe_allow_html=True)
            if temp_file_to_clean and os.path.exists(temp_file_to_clean):
                os.remove(temp_file_to_clean)
            return

        st.markdown('<hr style="margin:.8rem 0 1rem">', unsafe_allow_html=True)

        # ── STEP 2: Processing ───────────────────────────────────────────────
        st.markdown('<div class="step-num">Step 2</div>', unsafe_allow_html=True)
        st.markdown("### Processing")

        # Tensor shape readout
        st.markdown("""
<div class="tensor-shape">
  <span class="shape">[16, 3, 224, 224]</span>
  <span class="arrow">→ EfficientNet-B1 →</span>
  <span class="shape">[16, 1280]</span>
  <span class="arrow">→ Projection →</span>
  <span class="shape">[16, 512]</span>
  <span class="arrow">→ LSTM (2L) →</span>
  <span class="shape">[16, 512]</span>
  <span class="arrow">→ mean-pool →</span>
  <span class="shape">[1 logit]</span>
</div>
""", unsafe_allow_html=True)
        st.markdown('<div style="margin:.6rem 0"></div>', unsafe_allow_html=True)

        run_key = f"analysis_{video_name}_{model_key}_{with_stress}_{input_mode}"

        has_cache = False
        cached_clip_data = None
        if is_sample_mode and video_name in cached_dict:
            clip_models = cached_dict[video_name].get("models", {})
            if model_key in clip_models:
                cached_clip_data = clip_models[model_key]
                has_cache = True

        if run_key not in st.session_state:
            btn_text = "⚡ Load pre-computed result" if (is_sample_mode and has_cache) else "▶ Run analysis"
            is_running = st.session_state.get("is_running", False)

            if st.button(btn_text, type="primary", disabled=is_running):
                st.session_state["is_running"] = True
                try:
                    if is_sample_mode and has_cache:
                        with st.status("Replaying pre-computed analysis…", expanded=True) as status_box:
                            for s in cached_clip_data["stages"]:
                                time.sleep(min(0.08, max(0.01, s["ms"] / 4000.0)))
                                display_name = s["name"].replace("_", " ").title()
                                st.write(f"✓ **{display_name}** — {_fmt_ms(s['ms'])}")
                            status_box.update(label="Pre-computed result loaded.", state="complete", expanded=False)

                        loaded_res = dict(cached_clip_data)
                        crops = []
                        for cp in cached_clip_data["evidence"]["crop_paths"]:
                            p = _ROOT / cp
                            if p.exists():
                                bgr = cv2.imread(str(p))
                                crops.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
                        loaded_res["evidence"]["frames"] = crops

                        box_p = _ROOT / cached_clip_data["evidence"]["face_box_path"]
                        if box_p.exists():
                            bgr = cv2.imread(str(box_p))
                            loaded_res["evidence"]["first_frame_rgb"] = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

                        cam_imgs = []
                        for gp in cached_clip_data["explain"]["gradcam_paths"]:
                            p = _ROOT / gp
                            if p.exists():
                                bgr = cv2.imread(str(p))
                                cam_imgs.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
                        loaded_res["explain"]["cam_frames"] = cam_imgs
                        loaded_res["explain"]["gradcam"] = cam_imgs

                        st.session_state[run_key] = loaded_res
                        st.session_state["is_running"] = False
                        st.rerun()

                    else:
                        if not _INFERENCE_AVAILABLE:
                            st.markdown("""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:0.6rem 0.8rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.85rem;color:#721C24;">
  <strong>Inference Module Unavailable:</strong> Could not load inference engine.
</div>
""", unsafe_allow_html=True)
                            st.session_state["is_running"] = False
                            return

                        with st.status("Analysing video live…", expanded=True) as status_box:
                            def _progress_cb(stage_name, ms):
                                display_name = stage_name.replace("_", " ").title()
                                st.write(f"✓ **{display_name}** — {_fmt_ms(ms)}")

                            result = analyze_video(
                                path=video_path,
                                model=model_key,
                                with_stress=with_stress,
                                progress_cb=_progress_cb,
                            )
                            status_box.update(label="Analysis complete.", state="complete", expanded=False)

                        st.session_state[run_key] = result
                        st.session_state["is_running"] = False
                        st.rerun()

                except Exception as ex:
                    _log_error("Model forward pass / analysis", ex)
                    st.session_state["is_running"] = False
                    st.markdown(f"""
<div style="background:#FDE8E8;border-left:3px solid #D32F2F;padding:1rem;margin:0.8rem 0;font-family:var(--sans);font-size:0.9rem;color:#721C24;border-radius:2px;">
  <strong>Analysis could not be completed</strong>
  <p style="margin:0.4rem 0;font-size:0.82rem;">Reason: {str(ex)}</p>
  <p style="margin:0.4rem 0 0 0;font-size:0.75rem;color:#999;font-family:var(--mono);">Full diagnostic details recorded to error.log</p>
</div>
""", unsafe_allow_html=True)
                    if st.button("↺ Retry analysis"):
                        st.rerun()
                    return

                finally:
                    if temp_file_to_clean and os.path.exists(temp_file_to_clean):
                        try:
                            os.remove(temp_file_to_clean)
                        except Exception:
                            pass
            return

        result = st.session_state[run_key]

        # Stage timings table
        total_ms = sum(s["ms"] for s in result["stages"])
        with st.expander(f"Stage timings (total: {_fmt_ms(total_ms)})", expanded=False):
            rows_html = "".join(
                f"<tr><td style='font-family:var(--mono)'>{s['name'].replace('_',' ').title()}</td>"
                f"<td style='font-family:var(--mono);text-align:right'>{_fmt_ms(s['ms'])}</td></tr>"
                for s in result["stages"]
            )
            st.markdown(f"""
<table>
  <thead><tr><th>Stage</th><th style="text-align:right">Time</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>""", unsafe_allow_html=True)

        # Show real metadata
        meta = result["evidence"]["video_meta"]
        m_cols = st.columns(4)
        with m_cols[0]:
            st.metric("Duration", f"{meta['duration_s']:.1f} s")
        with m_cols[1]:
            st.metric("Resolution", f"{meta['width']} × {meta['height']}")
        with m_cols[2]:
            st.metric("FPS", f"{meta['fps']:.1f}")
        with m_cols[3]:
            st.metric("Frames", f"{meta['frame_count']}")

        # Face detection fallback warning
        if result["evidence"]["used_fallback_crop"]:
            st.markdown("""
<div style="background:#FFF3CD;border-left:3px solid #856404;padding:0.6rem 0.8rem;margin:0.6rem 0;font-family:var(--sans);font-size:0.85rem;color:#856404;">
  <strong>Notice:</strong> No stable face trajectory was detected by Haar cascades across the sampled frames.
  A central square crop fallback was used. Verdict has been flagged as <strong>INCONCLUSIVE</strong>.
</div>
""", unsafe_allow_html=True)

        # Multiple face note if detection rate indicates multiple candidate boxes
        if result["evidence"]["face_detect_rate"] > 0.8:
            st.caption("ℹ Face detection selected the primary (largest) face box across frames as specified in the evaluation protocol.")

        # Show detected face box on first frame
        if "first_frame_rgb" in result["evidence"]:
            with st.expander("Detected face bounding box (frame 0)", expanded=False):
                box = result["evidence"]["detected_box"]
                st.image(
                    result["evidence"]["first_frame_rgb"],
                    caption=f"Haar cascade detection [x0={box[0]}, y0={box[1]}, x1={box[2]}, y1={box[3]}] (margin 1.3×)",
                    width=280,
                )

        # Show 16 sampled face crops
        st.markdown('<p class="label-sc" style="margin-top:.8rem">16 sampled face crops</p>', unsafe_allow_html=True)
        _render_frame_sheet(result["evidence"]["frames"], result["evidence"]["frame_indices"])

        st.markdown('<hr style="margin:.8rem 0 1rem">', unsafe_allow_html=True)

        # ── STEP 3: Output ───────────────────────────────────────────────────
        st.markdown('<div class="step-num">Step 3</div>', unsafe_allow_html=True)
        st.markdown("### Output")

        # Ground truth badge if in sample mode
        if is_sample_mode and sample_ground_truth:
            gt_col = "#3D6B4F" if sample_ground_truth == "real" else "#C45A00"
            st.markdown(f"""
<div style="display:inline-block;padding:3px 10px;margin-bottom:0.6rem;border:1px solid {gt_col};background:{gt_col}15;color:{gt_col};font-family:var(--mono);font-size:0.8rem;font-weight:700;border-radius:2px;">
  GROUND TRUTH: {sample_ground_truth.upper()} (Sample Clip)
</div>
""", unsafe_allow_html=True)

        # Pre-computed vs live badge
        if is_sample_mode and has_cache:
            st.markdown("""
<span style="display:inline-block;padding:2px 8px;margin-bottom:0.6rem;background:#EDE8DF;color:#1A1612;font-family:var(--mono);font-size:0.75rem;border-radius:2px;">
  ⚡ PRE-COMPUTED RESULT (Cached)
</span>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
<span style="display:inline-block;padding:2px 8px;margin-bottom:0.6rem;background:#F0F4F8;color:#00335A;font-family:var(--mono);font-size:0.75rem;border-radius:2px;">
  🔴 LIVE INFERENCE RESULT
</span>
""", unsafe_allow_html=True)

        # Case-ID badge
        if "case_id" not in st.session_state:
            st.session_state["case_id"] = _case_id()
        st.markdown(
            f'<div class="case-id">{st.session_state["case_id"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="label-sc" style="margin:.3rem 0 .6rem">'
            f'Model: {result["model"]["name"]} · v{result["model"]["version"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Real Verdict banner
        _render_verdict(
            result["verdict"],
            result["probability"],
            result["threshold"],
            result["evidence"]["used_fallback_crop"],
        )

        # Gauge with real probability & threshold
        _render_gauge(result["probability"], result["threshold"], result["verdict"])

        st.markdown('<div style="margin:.6rem 0"></div>', unsafe_allow_html=True)

        # Grad-CAM contact sheet
        st.markdown('<p class="label-sc">Grad-CAM evidence</p>', unsafe_allow_html=True)
        st.caption(
            "Heatmaps indicate spatial regions that influenced the prediction. "
            "Layer hooked: EfficientNet-B1 block 8 (model.feature_extractor[0][-1])."
        )
        show_overlay = st.toggle("Show Grad-CAM overlay", value=True)
        _render_heatmap_sheet(
            result["explain"]["cam_frames"],
            result["explain"]["gradcam"],
            [result["evidence"]["frame_indices"][i] for i in result["explain"]["cam_frame_indices"]],
            overlay=show_overlay,
        )

        # Stress-test panel (if enabled or present in cache)
        if result.get("stress") is not None:
            st.markdown('<hr style="margin:.8rem 0">', unsafe_allow_html=True)
            st.markdown('<p class="label-sc">Stress test — FGSM (ε = 1/255)</p>', unsafe_allow_html=True)
            st.markdown("""
<div class="stress-warning">
The true label is <strong>unknown</strong> at inference — the model's own prediction was used as the
attack target (label_source="pred"). &nbsp;·&nbsp; <strong>FGSM only. This is not evidence of general adversarial robustness.</strong>
</div>
""", unsafe_allow_html=True)
            s = result["stress"]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Clean-trained model**")
                st.metric("Clean P(fake)",    f'{s["models"]["clean"]["clean_prob"]:.4f}')
                st.metric("Attacked P(fake)", f'{s["models"]["clean"]["attacked_prob"]:.4f}')
            with c2:
                st.markdown("**FGSM-trained model**")
                st.metric("Clean P(fake)",    f'{s["models"]["fgsm"]["clean_prob"]:.4f}')
                st.metric("Attacked P(fake)", f'{s["models"]["fgsm"]["attacked_prob"]:.4f}')

        # Evidence details table
        with st.expander("Evidence details"):
            ev = result["evidence"]
            st.markdown(f"""
<table>
<thead><tr><th>Attribute</th><th>Value</th></tr></thead>
<tbody>
  <tr><td>Face detect rate</td><td style="font-family:var(--mono)">{ev['face_detect_rate']:.0%}</td></tr>
  <tr><td>Fallback crop used</td><td style="font-family:var(--mono)">{'Yes ⚠' if ev['used_fallback_crop'] else 'No'}</td></tr>
  <tr><td>Raw logit</td><td style="font-family:var(--mono)">{result.get('raw_logit', 0.0):+.4f}</td></tr>
  <tr><td>Temperature T</td><td style="font-family:var(--mono)">{result.get('T', 1.0):.4f}</td></tr>
  <tr><td>Trained on</td><td style="font-family:var(--mono)">{result['model']['trained_on']}</td></tr>
  <tr><td>Total inference time</td><td style="font-family:var(--mono)">{_fmt_ms(total_ms)}</td></tr>
</tbody>
</table>""", unsafe_allow_html=True)

        # Download report button
        st.markdown('<hr style="margin:.8rem 0">', unsafe_allow_html=True)
        st.markdown('<p class="label-sc">Report</p>', unsafe_allow_html=True)
        report_html = _generate_html_report(st.session_state["case_id"], result)
        st.download_button(
            label="⬇ Download report (HTML)",
            data=report_html,
            file_name=f"{st.session_state['case_id'].replace(' · ', '_').replace(' ', '_')}.html",
            mime="text/html",
        )


render()
