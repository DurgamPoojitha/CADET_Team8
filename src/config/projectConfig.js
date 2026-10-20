/**
 * Centralized Project Configuration for CADET Documentation Portal
 * 
 * Source of Truth:
 * - Project Phase 2 Presentation & Implementation Updates
 * - IEEE Conference Paper: "Compression-Aware Explainable Bimodal Deepfake Detection for Image and Video Analysis"
 * - Project Proposal & Progress Milestones
 */

export const projectConfig = {
  // Official Project Identity
  title: "Compression-Aware Explainable Bimodal Deepfake Detection for Image and Video Analysis",
  acronym: "CADET",
  acronymFull: "Compression-Aware Deepfake & Explanation Technology",
  tagline: "An explainable, compression-resilient bimodal deepfake detection framework for image and video forensics in social media streams.",

  // Project Status: Phase 2 (100% Completed)
  status: {
    badge: "Project Phase 2 (100% Completed)",
    state: "Phase 2 Implementation Fully Completed",
    phase: "Project Phase 2",
    progressPercent: 100,
    note: "All Phase 2 implementation pipelines, bimodal models, compression-aware preprocessing, FGSM adversarial robustness training, cross-dataset generalization, and Grad-CAM explainability modules are 100% completed and verified.",
  },

  // Centralized URLs & Placeholders
  urls: {
    github: "https://github.com/DurgamPoojitha/CADET_Team8",
    liveDemo: "https://durgampoojitha.github.io/CADET_Team8/",
    isLiveDemoPlaceholder: false,
    institution: "https://www.amrita.edu",
    conferencePaperPlaceholder: "#",
  },

  // Academic Affiliation & Team 08 Details
  academic: {
    institution: "Amrita Vishwa Vidyapeetham",
    school: "Amrita School of Computing",
    department: "Department of Computer Science and Engineering",
    campus: "Coimbatore, Tamil Nadu, India",
    phase: "Project Phase 2",
    projectType: "Research-Based Project",
    teamNumber: "08",
    teamId: "Team 08",
    guide: {
      name: "Dr. Lalithamani N",
      designation: "Associate Professor",
      department: "Department of Computer Science and Engineering",
      institution: "Amrita Vishwa Vidyapeetham",
      email: "n_lalitha@cb.amrita.edu"
    },
    students: [
      { name: "Durgam Poojitha", regNo: "CB.SC.U4CSE23320" },
      { name: "Alana Mariya P C", regNo: "CB.SC.U4CSE23205" },
      { name: "Sidharth S Nair", regNo: "CB.SC.U4CSE23443" },
      { name: "Akshay Krishna P S", regNo: "CB.SC.U4CSE23403" },
      { name: "Kalyani H Karuvelil", regNo: "CB.SC.U4CSE23423" }
    ]
  },

  // Key Objectives (Phase 2 Focused including FGSM & Cross-Dataset Generalization)
  objectives: [
    {
      id: "bimodal-architecture",
      title: "Bimodal Image & Video Detection Pipeline",
      summary: "Deploying XceptionNet with depthwise-separable convolutions for static spatial artifact extraction, alongside EfficientNet-B1 coupled with a 2-layer uni-directional LSTM for spatiotemporal video sequence anomaly detection across 16-frame sequences.",
      source: "Project Phase 2 Methodology"
    },
    {
      id: "compression-preprocessing",
      title: "Compression-Aware Preprocessing (CBP)",
      summary: "Simulating authentic social-media degradation by applying dynamic area downscaling, bilinear upscaling, Gaussian blurring, and low-quality JPEG re-encoding (quality 10–25) to 70% of training data to harden model feature representations against compression artifacts.",
      source: "Project Phase 2 Data Pipeline"
    },
    {
      id: "adversarial-robustness",
      title: "Adversarial Robustness Training (FGSM)",
      summary: "Hardening the deepfake detection models against malicious evasion attacks and subtle perturbation noise through Fast Gradient Sign Method (FGSM) adversarial training, generating imperceptibly altered adversarial samples to enforce invariant feature learning.",
      source: "Project Phase 2 Robust ML"
    },
    {
      id: "cross-dataset-generalization",
      title: "Cross-Dataset Generalization & Open-Set Testing",
      summary: "Validating cross-domain generalization across multiple independent benchmark datasets—including CelebDF, 140K Faces, and FaceForensics++—using balanced sampling to prevent dataset bias and guarantee robust detection of unseen generation techniques.",
      source: "Project Phase 2 Generalization"
    },
    {
      id: "explainable-ai",
      title: "Visual Interpretability via Grad-CAM",
      summary: "Integrating Gradient-weighted Class Activation Mapping across pre-final convolutional layers (conv4 on XceptionNet and per-frame on EfficientNet) to generate visual heatmaps that pinpoint facial manipulation regions such as eyes, mouth, and seam boundaries for transparent forensic inspection.",
      source: "Project Phase 2 Explainability"
    }
  ]
};
