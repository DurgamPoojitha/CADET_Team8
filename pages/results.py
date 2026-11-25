"""
pages/results.py — Results page.
Two tabs: Video (full existing content) and Image (coming-soon panel).
All video content lives in components/video_results.py.
All image content lives in components/image_results.py.
"""
import sys
from pathlib import Path
import streamlit as st

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from components.video_results import render as _video_render
from components.image_results import render as _image_render


def render():
    st.markdown("## Results")

    tab_video, tab_image = st.tabs(["📹 Video", "🖼 Image"])

    with tab_video:
        _video_render()

    with tab_image:
        _image_render()


render()
