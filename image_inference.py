"""
image_inference.py — stub for the image analysis module.
A teammate implements this with the same result schema as analyze_video().
"""


def analyze_image(path: str) -> dict:
    """Analyse a still image for deepfake traces.

    Args:
        path: Absolute path to the image file (jpg / png / webp).

    Returns:
        A result dict matching the shared schema:
        {
            verdict: "manipulated" | "authentic" | "inconclusive",
            probability: float,
            threshold: float,
            stages: [{name, ms}],
            evidence: {frames, frame_indices, face_detect_rate, used_fallback_crop, video_meta},
            explain: {gradcam: [ndarray]},
            stress: None,
            model: {name, version, trained_on},
        }

    Raises:
        NotImplementedError: Always — module not yet implemented.
    """
    raise NotImplementedError(
        "Image analysis is not yet implemented. "
        "This module will be completed by a teammate using the same result schema."
    )
