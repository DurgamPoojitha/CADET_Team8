"""
app.py — CADET-AR entry point.
Injects CSS, verifies required model files, warms models with st.cache_resource,
and manages page navigation.
Run with:  streamlit run app.py
"""

import os
import sys
from pathlib import Path
import streamlit as st

_ROOT = Path(__file__).parent
sys.path.insert(0, str(_ROOT))

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="CADET-AR · Deepfake Detector",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ───────────────────────────────────────────────────────────────
_CSS_PATH = _ROOT / "assets" / "styles.css"
if _CSS_PATH.exists():
    st.markdown(f"<style>{_CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

from project_info import SITE_NAME, FULL_FORM, TEAM_NUMBER, INSTITUTION, DISCLAIMER

st.markdown(f"""
<div style="margin-bottom:.6rem">
  <div class="cadet-wordmark">{SITE_NAME}</div>
  <div class="cadet-wordmark-rule"></div>
  <div class="cadet-subhead">{FULL_FORM}</div>
  <div class="cadet-team-line" style="margin-top:.3rem">
    Team {TEAM_NUMBER} &nbsp;·&nbsp; {INSTITUTION}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Check for required model & config files ──────────────────────────────────
_REQUIRED_FILES = [
    _ROOT / "models" / "deploy_config.json",
    _ROOT / "models" / "best_clean_model.pth",
    _ROOT / "models" / "best_fgsm_model.pth",
]

_missing = [p for p in _REQUIRED_FILES if not p.exists()]
if _missing:
    missing_list_html = "".join(f"<li><code>{p.relative_to(_ROOT)}</code></li>" for p in _missing)
    st.markdown(f"""
<div style="background:#FFF3CD;border:1px solid #FFEBAA;color:#856404;padding:1rem;border-radius:2px;margin:1rem 0;font-family:var(--sans);">
  <strong style="font-size:1.05rem;">Setup Incomplete: Missing Model Files</strong>
  <p style="margin:0.5rem 0 0.3rem 0;font-size:0.9rem;">
    The application cannot run inference because the following required files were not found:
  </p>
  <ul style="margin:0.3rem 0;font-size:0.85rem;">
    {missing_list_html}
  </ul>
  <p style="margin:0.5rem 0 0 0;font-size:0.85rem;">
    Please copy the trained weights and deploy configuration into the <code>cadet_ar/models/</code> directory as instructed in <code>README.md</code>.
  </p>
</div>
""", unsafe_allow_html=True)
    st.stop()


# ── Model Warming (Cached Resource) ──────────────────────────────────────────
@st.cache_resource(show_spinner="Loading deepfake detection models…")
def _warm_models():
    """Load both models once into memory on startup."""
    try:
        from inference import load_model
        m_fgsm = load_model("fgsm")
        m_clean = load_model("clean")
        return True
    except Exception as ex:
        return str(ex)

_warm_status = _warm_models()
if _warm_status is not True:
    st.error(f"Error loading models: {_warm_status}")


# ── Navigation ───────────────────────────────────────────────────────────────
pages = {
    "Analyse":  "pages/analyse.py",
    "Method":   "pages/method.py",
    "Results":  "pages/results.py",
    "About":    "pages/about.py",
}

# Use query params to track active page
params = st.query_params
active = params.get("page", "Analyse")
if active not in pages:
    active = "Analyse"

# Render nav tabs at top level
cols = st.columns(len(pages))
for i, (name, _) in enumerate(pages.items()):
    with cols[i]:
        style = "font-weight:700;border-bottom:2px solid var(--ink);" if name == active else ""
        if st.button(name, key=f"nav_{name}", use_container_width=True):
            st.query_params["page"] = name
            st.rerun()

st.markdown('<hr style="margin:.4rem 0 1.2rem">', unsafe_allow_html=True)

# ── Dispatch to page module ──────────────────────────────────────────────────
import importlib.util

page_file = _ROOT / pages[active]
spec = importlib.util.spec_from_file_location(f"cadet_page_{active}", page_file)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cadet-footer">
  {SITE_NAME} &nbsp;·&nbsp; Team {TEAM_NUMBER} &nbsp;·&nbsp; {INSTITUTION}
</div>
""", unsafe_allow_html=True)
