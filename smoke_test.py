"""
CADET-AR Automated Smoke Test Suite
Verifies:
1. Model checkpoints exist and load
2. deploy_config.json has all required keys
3. Live inference on a benchmark clip produces the correct result schema
4. Pre-computed sample cache (samples/cached_results.json) integrity
5. Results metadata and figure assets exist

Exit code: 0 = all pass, 1 = one or more failures.
"""

import sys
import os
import json
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(condition, message):
    global PASS_COUNT, FAIL_COUNT
    tag = "[PASS]" if condition else "[FAIL]"
    print(f"{tag} {message}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def main():
    print("=" * 60)
    print(" CADET-AR SMOKE TEST SUITE")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    # 1. deploy_config.json
    # ------------------------------------------------------------------ #
    config_path = os.path.join(BASE_DIR, "models", "deploy_config.json")
    check(os.path.exists(config_path), "deploy_config.json exists")
    cfg = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            cfg = json.load(f)
        for key in ["clean_T", "clean_threshold", "fgsm_T", "fgsm_threshold"]:
            check(key in cfg, f"deploy_config.json has key '{key}' = {cfg.get(key)}")

    # ------------------------------------------------------------------ #
    # 2. Checkpoint files
    # ------------------------------------------------------------------ #
    clean_ckpt = os.path.join(BASE_DIR, "models", "best_clean_model.pth")
    fgsm_ckpt  = os.path.join(BASE_DIR, "models", "best_fgsm_model.pth")
    check(os.path.exists(clean_ckpt), f"Clean checkpoint exists ({os.path.getsize(clean_ckpt):,} bytes)")
    check(os.path.exists(fgsm_ckpt),  f"FGSM checkpoint exists  ({os.path.getsize(fgsm_ckpt):,} bytes)")

    # ------------------------------------------------------------------ #
    # 3. Model loading
    # ------------------------------------------------------------------ #
    print("\n--- Model Loading ---")
    try:
        from inference import load_model, analyze_video
    except Exception as e:
        check(False, f"Cannot import inference.py: {e}")
        return 1

    for mname in ("clean", "fgsm"):
        t0 = time.time()
        try:
            m = load_model(mname)
            check(m is not None, f"load_model('{mname}') succeeded in {time.time()-t0:.2f}s")
        except Exception as e:
            check(False, f"load_model('{mname}') raised: {e}")

    # ------------------------------------------------------------------ #
    # 4. Live inference – schema validation (no_stress to save time)
    # ------------------------------------------------------------------ #
    print("\n--- Live Inference on samples/0000.mp4 (FGSM model, with_stress=False) ---")
    sample_video = os.path.join(BASE_DIR, "samples", "0000.mp4")
    check(os.path.exists(sample_video), "Sample clip exists: samples/0000.mp4")

    res = None
    if os.path.exists(sample_video):
        try:
            t0  = time.time()
            res = analyze_video(sample_video, model="fgsm", with_stress=False)
            elapsed = time.time() - t0
            print(f"  Inference completed in {elapsed:.2f}s")
        except Exception as e:
            import traceback
            traceback.print_exc()
            check(False, f"analyze_video raised: {e}")

    if res is not None:
        # Top-level keys (actual schema from inference.py)
        for k in ["verdict", "probability", "raw_logit", "threshold", "T",
                  "stages", "evidence", "explain", "stress", "model"]:
            check(k in res, f"Result has key '{k}'")

        # Verdict must be one of three values
        check(res.get("verdict") in {"authentic", "manipulated", "inconclusive"},
              f"Verdict is valid: '{res.get('verdict')}'")

        # Probability in unit interval
        prob = res.get("probability", -1)
        check(0.0 <= prob <= 1.0, f"probability ∈ [0,1]: {prob:.6f}")

        # stages is a list of dicts with {name, ms}
        stages = res.get("stages", [])
        check(isinstance(stages, list) and len(stages) >= 3,
              f"stages is a list with ≥3 entries (got {len(stages)})")
        stage_names = [s.get("name") for s in stages if isinstance(s, dict)]
        for sn in ["face_detection", "frame_sampling", "feature_extraction", "temporal_model"]:
            check(sn in stage_names, f"stages contains '{sn}'")

        # evidence sub-keys (actual keys: frames, frame_indices, face_detect_rate, …)
        ev = res.get("evidence", {})
        for k in ["frames", "frame_indices", "face_detect_rate",
                  "used_fallback_crop", "detected_box", "first_frame_rgb", "video_meta"]:
            check(k in ev, f"evidence has key '{k}'")
        frames = ev.get("frames", [])
        check(len(frames) == 16, f"evidence.frames has 16 entries (got {len(frames)})")

        # explain sub-keys (actual keys: gradcam, cam_frames, cam_frame_indices)
        ex = res.get("explain", {})
        for k in ["gradcam", "cam_frames", "cam_frame_indices"]:
            check(k in ex, f"explain has key '{k}'")
        cam_maps = ex.get("gradcam", [])
        check(len(cam_maps) == 6, f"explain.gradcam has 6 entries (got {len(cam_maps)})")

        # stress is None when with_stress=False, dict when enabled
        check(res.get("stress") is None or isinstance(res.get("stress"), dict),
              "stress is None or dict")

        # model info
        minfo = res.get("model", {})
        check("name" in minfo and "version" in minfo, f"model info has name/version: {minfo}")

    # ------------------------------------------------------------------ #
    # 5. Cached samples JSON integrity
    # ------------------------------------------------------------------ #
    print("\n--- Cached Samples & Manifest ---")
    manifest_path = os.path.join(BASE_DIR, "samples", "manifest.json")
    check(os.path.exists(manifest_path), "samples/manifest.json exists")

    cache_json = os.path.join(BASE_DIR, "samples", "cached_results.json")
    check(os.path.exists(cache_json), "samples/cached_results.json exists")
    if os.path.exists(cache_json):
        with open(cache_json) as f:
            cache_data = json.load(f)
        expected_clips = ["0000.mp4", "0000_fake.mp4", "0013.mp4", "0013_fake.mp4"]
        check(len(cache_data) == 4, f"Cache has 4 clips (found {len(cache_data)})")
        for clip in expected_clips:
            entry = cache_data.get(clip, {})
            models_dict = entry.get("models", {})
            check("fgsm" in models_dict and "clean" in models_dict,
                  f"'{clip}' has both 'fgsm' and 'clean' caches")
            check("ground_truth" in entry, f"'{clip}' has ground_truth label")

    # ------------------------------------------------------------------ #
    # 6. Results page data and figures
    # ------------------------------------------------------------------ #
    print("\n--- Results Page Assets ---")
    results_dir = os.path.join(BASE_DIR, "models", "results")
    for fn in [
        "acceptance_criteria.json",
        "fgsm_v9_metrics.csv",
        "fgsm_v9_per_method.csv",
        "fgsm_v9_results_summary.json",
        "fgsm_v9_multiseed.csv",
        "fgsm_v9_paired_comparison.csv",
        "fgsm_v9_final_summary.md",
    ]:
        check(os.path.exists(os.path.join(results_dir, fn)), f"results/{fn} exists")

    figures_dir = os.path.join(results_dir, "figures")
    n_figs = len(os.listdir(figures_dir)) if os.path.isdir(figures_dir) else 0
    check(n_figs > 0, f"models/results/figures/ contains {n_figs} items")

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #
    total = PASS_COUNT + FAIL_COUNT
    print("\n" + "=" * 60)
    print(f" SMOKE TEST SUMMARY:  {PASS_COUNT}/{total} PASSED  |  {FAIL_COUNT} FAILED")
    print("=" * 60)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
