"""
components/image_method.py
"Coming soon" panel for the Image tab on the Method page.

HOW TO FILL IN (teammate instructions):
  1. Replace the render() body below with your actual image pipeline content.
  2. Use the same st.markdown / st.columns / st.image calls as video_method.py.
  3. No numbers, model names or claims should be added until real results exist.
"""
import streamlit as st
from pathlib import Path

_ROOT = Path(__file__).parent.parent
# Image results live here (separate from video):
_IMAGE_RESULTS_DIR = _ROOT / "models_image" / "results"


def _results_available() -> bool:
    """Returns True only when models_image/results/ exists and contains files."""
    return _IMAGE_RESULTS_DIR.exists() and any(_IMAGE_RESULTS_DIR.iterdir())


def render():
    if _results_available():
        # ── Teammate: replace this block with real image method content ──────
        st.info("Image method content not yet implemented. Edit components/image_method.py.")
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
    once the model and pipeline are finalised.
  </p>
  <p class="label-sc" style="color:var(--ink-muted);font-size:.7rem;margin-bottom:.5rem">
    This tab will show
  </p>
  <ul style="color:var(--ink-muted);font-size:.85rem;margin:0;padding-left:1.2rem;line-height:1.9">
    <li>Image preprocessing and face-crop pipeline diagram</li>
    <li>Model architecture description</li>
    <li>Calibration and threshold methodology</li>
    <li>Explainability approach (Grad-CAM or equivalent)</li>
  </ul>
</div>
""", unsafe_allow_html=True)
