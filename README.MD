# CADET — Compression-Aware Explainable Bimodal Deepfake Detection

**CADET (Compression-Aware Deepfake & Explanation Technology)** is a research project focused on detecting deepfakes in images and videos, even when the media has been compressed or modified before being shared online.

The project is developed by Team 08 at Amrita Vishwa Vidyapeetham, under the guidance of Dr. Lalithamani N.

## 1. Problem Statement

AI-generated images and videos have become increasingly realistic, making it difficult to distinguish manipulated media from genuine content. Deepfakes can be used to spread misinformation, impersonate individuals, and misuse someone's identity.

One of the main challenges is that deepfake detection models may perform well on high-quality media but struggle when the same content is uploaded to social media platforms. Compression, resizing, blurring, and repeated JPEG encoding can remove or weaken the visual traces that detectors use to identify manipulation.

Another challenge is that a prediction alone does not explain why an image or video was classified as real or fake. This makes it harder to inspect and trust the model's decision.

CADET addresses these challenges by combining image and video detection, compression-aware preprocessing, adversarial robustness training, and visual explanations in a single framework.

## 2. Why CADET?

The project focuses on three practical problems:

- **Detection after compression:** Media shared online often loses quality. The framework introduces compression-related changes during training to help the detectors handle these conditions.
- **Resistance to adversarial changes:** Small, deliberately introduced perturbations can affect a model's prediction. Adversarial Robustness Training (ART) is used to train the detectors with perturbed samples.
- **Understandable predictions:** Grad-CAM generates heatmaps that highlight image regions contributing to a prediction, helping users inspect the model's decision.

The goal is not just to classify media as real or fake, but to study how reliably the detectors perform under challenging conditions and how their predictions can be interpreted.

## 3. What Does the Framework Contain?

CADET uses two detection pipelines because images and videos contain different types of information.

### Image Deepfake Detection

The image branch uses a pretrained **XceptionNet** model with a custom classification head to distinguish real and manipulated facial images.

It is trained using real and fake face images, with compression-based preprocessing and adversarial training incorporated into the workflow. Grad-CAM is used to examine the regions that influence the model's predictions.

### Video Deepfake Detection

The video branch uses **EfficientNet-B1** to extract spatial features from video frames and a two-layer, unidirectional **LSTM** to learn patterns across sequences of 16 frames.

Unlike a detector that examines only one frame, this pipeline can use information from multiple frames to identify inconsistencies across time. The video workflow also includes compression-aware preprocessing, adversarial robustness training, and visual explanations.

### Compression-Based Preprocessing

The Compression-Based Preprocessing (CBP) stage simulates some of the quality changes that occur when media is shared online. Depending on the sample, these changes include:

- Image downscaling and resizing.
- Gaussian blurring.
- JPEG re-encoding at low quality settings.

According to the project's Phase 2 methodology, these transformations are applied to 70% of training samples, while the remaining samples retain their original form.

### Adversarial Robustness Training (ART)

Adversarial Robustness Training uses the **Fast Gradient Sign Method (FGSM)** to generate perturbed training samples. The detectors are trained with these samples to study and improve their resistance to small, deliberately introduced input changes.

ART is incorporated into both the image and video workflows. Its effectiveness is evaluated by comparing model performance under the relevant test conditions.

### Explainability with Grad-CAM

**Gradient-weighted Class Activation Mapping (Grad-CAM)** produces heatmaps showing which spatial regions contributed to a model's prediction.

For the image branch, the heatmaps help inspect facial regions associated with a classification. For the video branch, explanations can be generated for individual frames.

These visualisations provide an additional way to examine model behaviour instead of relying entirely on a real/fake label.

### Cross-Dataset Evaluation

A detector may learn patterns specific to its training dataset rather than general characteristics of deepfakes. To investigate this, CADET evaluates its models using multiple datasets containing different identities and manipulation methods.

This helps assess whether the detectors can generalise to data that differs from the data used during training.

## 4. Datasets

The project uses separate datasets for image and video detection.

| Dataset | Purpose |
|---|---|
| 140K Real & Fake Faces | Initial image detection training and validation |
| Celeb-DF | Evaluation of image and video detection on additional deepfake data |
| FaceForensics++ | Image frames and videos containing different manipulation methods |
| Celeb-DF v2 | Cross-dataset evaluation for video detection |
| UADFV | Additional cross-dataset video evaluation |

