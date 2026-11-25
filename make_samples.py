"""
make_samples.py — Pre-compute cached results for all sample clips.
Stage 3: runs analyze_video() over samples/*.mp4 for BOTH models (fgsm and clean),
with the stress test enabled.
Saves images under samples/cache/<clip_name>/ and writes samples/cached_results.json.
Prints a summary table at the end.
"""

import os
import sys
import json
from pathlib import Path
import cv2
import numpy as np

# Ensure cadet_ar directory is on sys.path
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from inference import analyze_video


def to_py_type(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return [to_py_type(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: to_py_type(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_py_type(x) for x in obj]
    return obj


def save_image(img_rgb: np.ndarray, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(out_path), img_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])


def main():
    samples_dir = ROOT / "samples"
    cache_dir = samples_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = samples_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest_list = json.load(f)
            manifest = {item["file"]: item for item in manifest_list}

    mp4_files = sorted(samples_dir.glob("*.mp4"))
    if not mp4_files:
        print("No .mp4 files found in samples/ directory.")
        return

    cached_results = {}
    summary_rows = []

    print(f"Found {len(mp4_files)} sample clips. Processing both FGSM and Clean models with stress test...\n")

    for mp4 in mp4_files:
        clip_name = mp4.stem  # e.g. 0000, 0000_fake
        clip_cache_dir = cache_dir / clip_name
        clip_cache_dir.mkdir(parents=True, exist_ok=True)

        true_label = manifest.get(mp4.name, {}).get("label")
        if not true_label:
            true_label = "fake" if "fake" in mp4.name.lower() else "real"
        source_group = manifest.get(mp4.name, {}).get("source_group", "FaceForensics++")

        cached_results[mp4.name] = {
            "file": mp4.name,
            "clip_name": clip_name,
            "ground_truth": true_label,
            "source_group": source_group,
            "models": {}
        }

        # Run for both models
        for m_name in ["fgsm", "clean"]:
            print(f"[{clip_name}] Running model: {m_name.upper()} (with stress test)...")
            res = analyze_video(str(mp4), model=m_name, with_stress=True)

            model_cache_dir = clip_cache_dir / m_name
            model_cache_dir.mkdir(parents=True, exist_ok=True)

            # 1. Save face crops
            crop_paths = []
            for i, crop_rgb in enumerate(res["evidence"]["frames"]):
                c_rel_path = f"samples/cache/{clip_name}/{m_name}/crop_{i:02d}.jpg"
                save_image(crop_rgb, ROOT / c_rel_path)
                crop_paths.append(c_rel_path)

            # 2. Save face box frame
            box_frame_rel = f"samples/cache/{clip_name}/{m_name}/face_box.jpg"
            save_image(res["evidence"]["first_frame_rgb"], ROOT / box_frame_rel)

            # 3. Save Grad-CAM overlays
            cam_paths = []
            for i, (cam_frame, h_map) in enumerate(zip(res["explain"]["cam_frames"], res["explain"]["gradcam"])):
                h_res = cv2.resize(h_map, (cam_frame.shape[1], cam_frame.shape[0]))
                colour = cv2.applyColorMap(np.uint8(255 * h_res), cv2.COLORMAP_JET)
                colour_rgb = cv2.cvtColor(colour, cv2.COLOR_BGR2RGB)
                blended = cv2.addWeighted(cam_frame, 0.6, colour_rgb, 0.4, 0)

                cam_rel_path = f"samples/cache/{clip_name}/{m_name}/gradcam_{i:02d}.jpg"
                save_image(blended, ROOT / cam_rel_path)
                cam_paths.append(cam_rel_path)

            # Build serializable result dict with to_py_type conversions
            serializable_res = {
                "verdict": res["verdict"],
                "probability": float(res["probability"]),
                "raw_logit": float(res["raw_logit"]),
                "threshold": float(res["threshold"]),
                "T": float(res["T"]),
                "stages": to_py_type(res["stages"]),
                "evidence": {
                    "crop_paths": crop_paths,
                    "face_box_path": box_frame_rel,
                    "frame_indices": to_py_type(res["evidence"]["frame_indices"]),
                    "face_detect_rate": float(res["evidence"]["face_detect_rate"]),
                    "used_fallback_crop": bool(res["evidence"]["used_fallback_crop"]),
                    "detected_box": to_py_type(res["evidence"]["detected_box"]),
                    "video_meta": to_py_type(res["evidence"]["video_meta"]),
                },
                "explain": {
                    "gradcam_paths": cam_paths,
                    "cam_frame_indices": to_py_type(res["explain"]["cam_frame_indices"]),
                },
                "stress": to_py_type(res["stress"]),
                "model": to_py_type(res["model"]),
            }

            cached_results[mp4.name]["models"][m_name] = serializable_res

            # Correctness evaluation
            verdict = res["verdict"]
            prob = res["probability"]
            is_correct = "Yes" if (verdict == "manipulated" and true_label == "fake") or \
                                  (verdict == "authentic" and true_label == "real") else "No"
            if verdict == "inconclusive":
                is_correct = "No (Inconclusive)"

            summary_rows.append({
                "clip": mp4.name,
                "ground_truth": true_label,
                "model": m_name,
                "p_fake": prob,
                "verdict": verdict,
                "correct": is_correct
            })

    # Write samples/cached_results.json
    out_json_path = samples_dir / "cached_results.json"
    with open(out_json_path, "w") as f:
        json.dump(cached_results, f, indent=2)
    print(f"\nSaved cached results to {out_json_path}")

    # Print Summary Table
    print("\n" + "="*85)
    print(f"{'Clip':<16} | {'Ground Truth':<12} | {'Model':<7} | {'P(fake)':<8} | {'Verdict':<12} | {'Correct?':<12}")
    print("-" * 85)
    n_correct = 0
    total = len(summary_rows)
    for row in summary_rows:
        corr = row["correct"]
        if corr == "Yes":
            n_correct += 1
        print(f"{row['clip']:<16} | {row['ground_truth']:<12} | {row['model']:<7} | {row['p_fake']:<8.4f} | {row['verdict']:<12} | {corr:<12}")
    print("=" * 85)
    acc = (n_correct / total) * 100 if total > 0 else 0
    print(f"Overall Accuracy: {n_correct}/{total} ({acc:.1f}%)\n")


if __name__ == "__main__":
    main()
