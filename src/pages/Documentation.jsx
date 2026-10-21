import React from 'react';
import { Link } from 'react-router-dom';
import {
  Cpu,
  Database,
  Workflow,
  Image as ImageIcon,
  Film,
  Github,
  ExternalLink
} from 'lucide-react';
import { projectConfig } from '../config/projectConfig';

/* The architecture diagram is held as a single asset entry. */
const ARCH_DIAGRAM = {
  src: `${import.meta.env.BASE_URL}assets/architecture/cadet_architecture.png`,
  alt: 'Architecture diagram of the CADET pipeline produced for the Phase 2 panel review.',
  caption:
    'Architecture diagram of CADET, covering the image branch, video branch, compression-aware preprocessing and explanation modules.'
};

/* Image detector figures come from updated Phase 2 evaluation records. */
const IMAGE_SPEC = [
  { label: 'Backbone', value: 'Pretrained XceptionNet with custom FC head, 299 x 299 input' },
  { label: 'Optimisation', value: 'AdamW, discriminative learning rates (backbone 1e-5, head 1e-3)' },
  { label: 'Combined Dataset', value: '140K Real & Fake Faces, Celeb-DF frames and FaceForensics++ frames' },
  { label: 'Compression pipeline', value: 'Blur and JPEG re-encode applied to 70% of training images' },
  { label: 'Clean-trained accuracy', value: '92.68%' },
  { label: 'Clean-trained F1-score', value: '92.74%' },
  { label: 'FGSM-trained accuracy', value: '44.33%' },
  { label: 'FGSM-trained F1-Score', value: '31.03%' }
];

/* Video detector figures come from executed notebook runs. */
const VIDEO_SPEC = [
  { label: 'Backbone', value: 'Pretrained EfficientNet-B1, 1280-dimensional spatial features' },
  { label: 'Optimisation', value: 'AdamW, with weight decay configured as 1e-3' },
  { label: 'Temporal model', value: '2-layer unidirectional Long Short-Term Memory (LSTM), 512 hidden units' },
  { label: 'Combined Dataset', value: 'FaceForensics++ C23, Celeb-DF, UADFV' },
  { label: 'Compression pipeline', value: 'Blur and JPEG re-encode applied to 70% of training images' },
  { label: 'Clean-trained accuracy', value: '87.17%' },
  { label: 'Clean-trained F1-Score', value: '87.15%' },
  { label: 'FGSM-trained accuracy', value: '86.42%' },
  { label: 'FGSM-trained F1-Score', value: '86.40%' },
];

/* Corpora are grouped by the detector branch that employs them. */
const IMAGE_DATASETS = [
  {
    name: '140k Real & Fake Faces',
    tag: 'Initial Dataset',
    text:
      'The dataset of 140k Real & Fake Faces consists of 70,000 images sourced from Flickr and 70,000 images produced by StyleGAN, and it was employed for training and validation of the image branch.'
  },
  {
    name: 'Celebrity DeepFake (Celeb-DF)',
    tag: 'Cross-Dataset',
    text:
      'Celebrity DeepFake (Celeb-DF) corpus was added to the image branch during Phase 2, in which held-out face images are employed for evaluation on unseen generators.'
  },
  {
    name: 'FaceForensics++ Frames',
    tag: 'Cross-Dataset',
    text:
      'FaceForensics++ frames were included in the image branch with balanced train, validation and test splits, so that comparison with the video branch remains possible.'
  }
];

const VIDEO_DATASETS = [
  {
    name: 'FaceForensics++ C23',
    tag: 'Initial Dataset',
    text:
      'FaceForensics++ at C23 compression comprises 6,000 videos, of which 1,000 are genuine and 5,000 contain five face-swap manipulations, namely Deepfakes, Face2Face, FaceShifter, FaceSwap and NeuralTextures.'
  },
  {
    name: 'Celebrity DeepFake v2 (Celeb-DF v2)',
    tag: 'Cross-Dataset',
    text:
      'Celebrity DeepFake version 2 (Celeb-DF v2) is employed for cross-dataset evaluation of the video detector, in which detection of unseen generation techniques is examined.'
  },
  {
    name: 'Unmasking AI-Generated Videos (UADFV)',
    tag: 'Cross-Dataset',
    text:
      'Unmasking AI-Generated DeepFake Videos (UADFV) dataset completes the cross-dataset study.'
  }
];

