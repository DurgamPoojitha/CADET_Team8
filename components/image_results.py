"""
components/image_results.py
"Coming soon" panel for the Image tab on the Results page.

HOW TO FILL IN (teammate instructions):
  1. Put your result files (CSVs, JSONs, figures) under models_image/results/.
  2. Replace the render() body below with real tables, charts and figures,
     following the same patterns as components/video_results.py.
  3. analyze_image(path) must return the same schema as analyze_video():
       verdict, probability, raw_logit, threshold, T, stages,
       evidence, explain, stress, model
  4. Do NOT invent numbers — read everything from files in models_image/results/.
"""
import streamlit as st
from pathlib import Path

_ROOT = Path(__file__).parent.parent
_IMAGE_RESULTS_DIR = _ROOT / "models_image" / "results"


def _results_available() -> bool:
    """Returns True only when models_image/results/ exists and contains files."""
    return _IMAGE_RESULTS_DIR.exists() and any(_IMAGE_RESULTS_DIR.iterdir())


def render():
    if _results_available():
        # ── Teammate: replace this block with real image results content ─────
        st.info(
            f"Image results files found in `{_IMAGE_RESULTS_DIR.relative_to(_ROOT)}`. "
            "Edit `components/image_results.py` to display them."
        )
        return

    # ── Coming-soon panel ────────────────────────────────────────────────────
    st.markdown("""
<div style="
  border: 1.5px dashed var(--border);
  border-radius: 4px;
  padding: 2rem 2.4rem;
  background: var(--surface);
  margin: 1.2rem 0;
">
  <p class="label-sc" style="color:var(--ink-muted);margin-bottom:.4rem">In development</p>
  <h3 style="margin:0 0 .6rem;font-size:1.15rem;color:var(--ink)">
    Image detector: in development
  </h3>
  <p style="color:var(--ink-muted);font-size:.9rem;margin-bottom:1.2rem">
    The image analysis module is being built separately and will appear here
    once evaluation is complete and result files are available.
  </p>
  <p class="label-sc" style="color:var(--ink-muted);font-size:.7rem;margin-bottom:.5rem">
    This tab will show
  </p>
  <ul style="color:var(--ink-muted);font-size:.85rem;margin:0;padding-left:1.2rem;line-height:1.9">
    <li>Clean test accuracy and AUC for the image model</li>
    <li>Per-manipulation detection-rate breakdown</li>
    <li>Acceptance-criteria table</li>
    <li>Training figures and Grad-CAM examples</li>
  </ul>
</div>
""", unsafe_allow_html=True)
