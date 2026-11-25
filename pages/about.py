"""
pages/about.py — About page.
PROJECT_TITLE, Team 8 table, guide, institution.
No photos, no invented bios, no fake social links.
"""
import streamlit as st
from project_info import (
    PROJECT_TITLE, ALT_TITLE, SHOW_ALT_TITLE,
    TEAM_NUMBER, INSTITUTION, GUIDE, TEAM, SITE_NAME, FULL_FORM,
)


def render():
    st.markdown("## About")

    # ── Project title ─────────────────────────────────────────────────────────
    st.markdown(f"### {PROJECT_TITLE}")

    if SHOW_ALT_TITLE:
        st.markdown(
            f'<p class="label-sc">Report title</p>'
            f'<p style="font-family:var(--serif);font-size:1.05rem;font-style:italic">'
            f'{ALT_TITLE}</p>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Team ─────────────────────────────────────────────────────────────────
    st.markdown(f"### Team {TEAM_NUMBER}")

    rows_html = "".join(
        f"<tr>"
        f"<td style='font-family:var(--mono);text-align:center'>{m['sno']}</td>"
        f"<td style='font-family:var(--mono);font-size:.82rem'>{m['reg']}</td>"
        f"<td style='font-family:var(--sans)'>{m['name']}</td>"
        f"</tr>"
        for m in TEAM
    )
    st.markdown(f"""
<table>
  <thead>
    <tr>
      <th style="text-align:center">S.No</th>
      <th>Register Number</th>
      <th>Student Name</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Guide & institution ────────────────────────────────────────────────────
    st.markdown("### Academic information")
    st.markdown(f"""
<table>
  <tbody>
    <tr>
      <td style="font-family:var(--mono);font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-muted);padding-right:1.2rem">Guide</td>
      <td>{GUIDE}</td>
    </tr>
    <tr>
      <td style="font-family:var(--mono);font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-muted)">Institution</td>
      <td>{INSTITUTION}</td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── System description ────────────────────────────────────────────────────
    st.markdown("### System description")
    st.markdown(f"""
**{SITE_NAME}** (*{FULL_FORM}*) is a deepfake video detector
built on top of a bimodal neural architecture combining spatial and temporal analysis.

**Core architecture:** EfficientNet-B1 (spatial frame features) → projection (1280 → 512) →
2-layer LSTM (temporal integration) → mean pooling → binary classifier.

**Key properties:**
- Identity-disjoint train/val/test split across FaceForensics++ C23, Celeb-DF, and UADFV.
- Compression-aware preprocessing: every training crop is re-encoded at JPEG quality 60–95
  to simulate social-media codec degradation.
- Adversarial training variant (FGSM-trained): trained with single-step FGSM perturbations
  (ε = 4/255) to maintain robustness under FGSM-type attacks.
- Grad-CAM spatial explanations for model transparency.
- Temperature-scaled probabilities and EER-calibrated thresholds.

**Version:** v9 (FGSM-only adversarial training, stabilised)
""")

render()