/* Techniques were introduced during Project Phase 2. */
const METHODS = [
  {
    num: '01',
    title: 'Compression-Based Preprocessing',
    tag: 'Data Pipeline',
    paragraphs: [
      'The Compression-Based Preprocessing (CBP) step was introduced in response to the degradation observed in media shared across social platforms.',
      'Summary on the working of the stage is provided below: an area downscale with factor sampled from a uniform distribution between 0.85 and 1.0 is applied first, after which bilinear upscaling, a Gaussian blur of 5×5 kernel at probability 0.7 and JPEG re-encoding at quality factors between 10 and 25 are carried out on 70% of training samples.',
      'This was applied to 70% of training samples during dataset preparation, while the remaining samples were kept in their original form.'
    ]
  },
  {
    num: '02',
    title: 'Adversarial Robustness Training',
    tag: 'Robust ML',
    paragraphs: [
      'Fast Gradient Sign Method (FGSM) adversarial training was incorporated so that invariance to perturbations levied against the classifier could be enforced during optimisation.',
      'As a result, adversarial samples carrying imperceptible noise were generated during training, and the models were retrained on the augmented dataset.',
      'The robustness study was carried out during Phase 2.'
    ]
  },
  {
    num: '03',
    title: 'Grad-CAM Explainability',
    tag: 'XAI',
    paragraphs: [
      'Gradient-weighted Class Activation Mapping (Grad-CAM) heatmaps were generated on the pre-final convolutional layers, that is the conv4 branch of XceptionNet and the per-frame maps of EfficientNet-B1.',
      'A small handful heatmaps were retained for qualitative review, while the remainder was discarded after scoring.',
      'The deletion-based faithfulness score was recorded as 0.3870 over 50 evaluated videos, which indicates moderate confidence of the explanation module for the time being.'
    ]
  }
];



