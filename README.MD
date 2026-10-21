# CADET: Compression-Aware Explainable Bimodal Deepfake Detection Documentation Portal

[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Routing](https://img.shields.io/badge/Router-HashRouter-F44250?style=flat)](https://reactrouter.com/)
[![GitHub Pages](https://img.shields.io/badge/Deployment-GitHub%20Pages-222222?style=flat&logo=github)](https://pages.github.com/)
[![Status](https://img.shields.io/badge/Status-Project%20Phase%202%20(100%25%20Completed)-0d9488?style=flat)]()

Official academic documentation portal for **CADET (Compression-Aware Deepfake & Explanation Technology)** — *Compression-Aware Explainable Bimodal Deepfake Detection for Image and Video Analysis*.

Conducted at **Amrita Vishwa Vidyapeetham**, School of Computing, Department of Computer Science and Engineering, Coimbatore, India (Project Phase 2, Team 08, Research-Based Project).

---

## 1. Project Background & Fact Summary

All information presented on this portal is strictly derived from the three verified primary documents:
1. **IEEE Conference Paper - Draft**: *Compression-Aware Explainable Bimodal Deepfake Detection for Image and Video Analysis*
2. **Project Presentation (PR2)**: *23CSE399 Phase 1 Panel Review 2 (Team 08, March 28, 2026)*
3. **Project Report**: *Phase 1 Review 2 Report, Department of CSE, Amrita Vishwa Vidyapeetham*

### Core Highlights & Model Specifications

| Component | Architecture / Method | Dataset & Scope | Verified Metrics | Implementation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Image Detector** | Pretrained **XceptionNet** Backbone (2048-dim features) + FC(512) + 10% Dropout + FC(1) + Sigmoid | **140k Real & Fake Faces** (70,000 Flickr real + 70,000 StyleGAN fake) | **99.76% Accuracy**, 99.78% Precision, 99.73% Recall, 99.75% F1-Score | **Completed & Verified** *(IEEE Paper Draft Sec. IV-G & Table II)* |
| **Video Detector** | Pretrained **EfficientNet-B1** (1280-dim spatial) + 2-layer uni-directional **LSTM** (512 hidden, 0.1 dropout, temporal mean pooling) + FC(256) + 10% Dropout + FC(1) + Sigmoid | **FaceForensics++** (6,000 videos: 1,000 real + 5,000 fakes across Deepfakes, Face2Face, FaceShifter, FaceSwap, NeuralTextures; 16 frames/video) | **79.00% Accuracy**, 79.03% Precision, 79.00% Recall, 78.99% F1-Score, **0.8703 AUC-ROC** | **Completed & Verified** *(IEEE Paper Draft Sec. IV-H & Table I)* |
| **Preprocessing** | **Compression-Based Preprocessing (CBP)**: Area downscaling ($s \sim U(0.85, 1.0)$), Bilinear upscaling, Gaussian blur ($5\times 5, p=0.7$), and JPEG buffers ($q \in [10, 25]$) | Simulates real-world lossy compression observed on social media streams | Mitigates severe compression degradation | **Completed & Implemented** *(IEEE Paper Draft Sec. IV-C)* |
| **Explainable AI (XAI)** | **Grad-CAM** (Gradient-Weighted Class Activation Mapping) on pre-final convolutional layers | Highlights salient facial manipulation regions (eyes, mouth, boundary blending) | Deletion-based faithfulness **$AUC_{\text{del}} = 0.4579$** | **Completed & Implemented** *(IEEE Paper Draft Sec. IV-I & Fig. 6)* |
| **Adversarial Hardening** | **Adversarial Robustness Training (ART)** | Defense against adversarial perturbations and noise attacks | Proposed Enhancement | **Scheduled for Future Phase** *(IEEE Paper Draft Sec. VII)* |
| **Generalization** | Evaluation across unseen diffusion-generated faces | Cross-dataset testing | Proposed Enhancement | **Scheduled for Future Phase** *(IEEE Paper Draft Sec. VII)* |

---

## 2. Repository File Tree

```
project-docs/
├── .github/
│   └── workflows/
│       └── deploy.yml              # Automated GitHub Pages build & deploy workflow
├── public/
│   └── assets/
│       └── architecture/
│           ├── cadet_architecture.png   # Cropped PR2 System Architecture diagram
│           └── cadet_ieee_arch.png      # Cropped IEEE Conference Paper architecture figure
├── src/
│   ├── components/
│   │   ├── Navbar.jsx              # Responsive navigation with active link indicators
│   │   ├── Footer.jsx              # Understated academic footer with citations & team info
│   │   └── UnimplementedNotice.jsx # Route helper rendering notice for progress page
│   ├── config/
│   │   └── projectConfig.js        # Centralized configuration (URLs, status, facts, metrics)
│   ├── pages/
│   │   ├── Overview.jsx            # Page 1: Complete Project Overview (FULLY IMPLEMENTED)
│   │   ├── Documentation.jsx       # Page 2: Technical Documentation (FULLY IMPLEMENTED)
│   │   └── Progress.jsx            # Page 3: Empty placeholder file (0 bytes)
│   ├── styles/
│   │   └── global.css              # Custom academic design system (Burgundy & Navy theme)
│   ├── App.jsx                     # Root router using HashRouter for GitHub Pages
│   └── main.jsx                    # React 18 DOM mount entrypoint
├── index.html                      # HTML template with metadata and typography
├── package.json                    # Project dependencies and npm scripts
├── vite.config.js                  # Vite configuration with relative base deployment
└── README.md                       # Comprehensive portal documentation
```

### Note on Page Implementation Status
**Page 1 (`Overview.jsx`)** and **Page 2 (`Documentation.jsx`)** are implemented with complete UI and interactive elements, with the technical documentation covering system architecture, model specifications, benchmark corpora grouped by detector and methodology. In response to the scope remaining for later phase, **Page 3 (`Progress.jsx`)** is maintained as an empty placeholder file, and routing handles the `/progress` path gracefully through `UnimplementedNotice.jsx` without populating the empty file.

---

## 3. Step-by-Step Terminal Commands

### Prerequisites
- Node.js `v18+` or `v20+` (LTS recommended)
- npm `v9+` or `v10+`
- Git

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Local Development Server
```bash
npm run dev
```
Navigate to `http://localhost:5173` in your browser.

### 3. Run Production Build
```bash
npm run build
```
Build output is generated into the `dist/` directory.

### 4. Preview Production Build Locally
```bash
npm run preview
```

---

## 4. How to Configure URLs and Project Status

All project metadata, URLs, and status indicators are centralized in `src/config/projectConfig.js` for instant updates without modifying components:

```javascript
// src/config/projectConfig.js

export const projectConfig = {
  // Update your project status here:
  status: {
    badge: "Phase 1 & Experimental Validation Completed",
    state: "Research & Benchmark Evaluation Completed",
    requiresConfirmation: true, // set to false once confirmed with faculty
    note: "Status established from IEEE conference submission & PR2 review."
  },

  urls: {
    // 1. GitHub Repository URL (replace or confirm):
    github: "https://github.com/DurgamPoojitha/CADET_Team8",

    // 2. Live Demo URL (replace with actual deployment URL when live):
    liveDemo: "https://durgampoojitha.github.io/CADET_Team8/",
    isLiveDemoPlaceholder: false // set to true if showing placeholder tag
  }
};
```

---

## 5. GitHub Pages Deployment Guide

### Option A: Automated GitHub Actions (Recommended)
This repository includes `.github/workflows/deploy.yml`. When pushed to your GitHub repository:
1. Push this project code to your GitHub repository (e.g., `https://github.com/DurgamPoojitha/CADET_Team8`).
2. On GitHub, go to your repository **Settings** &rarr; **Pages**.
3. Under **Build and deployment** &rarr; **Source**, select **GitHub Actions**.
4. Push a commit to `main` (or run manually via **Actions** &rarr; **Deploy CADET Portal to GitHub Pages** &rarr; **Run workflow**).
5. Your site will automatically build and publish at `https://<username>.github.io/<repo-name>/`.

### Option B: Manual Deployment via `gh-pages`
If you prefer deploying the `dist` folder directly:
```bash
npm install -D gh-pages
npx gh-pages -d dist
```

---

## 6. Verification Checklist

- [x] **Project Facts Accuracy**: Title, acronym (CADET), models (XceptionNet, EfficientNet-B1, LSTM, Grad-CAM, CBP), and datasets (140k Faces, FaceForensics++) match uploaded PDFs.
- [x] **Distinction of Work**: Implemented models and reported metrics (99.76% image, 79.00% video) are clearly distinguished from future enhancements (ART, diffusion testing).
- [x] **Page 1 Complete**: `Overview.jsx` includes Hero, Objectives, Architecture breakdown, Tech highlights, Metrics, Status badge, and Academic team credits.
- [x] **Page 2 Complete**: `Documentation.jsx` includes the Architecture diagram, Model specifications, Datasets grouped by detector, Methodology and References, with the register of project report applied throughout to all prose.
- [x] **Progress Placeholder**: `Progress.jsx` exists and is strictly 0 bytes.
- [x] **Router Stability**: Uses `HashRouter` to prevent GitHub Pages 404 errors on page reload.
- [x] **Relative Base Path**: `vite.config.js` uses relative base (`./`) ensuring assets load on any GitHub Pages subpath.
- [x] **Build Verification**: `npm run build` succeeds cleanly without warnings or errors.
- [x] **Responsive UI**: Fully tested on desktop, tablet, and mobile screen layouts.
