"""
pages/method.py — Method page.
Pipeline diagram, plain-language explanation of the architecture
and the three ideas behind the CADET-AR name.
"""
import streamlit as st


def render():
    st.markdown("## Method")
    st.caption(
        "A technical overview of the CADET-AR pipeline, model design, "
        "and the three ideas behind the system's name."
    )

    # ── Pipeline diagram ─────────────────────────────────────────────────────
    st.markdown('<p class="label-sc" style="margin-top:.6rem">Analysis pipeline</p>',
                unsafe_allow_html=True)

    st.markdown("""
<div class="pipeline-wrap">
  <div class="pipeline-block"><strong>MP4 / MOV</strong><br>Upload</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Frame<br>sampling<br><em style="font-size:.65rem">32 uniform</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Haar<br>face crop<br><em style="font-size:.65rem">256×256</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block accent">JPEG Q95<br>encode<br>&amp; decode</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">16-frame<br>selection<br><em style="font-size:.65rem">bin midpoints</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Resize<br>224×224<br>ImageNet norm</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block accent">EfficientNet<br>-B1<br><em style="font-size:.65rem">→ 1280-D</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Projection<br>1280 → 512</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block accent">2-layer<br>LSTM<br><em style="font-size:.65rem">hidden=512</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Mean<br>pooling</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Classifier<br>512→256→1<br><em style="font-size:.65rem">logit</em></div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block accent">Temperature<br>calibration<br>+ threshold</div>
  <div class="pipeline-arrow">→</div>
  <div class="pipeline-block">Verdict<br>+ Grad-CAM</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Architecture ─────────────────────────────────────────────────────────
    st.markdown("### Model architecture — EfficientNet-B1 + LSTM")
    st.markdown("""
Each uploaded video is processed as a sequence of **16 face crops**.

**Spatial backbone — EfficientNet-B1**  
A pretrained EfficientNet-B1 (ImageNet weights) acts as a per-frame feature extractor.
Its last classification head is removed; the remaining network maps each 224×224 RGB crop
to a 1280-dimensional feature vector capturing fine-grained facial texture artefacts.
The backbone was fine-tuned (last 5 blocks unfrozen in phase 2) while the earlier
convolutional layers were kept frozen.

**Temporal model — 2-layer LSTM**  
The 16 per-frame vectors (each projected from 1280 to 512 dimensions) are fed sequentially
into a 2-layer unidirectional LSTM with hidden size 512. The LSTM learns to integrate
temporal cues: flickering boundaries, inconsistent blinking, lighting changes across frames.
The 16 LSTM outputs are averaged (mean pooling) and passed to a two-stage classifier
(512 → 256 → 1 logit).

**Output — one logit per clip**  
Positive = FAKE. Calibrated probability P(fake) = sigmoid(logit / T),
where T is the temperature constant fitted on the validation set.
""")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Temperature calibration ───────────────────────────────────────────────
    st.markdown("### Calibration — temperature scaling and threshold")
    st.markdown("""
Raw logit outputs are sharpened or softened by a **temperature scalar T** before
the sigmoid, correcting the confidence miscalibration that is common in deep classifiers.
T is fitted on the validation set by minimising expected calibration error.

A **decision threshold** θ is then chosen by the equal-error-rate (EER) rule on
the validation set: the point where false-positive rate equals false-negative rate.
This avoids the arbitrary θ = 0.5 assumption.

For the **stress test** (FGSM-attacked inputs), a separate *attack-aware threshold*
is fitted on the pooled clean + attacked validation scores, trading some clean
specificity for better attacked-input recall.
""")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Three ideas in the name ───────────────────────────────────────────────
    st.markdown("### The three ideas in CADET-AR")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
**C — Compression Aware**

Social-media platforms re-encode video (JPEG, downscale, H.264 compression).
To match this, **every training face crop is re-encoded** as a JPEG at quality
60–95 (randomly sampled), optionally downscaled by 0.7–1.0×, and optionally
Gaussian-blurred before final resizing.

The evaluation pipeline mimics this exactly (quality 95, no downscale).
The model therefore learned to detect manipulation artefacts that *survive*
codec degradation, not just pixel-perfect originals.
""")

    with col2:
        st.markdown("""
**E — Explanation (Grad-CAM)**

A `VideoGradCAM` hook is attached to the last convolutional block of
EfficientNet-B1 (`model.feature_extractor[0][-1]`).

For 6 evenly-spaced frames, the backward gradient of the logit with
respect to that layer's activations is computed; a weighted sum produces
a spatial heatmap that highlights the pixels that *most influenced the
prediction*. The heatmaps are displayed as overlays on the original crops.

**Caveat:** Grad-CAM localises evidence but does not prove manipulation.
""")

    with col3:
        st.markdown("""
**AR — Adversarially Robust**

The FGSM-trained model uses **adversarial training** with a single-step
Fast Gradient Sign Method (FGSM) perturbation at ε = 4/255 pixels
(training) evaluated at ε = 2/255 (target).

A combined clean+adversarial loss (ALP weight 0.2) is optimised,
so the model learns to be stable under small input perturbations
while retaining clean-data performance (AUC ratio 0.998).

⚠ **Scope:** FGSM only. No PGD, no iterative attacks were evaluated.
This is not a claim of general adversarial robustness.
""")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Clean vs FGSM ────────────────────────────────────────────────────────
    st.markdown("### Clean-trained vs. FGSM-trained")
    st.markdown("""
| | **Clean-trained** | **FGSM-trained** |
|---|---|---|
| Training objective | BCE on clean crops | ALP: 0.8 × BCE(clean) + 0.2 × BCE(FGSM) |
| Clean test AUC | **0.9745** | 0.9727 (ratio 0.998) |
| FGSM test AUC @ ε=2/255 | 0.046 | **0.911** |
| FGSM test accuracy @ ε=2/255 | 14.8 % | **82.5 %** |
| Recommended for | Standard uploads | Adversarially stressed inputs |

The clean-trained model achieves marginally higher clean-input AUC.
The FGSM-trained model sacrifices ≈0.2 % of clean AUC to gain >86 points
of FGSM-attack AUC at the target epsilon.

Both models share the same EfficientNet-B1 + LSTM architecture and preprocessing pipeline;
only the training procedure differs.
""")

    st.markdown('<hr style="margin:.8rem 0 1.2rem">', unsafe_allow_html=True)

    # ── Datasets ─────────────────────────────────────────────────────────────
    st.markdown("### Training data")
    st.markdown("""
The model was trained on three public deepfake benchmarks with an **identity-disjoint split**:
no identity (face) appears in more than one of train / validation / test.

| Dataset | Manipulation types | Note |
|---|---|---|
| FaceForensics++ C23 | Deepfakes, Face2Face, FaceSwap, NeuralTextures, FaceShifter | FF++ compressed (C23) |
| Celeb-DF | Celeb-synthesis (high-quality GAN swaps) | — |
| UADFV | Face-reenactment | — |
""")


render()