/* Main Component */
export default function Documentation() {
  return (
    <div className="doc-root">

      {/* Hero section mirrors the Overview layout. */}
      <section className="doc-hero">
        <div className="container doc-hero-inner">

          <div className="doc-meta-strip">
            <span className="doc-meta-tag">Amrita Vishwa Vidyapeetham</span>
            <span className="doc-meta-sep">·</span>
            <span className="doc-meta-tag">Team 08</span>
            <span className="doc-meta-sep">·</span>
            <span className="doc-meta-tag">Technical Reference</span>
            <span className="doc-meta-sep">·</span>
            <span className="doc-status-dot-wrap">
              <span className="doc-status-dot" />
              <span className="doc-meta-tag doc-status-text">Phase 2 Completed</span>
            </span>
          </div>

          <h1 className="doc-title">Technical Documentation</h1>

          <div className="doc-acronym-line">
            <span className="doc-acronym-badge">{projectConfig.acronym}</span>
            <span className="doc-acronym-sep">—</span>
            <span className="doc-acronym-expansion">{projectConfig.acronymFull}</span>
          </div>

          <div className="doc-summary-grid">
            <div className="doc-summary-col doc-summary-col-lead">
              <p className="doc-summary-lead">
                The present document constitutes the technical reference for the
                Compression-Aware Deepfake &amp; Explanation Technology (CADET) framework,
                which was developed at Amrita Vishwa Vidyapeetham under the supervision of
                Lalithamani N, Department of Computer Science and Engineering.
              </p>
            </div>

            <div className="doc-summary-col doc-summary-col-body">
              <p className="doc-summary-body doc-summary-body--spaced">
                The material presented herein is derived from verified sources, namely the
                updated notebook runs and the Phase 2 evaluation records.
              </p>
              <div className="doc-cta-row">
                <a
                  href={projectConfig.urls.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="doc-btn doc-btn-primary"
                >
                  <Github size={16} />
                  <span>GitHub Repository</span>
                  <ExternalLink size={13} className="doc-btn-ext" />
                </a>
                <Link to="/" className="doc-btn doc-btn-ghost">
                  <span>Project Overview</span>
                </Link>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Architecture section presents the single pipeline diagram. */}
      <section className="doc-section">
        <div className="container">
          <div className="doc-sec-header">
            <span className="doc-sec-eyebrow">System Architecture · Phase 2 Methodology</span>
            <h2 className="doc-sec-title">Architecture Diagram</h2>
            <p className="doc-sec-intro">
              The architecture of the CADET framework is presented below, featuring the compression preprocessing,
              adversarial robustness training and bimodal approach with explainability.
            </p>
          </div>

          <figure className="doc-figure">
            <div className="doc-figure-frame">
              <img
                src={ARCH_DIAGRAM.src}
                alt={ARCH_DIAGRAM.alt}
                loading="lazy"
              />
            </div>
            <figcaption className="doc-figure-caption">{ARCH_DIAGRAM.caption}</figcaption>
          </figure>
        </div>
      </section>

      {/* Specification tables were verified against updated runs. */}
      <section className="doc-section doc-section--alt">
        <div className="container">
          <div className="doc-sec-header">
            <span className="doc-sec-eyebrow">Model Reference · Verified Metrics</span>
            <h2 className="doc-sec-title">CADET Specifications</h2>
            <p className="doc-sec-intro">
              The two detectors that constitute the bimodal pipeline are documented below,
              with architecture details, datasets and verified metrics presented for
              each branch.
            </p>
          </div>

          <div className="doc-spec-grid">
            <div className="doc-spec-card">
              <div className="doc-spec-head">
                <span className="doc-spec-icon"><Cpu size={16} /></span>
                <h3 className="doc-spec-title">Image Detector</h3>
                <span className="badge badge-success">Completed &amp; Verified</span>
              </div>
              <dl className="doc-spec-list">
                {IMAGE_SPEC.map((row) => (
                  <div className="doc-spec-row" key={row.label}>
                    <dt className="doc-spec-label">{row.label}</dt>
                    <dd className="doc-spec-value">{row.value}</dd>
                  </div>
                ))}
              </dl>
            </div>

            <div className="doc-spec-card">
              <div className="doc-spec-head">
                <span className="doc-spec-icon"><Workflow size={16} /></span>
                <h3 className="doc-spec-title">Video Detector</h3>
                <span className="badge badge-success">Completed &amp; Verified</span>
              </div>
              <dl className="doc-spec-list">
                {VIDEO_SPEC.map((row) => (
                  <div className="doc-spec-row" key={row.label}>
                    <dt className="doc-spec-label">{row.label}</dt>
                    <dd className="doc-spec-value">{row.value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>

          <p className="doc-closing-note">
            The performance metrics given here are the latest metrics from the work started for phase 3. These metrics do not reflect final submission performance.
          </p>
        </div>
      </section>

      {/* Datasets section groups corpora by detector branch. */}
      <section className="doc-section">
        <div className="container">
          <div className="doc-sec-header">
            <span className="doc-sec-eyebrow">Datasets · Training and Evaluation</span>
            <h2 className="doc-sec-title">Datasets in Use</h2>
            <p className="doc-sec-intro">
              The following section higlights the datasets that were used for training, validating and testing the models.
            </p>
          </div>

          <div className="doc-dataset-group">
            <div className="doc-dataset-group-head">
              <span className="doc-dataset-group-icon"><ImageIcon size={15} /></span>
              <h3 className="doc-dataset-group-title">Datasets for the Image Detector</h3>
            </div>
            <div className="doc-dataset-grid">
              {IMAGE_DATASETS.map((d) => (
                <div className="doc-dataset-card" key={d.name}>
                  <div className="doc-dataset-head">
                    <span className="doc-dataset-icon"><Database size={15} /></span>
                    <span className="doc-dataset-tag">{d.tag}</span>
                  </div>
                  <h4 className="doc-dataset-name">{d.name}</h4>
                  <p className="doc-dataset-text">{d.text}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="doc-dataset-group">
            <div className="doc-dataset-group-head">
              <span className="doc-dataset-group-icon"><Film size={15} /></span>
              <h3 className="doc-dataset-group-title">Datasets for the Video Detector</h3>
            </div>
            <div className="doc-dataset-grid">
              {VIDEO_DATASETS.map((d) => (
                <div className="doc-dataset-card" key={d.name}>
                  <div className="doc-dataset-head">
                    <span className="doc-dataset-icon"><Database size={15} /></span>
                    <span className="doc-dataset-tag">{d.tag}</span>
                  </div>
                  <h4 className="doc-dataset-name">{d.name}</h4>
                  <p className="doc-dataset-text">{d.text}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>

      {/* Methodology section presents the Phase 2 techniques. */}
      <section className="doc-section doc-section--alt">
        <div className="container">
          <div className="doc-sec-header">
            <span className="doc-sec-eyebrow">Methodology · Phase 2 Techniques</span>
            <h2 className="doc-sec-title">Core Techniques of the Pipeline</h2>
            <p className="doc-sec-intro">
              The three principal techniques introduced during Phase 2 are described below,
              namely the compression-based preprocessing stage, the adversarial robustness
              procedure and the explainability module.
            </p>
          </div>

          <ol className="doc-method-list">
            {METHODS.map((m) => (
              <li className="doc-method-item" key={m.num}>
                <span className="doc-method-num" aria-hidden="true">{m.num}</span>
                <div className="doc-method-body">
                  <div className="doc-method-title-row">
                    <h3 className="doc-method-title">{m.title}</h3>
                    <span className="doc-method-tag">{m.tag}</span>
                  </div>
                  {m.paragraphs.map((p, i) => (
                    <p className="doc-method-text" key={i}>{p}</p>
                  ))}
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>


      {/* Scoped styles follow the Overview design language. */}
      <style>{`
        /* ── Root ── */
        .doc-root {
          display: flex;
          flex-direction: column;
          width: 100%;
        }

        /* ── Hero ── */
        .doc-hero {
          background-color: #faf9f7;
          border-bottom: 1px solid #e8e3dd;
          padding: 3.5rem 0 3.25rem;
        }

        .doc-hero-inner {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        }

        .doc-meta-strip {
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 0.35rem;
          margin-bottom: 1.4rem;
        }

        .doc-meta-tag {
          font-size: 0.78rem;
          font-weight: 500;
          color: #64748b;
          letter-spacing: 0.01em;
        }

        .doc-meta-sep {
          color: #cbd5e1;
          font-size: 0.78rem;
        }

        .doc-status-dot-wrap {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
        }

        .doc-status-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #22c55e;
          flex-shrink: 0;
        }

        .doc-status-text {
          color: #166534;
          font-weight: 600;
        }

        .doc-title {
          font-size: 2.25rem;
          font-weight: 800;
          color: #0f172a;
          line-height: 1.18;
          letter-spacing: -0.035em;
          margin-bottom: 1rem;
          max-width: 860px;
        }

        .doc-acronym-line {
          display: flex;
          align-items: baseline;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 2rem;
        }

        .doc-acronym-badge {
          font-family: var(--font-mono);
          font-size: 0.88rem;
          font-weight: 700;
          color: #7c152a;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          padding: 0.2rem 0.55rem;
          border-radius: 4px;
          letter-spacing: 0.04em;
        }

        .doc-acronym-sep {
          color: #94a3b8;
          font-size: 0.88rem;
        }

        .doc-acronym-expansion {
          font-size: 0.88rem;
          color: #334155;
          font-weight: 500;
        }

        .doc-summary-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2.5rem;
          margin-bottom: 0.5rem;
          max-width: 1100px;
          align-items: start;
        }

        .doc-summary-col {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .doc-summary-lead {
          font-size: 1.025rem;
          color: #334155;
          line-height: 1.82;
          font-weight: 400;
        }

        .doc-summary-body {
          font-size: 0.975rem;
          color: #475569;
          line-height: 1.8;
        }

        .doc-summary-body--spaced {
          margin-top: 0.15rem;
        }

        /* CTA row */
        .doc-cta-row {
          display: flex;
          align-items: center;
          gap: 1rem;
          flex-wrap: wrap;
          margin-top: 1rem;
        }

        .doc-btn {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          font-size: 0.9rem;
          font-weight: 600;
          padding: 0.65rem 1.35rem;
          border-radius: 5px;
          cursor: pointer;
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
          border: 1px solid transparent;
          text-decoration: none;
          white-space: nowrap;
        }

        .doc-btn-primary {
          background: #7c152a;
          color: #ffffff;
          box-shadow: 0 1px 3px rgba(124, 21, 42, 0.22);
        }

        .doc-btn-primary:hover {
          background: #5c0d1c;
          color: #ffffff;
          box-shadow: 0 4px 12px rgba(124, 21, 42, 0.28);
          transform: translateY(-1px);
        }

        .doc-btn-ghost {
          background: #ffffff;
          color: #1e293b;
          border-color: #d4cfc9;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        }

        .doc-btn-ghost:hover {
          background: #f8f5f2;
          border-color: #b0a99f;
          color: #0f172a;
          transform: translateY(-1px);
        }

        .doc-btn-ext {
          opacity: 0.6;
        }

        /* ── Sections ── */
        .doc-section {
          padding: 4rem 0;
          background: #ffffff;
          border-bottom: 1px solid #ede9e3;
        }

        .doc-section--alt {
          background: #faf9f7;
        }

        .doc-section--last {
          border-bottom: none;
        }

        .doc-sec-header {
          margin-bottom: 2.5rem;
          max-width: 900px;
        }

        .doc-sec-eyebrow {
          display: block;
          font-size: 0.75rem;
          font-weight: 700;
          color: #7c152a;
          text-transform: uppercase;
          letter-spacing: 0.09em;
          margin-bottom: 0.45rem;
        }

        .doc-sec-title {
          font-size: 1.65rem;
          font-weight: 800;
          color: #0f172a;
          letter-spacing: -0.03em;
          line-height: 1.2;
          margin-bottom: 0.85rem;
        }

        .doc-sec-intro {
          font-size: 0.975rem;
          color: #475569;
          line-height: 1.8;
        }

        .doc-sec-intro + .doc-sec-intro {
          margin-top: 0.85rem;
        }

        /* ── Architecture figure ── */
        .doc-figure {
          margin: 0;
        }

        .doc-figure-frame {
          background: #ffffff;
          border: 1px solid #e8e3dd;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
          display: flex;
          justify-content: center;
          overflow: auto;
        }

        .doc-figure-frame img {
          max-width: 100%;
          height: auto;
          object-fit: contain;
        }

        .doc-figure-caption {
          margin-top: 0.75rem;
          font-size: 0.83rem;
          color: #64748b;
          line-height: 1.6;
          max-width: 820px;
        }

        /* ── Specification tables ── */
        .doc-spec-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.75rem;
          margin-bottom: 2.5rem;
        }

        .doc-spec-card {
          background: #ffffff;
          border: 1px solid #e8e3dd;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .doc-spec-card:hover {
          border-color: #f4cdd4;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
        }

        .doc-spec-head {
          display: flex;
          align-items: center;
          gap: 0.6rem;
          padding-bottom: 0.9rem;
          margin-bottom: 0.4rem;
          border-bottom: 1px solid #ede9e3;
          flex-wrap: wrap;
        }

        .doc-spec-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 30px;
          height: 30px;
          border-radius: 6px;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          color: #7c152a;
          flex-shrink: 0;
        }

        .doc-spec-title {
          font-size: 1rem;
          font-weight: 700;
          color: #0f172a;
          letter-spacing: -0.02em;
          margin-right: auto;
        }

        .doc-spec-list {
          display: flex;
          flex-direction: column;
        }

        .doc-spec-row {
          display: grid;
          grid-template-columns: 165px 1fr;
          gap: 1rem;
          padding: 0.65rem 0;
          border-bottom: 1px solid #f3eeea;
          align-items: baseline;
        }

        .doc-spec-row:last-child {
          border-bottom: none;
        }

        .doc-spec-label {
          font-size: 0.78rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: #94a3b8;
        }

        .doc-spec-value {
          font-family: var(--font-mono);
          font-size: 0.8rem;
          color: #334155;
          line-height: 1.6;
          word-break: break-word;
        }

        .doc-prose {
          max-width: 900px;
        }

        .doc-prose-text {
          font-size: 0.935rem;
          color: #475569;
          line-height: 1.75;
        }

        .doc-prose-text + .doc-prose-text {
          margin-top: 0.85rem;
        }

        /* ── Datasets ── */
        .doc-dataset-group {
          margin-bottom: 2.5rem;
        }

        .doc-dataset-group-head {
          display: flex;
          align-items: center;
          gap: 0.55rem;
          margin-bottom: 1.1rem;
          padding-bottom: 0.7rem;
          border-bottom: 1px solid #ede9e3;
        }

        .doc-dataset-group-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          border-radius: 6px;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          color: #7c152a;
          flex-shrink: 0;
        }

        .doc-dataset-group-title {
          font-size: 0.95rem;
          font-weight: 700;
          color: #0f172a;
          letter-spacing: -0.01em;
        }

        .doc-dataset-grid {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 1.5rem;
        }

        .doc-dataset-card {
          background: #ffffff;
          border: 1px solid #e8e3dd;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
          transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .doc-dataset-card:hover {
          border-color: #f4cdd4;
          box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07);
          transform: translateY(-2px);
        }

        .doc-dataset-head {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 0.6rem;
          margin-bottom: 0.9rem;
        }

        .doc-dataset-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 30px;
          height: 30px;
          border-radius: 6px;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          color: #7c152a;
          flex-shrink: 0;
        }

        .doc-dataset-tag {
          font-size: 0.72rem;
          font-weight: 600;
          color: #7c152a;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          padding: 0.15rem 0.5rem;
          border-radius: 3px;
          letter-spacing: 0.03em;
        }

        .doc-dataset-name {
          font-size: 1rem;
          font-weight: 700;
          color: #0f172a;
          letter-spacing: -0.02em;
          margin-bottom: 0.55rem;
        }

        .doc-dataset-text {
          font-size: 0.885rem;
          color: #475569;
          line-height: 1.7;
        }

        .doc-closing-note {
          margin-top: 0.5rem;
          font-size: 0.875rem;
          color: #64748b;
          font-style: italic;
        }

        /* ── Methodology ── */
        .doc-method-list {
          list-style: none;
          display: flex;
          flex-direction: column;
        }

        .doc-method-item {
          display: flex;
          align-items: flex-start;
          gap: 1.75rem;
          padding: 1.6rem 0;
          border-bottom: 1px solid #ede9e3;
        }

        .doc-method-item:first-child {
          padding-top: 0;
        }

        .doc-method-item:last-child {
          border-bottom: none;
          padding-bottom: 0;
        }

        .doc-method-num {
          font-family: var(--font-mono);
          font-size: 0.8rem;
          font-weight: 700;
          color: #d4cfc9;
          letter-spacing: 0.04em;
          min-width: 28px;
          padding-top: 0.1rem;
          flex-shrink: 0;
        }

        .doc-method-body {
          flex: 1;
        }

        .doc-method-title-row {
          display: flex;
          align-items: baseline;
          gap: 0.85rem;
          margin-bottom: 0.6rem;
          flex-wrap: wrap;
        }

        .doc-method-title {
          font-size: 1.05rem;
          font-weight: 700;
          color: #0f172a;
          line-height: 1.3;
          letter-spacing: -0.02em;
        }

        .doc-method-tag {
          font-size: 0.73rem;
          font-weight: 600;
          color: #7c152a;
          background: #fdf2f4;
          border: 1px solid #f4cdd4;
          padding: 0.15rem 0.5rem;
          border-radius: 3px;
          letter-spacing: 0.03em;
          flex-shrink: 0;
        }

        .doc-method-text {
          font-size: 0.935rem;
          color: #475569;
          line-height: 1.75;
          max-width: 860px;
        }

        .doc-method-text + .doc-method-text {
          margin-top: 0.7rem;
        }

        /* ── References ── */
        .doc-ref-list {
          list-style: none;
          display: flex;
          flex-direction: column;
          max-width: 900px;
        }

        .doc-ref-item {
          display: flex;
          align-items: flex-start;
          gap: 1.25rem;
          padding: 1rem 0;
          border-bottom: 1px solid #ede9e3;
        }

        .doc-ref-item:first-child {
          padding-top: 0;
        }

        .doc-ref-item:last-child {
          border-bottom: none;
          padding-bottom: 0;
        }

        .doc-ref-num {
          font-family: var(--font-mono);
          font-size: 0.78rem;
          font-weight: 700;
          color: #d4cfc9;
          letter-spacing: 0.04em;
          min-width: 26px;
          padding-top: 0.15rem;
          flex-shrink: 0;
        }

        .doc-ref-text {
          font-size: 0.925rem;
          color: #334155;
          line-height: 1.7;
        }

        /* ── Responsive ── */
        @media (max-width: 1060px) {
          .doc-title {
            font-size: 1.9rem;
            max-width: 100%;
          }
        }

        @media (max-width: 860px) {
          .doc-summary-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
          }

          .doc-summary-col-lead {
            border-bottom: 1px solid #e8e3dd;
            padding-bottom: 1rem;
          }

          .doc-spec-grid {
            grid-template-columns: 1fr;
          }

          .doc-dataset-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 640px) {
          .doc-hero {
            padding: 2.5rem 0 2rem;
          }

          .doc-title {
            font-size: 1.55rem;
          }

          .doc-summary-lead,
          .doc-summary-body {
            font-size: 0.95rem;
          }

          .doc-section {
            padding: 2.5rem 0;
          }

          .doc-sec-title {
            font-size: 1.35rem;
          }

          .doc-method-item {
            gap: 1rem;
          }

          .doc-method-num {
            min-width: 22px;
          }

          .doc-spec-row {
            grid-template-columns: 1fr;
            gap: 0.25rem;
          }

          .doc-figure-frame {
            padding: 0.85rem;
          }
        }
      `}</style>
    </div>
  );
}