The precise datasets and splits used depend on the corresponding notebook and experiment. Please refer to each notebook for its actual configuration.

## 5. Repository Structure

The repository is organised around the image detector, video detector, cross-dataset video experiments, and final project materials.

```text
CADET_Team8/
│
├── art_imgfolder/
│   └── Image detector ART training notebooks
│
├── art_videofolder/
│   └── Video detector ART training notebooks
│
├── cross_data_video/
│   └── Cross-dataset video evaluation notebooks
│
├── final_folder/
│   └── Final project notebooks and related materials
│
├── README.MD
└── .gitignore
```

The descriptions above indicate each folder's intended role. Notebook filenames and any additional files may vary as the project develops.

## 6. Running the Notebooks on Kaggle

The experiments are designed to be run through Kaggle Notebooks, which provides a convenient environment for working with datasets and GPU-enabled machine learning workloads.

### Step 1: Open the repository

1. Visit the [CADET_Team8 GitHub repository](https://github.com/DurgamPoojitha/CADET_Team8).
2. Open the folder containing the experiment you want to run.
3. Select the relevant `.ipynb` notebook.
4. Download the notebook using GitHub's download option, or download the repository as a ZIP file.

### Step 2: Open Kaggle

1. Sign in to [Kaggle](https://www.kaggle.com/).
2. Open the **Code** section and create a new notebook, or use the notebook import option if available.
3. Upload the downloaded `.ipynb` file.

### Step 3: Configure the environment

Before running the notebook:

1. Check the imports and install any missing dependencies listed in the notebook.
2. Attach the required datasets using the notebook's **Add Input** option.
3. Verify the dataset paths used in the code.
4. Enable GPU acceleration in the notebook settings if the experiment requires it and GPU access is available.

Dataset paths on Kaggle are generally read from `/kaggle/input/`. Update any paths that refer to a local computer or a different environment.

### Step 4: Run the notebook

Run the cells in order, starting with the imports and configuration.

The notebook may include dataset preparation, preprocessing, model loading, training, validation, evaluation, and visualisation. Follow the execution order already defined in the notebook.

For ART experiments, make sure the correct model checkpoint, dataset split, and training configuration are being used.

### Step 5: Review and save the results

After execution, inspect the evaluation metrics, classification results, and any generated Grad-CAM heatmaps. Save the required model checkpoints, plots, and other outputs before ending the session.

**Important:** Kaggle sessions have resource and execution-time limits. Large datasets and model training can take considerable time, so use the notebook's existing checkpoints and configuration where appropriate. Do not assume that every notebook needs to be trained from scratch.

The project also examines cross-dataset generalisation and the quality of Grad-CAM explanations.

## 8. Team 08

**Institution:** Amrita Vishwa Vidyapeetham  
**Department:** Computer Science and Engineering  
**Location:** Coimbatore, Tamil Nadu, India  
**Project Guide:** Dr. Lalithamani N

| Team member | Contributions |
|---|---|
| Durgam Poojitha | Implemented ART in the video detector; contributed to research paper writing |
| Alana Mariya P C | Implemented ART in the image detector; contributed to research paper writing |
| Sidharth S Nair | Implemented the image detector; worked on cross-dataset evaluation |
| Akshay Krishna P S | Implemented the video detector; worked on cross-dataset evaluation and research paper writing |
| Kalyani H Karuveil | Implemented the video detector; worked on ART in the video detector |

## 9. Project Status

The Phase 2 implementation covers the image and video detection pipelines, compression-aware preprocessing, adversarial robustness training, cross-dataset evaluation, and Grad-CAM explainability.

Further experiments and performance improvements may continue as part of subsequent project phases. The latest results and implementation details should be taken from the corresponding notebooks and project documentation.

## 10. Project Links

- **GitHub Repository:** https://github.com/DurgamPoojitha/CADET_Team8
- **Documentation Portal:** See the project's GitHub Pages documentation portal for the overview, architecture, methodology, model specifications, and project progress.

---

*CADET is an academic research project exploring more robust and interpretable deepfake detection for images and videos.*
