# CADET-AR – 5-Minute Demo Script

**Team 8 · Amrita School of Engineering · Department of CSE**  
*Compression Aware Deepfake Explanation Technology – Adversarially Robust*

---

## Pre-Demo Checklist (do this 10 minutes before)

- [ ] `source venv/bin/activate && streamlit run app.py` — confirm it loads without errors
- [ ] Browser at **http://localhost:8501**, window maximised
- [ ] `samples/cached_results.json` exists (run `python make_samples.py` if not)
- [ ] Have one real clip (`samples/0000.mp4`) and one fake clip (`samples/0000_fake.mp4`) ready on the Desktop as a backup
- [ ] Screen font size bumped to 125 % for projector readability
- [ ] Close all other applications / browser tabs

---

## Timing Map

| Segment | Clock |
|---|---|
| Opening & About page | 0:00 – 0:45 |
| Method page walkthrough | 0:45 – 1:30 |
| Sample real clip demo | 1:30 – 2:30 |
| Sample fake clip demo | 2:30 – 3:15 |
| Adversarial stress demonstration | 3:15 – 3:45 |
| Results page walkthrough | 3:45 – 4:30 |
| Closing & Q-A invitation | 4:30 – 5:00 |

---

## Full Script

### 0:00 – Opening (About page)

> "Good [morning/afternoon]. This is **CADET-AR** — Compression Aware Deepfake Explanation Technology, Adversarially Robust — developed by Team 8 at Amrita School of Engineering under the guidance of Dr. N Lalithamani."

Click **About** in the sidebar.

> "The system detects manipulated faces in video by combining an EfficientNet backbone with a temporal LSTM, trained on FaceForensics++ and Celeb-DF datasets. It is compression-aware and adversarially hardened against FGSM attacks."

Point to the team table.

> "Here is our five-member team. The app only runs inference — no retraining, no cloud calls."

---

### 0:45 – Method page

Click **Method** in the sidebar.

> "The pipeline has four stages. First, Haar-cascade face detection extracts the subject. Each face is put through a JPEG 95 compression roundtrip to simulate social-media codec conditions. Sixteen frames are then fed through EfficientNet-B1 frame-by-frame; temporal patterns are captured by an LSTM. Temperature scaling calibrates the probability output."

Scroll to the Explainability section.

> "Grad-CAM localises the facial regions the model found suspicious. We also run a single-step FGSM adversarial perturbation stress test to show the model does not trivially flip on small input noise."

---

### 1:30 – Real clip demo (sample mode)

Click **Analyse** in the sidebar.

> "On the Analyse page you can upload any MP4, or choose from our pre-computed benchmark clips. I'll start with a **real** clip."

In the **Sample clips** picker, select **0000.mp4** (badge shows "Ground truth: Real").

> "Because this result is pre-computed, it loads instantly — the stage timings you see reflect the actual CPU time it took when we ran the model offline."

Point to the stage progress list as it animates.

> "Face detection, JPEG roundtrip, forward pass, Grad-CAM. All green."

Scroll to the verdict card.

> "Verdict: **Authentic**. Probability of manipulation: around 0.3 %. Well below the 51.3 % threshold for the FGSM-trained model."

Switch the model selector to **Clean-trained** — result reloads from cache with no model call.

> "Switching models is instant because both results are pre-cached. The Clean model also calls this authentic."

---

### 2:30 – Fake clip demo (sample mode)

In the picker, select **0000_fake.mp4** (badge shows "Ground truth: Fake").

> "Now a deepfake. FaceSwap manipulation from FaceForensics++."

Scroll to the verdict card.

> "Verdict: **Manipulated**. The probability of fakeness is well above threshold."

Scroll to the Grad-CAM heatmaps.

> "The heatmaps highlight the cheek and jaw region — exactly where facial blending artefacts appear. The six frames shown are uniformly sampled across the clip."

Scroll to the face crops strip.

> "These are the 16 raw face crops the model actually received. You can verify the pipeline is not operating on the full frame."

---

### 3:15 – Adversarial stress

> "The key research contribution is adversarial robustness. Each analysis includes a **stress test** where we apply an FGSM perturbation at ε = 4/255 — invisible to the human eye — and re-run the classifier."

Scroll to the Adversarial Stress card.

> "The verdict holds. The probability shifts by only a few percentage points. This is because the FGSM-trained model was explicitly hardened against single-step attacks during training."

---

### 3:45 – Results page

Click **Results** in the sidebar.

> "These results come directly from the evaluation notebook — no manual editing."

Point to the AUC table.

> "On the FaceForensics++ C23 test set, the FGSM model achieves an AUC of [read from table]. The clean model scores [read from table]. Both pass the acceptance threshold."

Scroll to the Accuracy vs ε chart.

> "This chart shows how accuracy degrades as we increase FGSM epsilon for each model. The FGSM-trained model retains higher accuracy at higher epsilon values."

Scroll to the per-method breakdown.

> "Per manipulation method: NeuralTextures is the hardest — that is consistent with the literature. FaceSwap and Deepfakes are the strongest performers."

Scroll to the Acceptance Criteria table (C1–C8).

> "All eight acceptance criteria are met. The model passed the AUC threshold, the accuracy threshold, adversarial robustness threshold, multi-seed consistency, and reproducibility checks."

---

### 4:30 – Closing

> "To summarise: CADET-AR is a fully explainable, compression-aware, adversarially robust deepfake video detector. It runs locally, produces calibrated probabilities, and generates Grad-CAM evidence alongside every verdict. Thank you — we're happy to take questions."

---

## Fallback: If the live upload stalls (> 60 s)

Switch to a sample clip immediately — tell the audience:

> "I'll switch to our pre-computed result for this clip, which runs the same pipeline offline. The numbers you see are identical to what you would get from a live run."

The sample mode is visually labelled **"Pre-computed result"** so there is no ambiguity.

---

## Common Questions & Answers

**Q: Does this work on DALL·E / Stable Diffusion fakes?**  
A: Training data covered GAN-based manipulations up to 2022. Diffusion-model fakes are outside the training distribution; performance is unknown — this is listed as a limitation.

**Q: What is temperature scaling?**  
A: A post-hoc calibration method. We learn a single scalar T that divides the logit before sigmoid, making the output probability better calibrated against the validation set.

**Q: Why FGSM and not PGD?**  
A: FGSM adversarial training is the scope of this project. PGD robustness is a future direction; we explicitly state the adversarial robustness claim is limited to single-step FGSM at ε ≤ 4/255.

**Q: Can I upload my own video?**  
A: Yes — the Upload tab on the Analyse page accepts any MP4 up to 50 MB and 30 seconds. It runs the full live pipeline including Grad-CAM and the stress test.

**Q: How long does it take per clip?**  
A: ~35 seconds with Grad-CAM on an M-series MacBook CPU. ~10 seconds for the forward pass alone.

---

*CADET-AR · Research prototype · Not for real-world forensic decisions.*
