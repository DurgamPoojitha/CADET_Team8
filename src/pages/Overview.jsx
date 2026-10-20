import React from 'react';
import { Github, ExternalLink, GraduationCap, Users } from 'lucide-react';
import { projectConfig } from '../config/projectConfig';

/* ─────────────────────────────────────────────────────────────
   Objectives — editorial numbered list
────────────────────────────────────────────────────────────── */
const OBJECTIVES = [
  {
    num: '01',
    title: 'Bimodal Detection',
    body: 'XceptionNet for spatial artifact localisation in images; EfficientNet-B1 paired with a 2-layer LSTM for spatiotemporal anomaly detection across 16-frame video sequences.',
    tag: 'Image · Video'
  },
  {
    num: '02',
    title: 'Compression-Aware Preprocessing',
    body: 'Dynamic simulation of social-media lossy degradation—area downscaling, Gaussian blur, and JPEG re-encoding at quality 10–25—applied to 70% of training data to harden model representations.',
    tag: 'Data Pipeline'
  },
  {
    num: '03',
    title: 'Adversarial Robustness via FGSM',
    body: 'Fast Gradient Sign Method adversarial sample generation during training to defend against imperceptible evasion perturbations and malicious noise manipulation.',
    tag: 'Robust ML'
  },
  {
    num: '04',
    title: 'Cross-Dataset Generalisation',
    body: 'Open-set evaluation across CelebDF, 140K Faces, and FaceForensics++ with balanced per-class sampling to verify detection of unseen generation techniques.',
    tag: 'Evaluation'
  },
  {
    num: '05',
    title: 'Visual Explainability via Grad-CAM',
    body: 'Gradient-weighted Class Activation Maps on pre-final convolutional layers expose the exact manipulated facial landmarks—eyes, mouth, and seam boundaries—for transparent forensic inspection.',
    tag: 'XAI'
  }
];

/* ─────────────────────────────────────────────────────────────
   Main Component
────────────────────────────────────────────────────────────── */
export default function Overview() {
  return (
    <div className="ov-root">

      {/* ══════════════════════════════════════════
          HERO — full-width editorial layout
      ══════════════════════════════════════════ */}
      <section className="ov-hero">
        <div className="container ov-hero-inner">

          {/* Meta strip */}
          <div className="ov-meta-strip">
            <span className="ov-meta-tag">Amrita Vishwa Vidyapeetham</span>
            <span className="ov-meta-sep">·</span>
            <span className="ov-meta-tag">Team 08</span>
            <span className="ov-meta-sep">·</span>
            <span className="ov-meta-tag">Research-Based Project</span>
            <span className="ov-meta-sep">·</span>
            <span className="ov-status-dot-wrap">
              <span className="ov-status-dot" />
              <span className="ov-meta-tag ov-status-text">Phase 2 Completed</span>
            </span>
          </div>

          {/* Title */}
          <h1 className="ov-title">{projectConfig.title}</h1>

          {/* Acronym line */}
          <div className="ov-acronym-line">
            <span className="ov-acronym-badge">{projectConfig.acronym}</span>
            <span className="ov-acronym-sep">—</span>
            <span className="ov-acronym-expansion">{projectConfig.acronymFull}</span>
          </div>

          {/* Improved summary — two-column editorial layout on wider screens */}
          <div className="ov-summary-grid">
            <div className="ov-summary-col ov-summary-col-lead">
              <p className="ov-summary-lead">
                The proliferation of AI-generated synthetic media — commonly known as deepfakes —
                has created a serious and growing threat to digital trust. Generative models can
                now produce hyper-realistic face-swapped images and videos that are virtually
                indistinguishable from genuine recordings, even to trained human observers.
                The problem is significantly amplified in real-world conditions: when media is
                shared across social platforms, it passes through aggressive lossy compression
                pipelines — JPEG re-encoding, resolution downscaling, and transmission artefacts —
                that degrade the subtle forensic traces that most detectors rely on.
                The result is that conventional deepfake detectors, trained on clean
                high-resolution data, fail badly the moment they encounter compressed media
                from the wild.
              </p>
            </div>

            <div className="ov-summary-col ov-summary-col-body">
              <p className="ov-summary-body">
                CADET is a bimodal forensic detection framework built specifically to address these
                two compounding challenges. On the image side, a fine-tuned{' '}
                <strong>XceptionNet</strong> backbone — with depthwise-separable convolutions
                and discriminative learning rates — is trained to detect localised spatial
                inconsistencies introduced by face-synthesis and face-swap algorithms. On the
                video side, an <strong>EfficientNet-B1</strong> spatial feature extractor is
                coupled with a 2-layer unidirectional <strong>LSTM</strong> to model temporal
                patterns across 16-frame sequences, catching the subtle frame-to-frame anomalies
                that single-frame models cannot see.
              </p>
              <p className="ov-summary-body ov-summary-body--spaced">
                Both pipelines are hardened during training through a custom{' '}
                <strong>Compression-Based Preprocessing (CBP)</strong> stage that simulates
                real-world social-media degradation — dynamic bilinear rescaling, Gaussian
                blurring, and low-quality JPEG re-encoding at quality factors between 10 and 25 —
                applied to 70% of training samples. Additionally, <strong>Fast Gradient Sign
                Method (FGSM)</strong> adversarial training is incorporated to defend against
                deliberate evasion attacks. To ensure the detectors do not overfit to a single
                dataset's characteristics, the system is evaluated across multiple independent
                benchmarks — CelebDF, 140K Faces, and FaceForensics++ — using balanced
                per-class sampling. Finally, <strong>Grad-CAM</strong> heatmaps are generated
                across the pre-final convolutional layers to visually highlight the exact facial
                regions driving each prediction, making the system's reasoning transparent and
                auditable rather than a black box.
              </p>
            </div>
          </div>

          {/* CTA row */}
          <div className="ov-cta-row">
            <a
              href={projectConfig.urls.github}
              target="_blank"
              rel="noopener noreferrer"
              className="ov-btn ov-btn-primary"
            >
              <Github size={16} />
              <span>GitHub Repository</span>
              <ExternalLink size={13} className="ov-btn-ext" />
            </a>
            <a
              href={projectConfig.urls.liveDemo}
              target={projectConfig.urls.isLiveDemoPlaceholder ? '_self' : '_blank'}
              rel="noopener noreferrer"
              className="ov-btn ov-btn-ghost"
            >
              <ExternalLink size={16} />
              <span>Live Demo</span>
              {projectConfig.urls.isLiveDemoPlaceholder && (
                <span className="ov-placeholder-tag">Placeholder</span>
              )}
            </a>
          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════
          OBJECTIVES — editorial numbered list
      ══════════════════════════════════════════ */}
      <section className="ov-objectives">
        <div className="container">
          <div className="ov-sec-header">
            <span className="ov-sec-eyebrow">Key Objectives · Project Phase 2</span>
            <h2 className="ov-sec-title">Research Objectives</h2>
          </div>

          <ol className="ov-obj-list">
            {OBJECTIVES.map((obj) => (
              <li key={obj.num} className="ov-obj-item">
                <span className="ov-obj-num" aria-hidden="true">{obj.num}</span>
                <div className="ov-obj-body">
                  <div className="ov-obj-head-row">
                    <h3 className="ov-obj-title">{obj.title}</h3>
                    <span className="ov-obj-tag">{obj.tag}</span>
                  </div>
                  <p className="ov-obj-text">{obj.body}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          TEAM — academic credits strip
      ══════════════════════════════════════════ */}
      <section className="ov-team">
        <div className="container ov-team-inner">

          {/* Institution + guide */}
          <div className="ov-team-left">
            <div className="ov-team-inst-row">
              <GraduationCap size={16} className="ov-team-inst-icon" />
              <span className="ov-team-inst">{projectConfig.academic.institution}</span>
            </div>
            <p className="ov-team-dept">
              {projectConfig.academic.department}&nbsp;·&nbsp;
              {projectConfig.academic.school}
            </p>
            <p className="ov-team-campus">{projectConfig.academic.campus}</p>

            <div className="ov-guide-block">
              <span className="ov-guide-role">Project Guide</span>
              <span className="ov-guide-name">{projectConfig.academic.guide.name}</span>
              <span className="ov-guide-desig">
                {projectConfig.academic.guide.designation}
              </span>
            </div>
          </div>

          {/* Team members */}
          <div className="ov-team-right">
            <div className="ov-members-head">
              <Users size={14} />
              <span>Team 08 · Members</span>
            </div>
            <ul className="ov-members-list">
              {projectConfig.academic.students.map((s, i) => (
                <li key={i} className="ov-member-row">
                  <span className="ov-member-idx">{String(i + 1).padStart(2, '0')}</span>
                  <span className="ov-member-name">{s.name}</span>
                  <span className="ov-member-reg">{s.regNo}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>
      </section>

      {/* ══════════════════════════════════════════
          SCOPED STYLES
      ══════════════════════════════════════════ */}
      <style>{`
        /* ── Root ── */
        .ov-root {
          display: flex;
          flex-direction: column;
          width: 100%;
        }

        /* ─────────────────────────────────────
           HERO — full-width
        ───────────────────────────────────── */
        .ov-hero {
          background-color: #faf9f7;
          border-bottom: 1px solid #e8e3dd;
          padding: 3.5rem 0 3.25rem;
        }

        .ov-hero-inner {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
        }

        /* Meta strip */
        .ov-meta-strip {
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 0.35rem;
          margin-bottom: 1.4rem;
        }

        .ov-meta-tag {
          font-size: 0.78rem;
          font-weight: 500;
          color: #64748b;
          letter-spacing: 0.01em;
        }

        .ov-meta-sep {
          color: #cbd5e1;
          font-size: 0.78rem;
        }

        .ov-status-dot-wrap {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
        }

        .ov-status-dot {
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: #22c55e;
          flex-shrink: 0;
        }

        .ov-status-text {
          color: #166534;
          font-weight: 600;
        }

        /* Title */
        .ov-title {
          font-size: 2.25rem;
          font-weight: 800;
          color: #0f172a;
          line-height: 1.18;
          letter-spacing: -0.035em;
          margin-bottom: 1rem;
          max-width: 860px;
        }

        /* Acronym */
        .ov-acronym-line {
          display: flex;
          align-items: baseline;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-bottom: 2rem;
        }

        .ov-acronym-badge {
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

        .ov-acronym-sep {
          color: #94a3b8;
          font-size: 0.88rem;
        }

        .ov-acronym-expansion {
          font-size: 0.88rem;
          color: #334155;
          font-weight: 500;
        }

        /* Summary — two-column editorial grid */
        .ov-summary-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2.5rem;
          margin-bottom: 2.25rem;
          max-width: 1100px;
          align-items: start;
        }

        .ov-summary-col {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .ov-summary-lead {
          font-size: 1.025rem;
          color: #334155;
          line-height: 1.82;
          font-weight: 400;
        }

        .ov-summary-body {
          font-size: 0.975rem;
          color: #475569;
          line-height: 1.8;
        }

        .ov-summary-body--spaced {
          margin-top: 0.85rem;
        }

        .ov-summary-body strong {
          color: #1e293b;
          font-weight: 650;
        }

        /* Divider between cols on narrow screens */
        @media (max-width: 860px) {
          .ov-summary-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
          }

          .ov-summary-col-lead {
            border-bottom: 1px solid #e8e3dd;
            padding-bottom: 1rem;
          }
        }

        /* CTA row */
        .ov-cta-row {
          display: flex;
          align-items: center;
          gap: 1rem;
          flex-wrap: wrap;
        }

        .ov-btn {
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

        .ov-btn-primary {
          background: #7c152a;
          color: #ffffff;
          box-shadow: 0 1px 3px rgba(124, 21, 42, 0.22);
        }

        .ov-btn-primary:hover {
          background: #5c0d1c;
          color: #ffffff;
          box-shadow: 0 4px 12px rgba(124, 21, 42, 0.28);
          transform: translateY(-1px);
        }

        .ov-btn-ghost {
          background: #ffffff;
          color: #1e293b;
          border-color: #d4cfc9;
          box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }

        .ov-btn-ghost:hover {
          background: #f8f5f2;
          border-color: #b0a99f;
          color: #0f172a;
          transform: translateY(-1px);
        }

        .ov-btn-ext {
          opacity: 0.6;
        }

        .ov-placeholder-tag {
          font-size: 0.65rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: #94a3b8;
          background: #f1f5f9;
          border: 1px solid #e2e8f0;
          padding: 0.1rem 0.35rem;
          border-radius: 3px;
        }

        /* ─────────────────────────────────────
           OBJECTIVES
        ───────────────────────────────────── */
        .ov-objectives {
          padding: 4rem 0;
          background: #ffffff;
          border-bottom: 1px solid #ede9e3;
        }

        .ov-sec-header {
          margin-bottom: 2.5rem;
        }

        .ov-sec-eyebrow {
          display: block;
          font-size: 0.75rem;
          font-weight: 700;
          color: #7c152a;
          text-transform: uppercase;
          letter-spacing: 0.09em;
          margin-bottom: 0.45rem;
        }

        .ov-sec-title {
          font-size: 1.65rem;
          font-weight: 800;
          color: #0f172a;
          letter-spacing: -0.03em;
          line-height: 1.2;
        }

        /* Objectives list */
        .ov-obj-list {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 0;
        }

        .ov-obj-item {
          display: flex;
          align-items: flex-start;
          gap: 1.75rem;
          padding: 1.5rem 0;
          border-bottom: 1px solid #ede9e3;
          transition: background 0.15s ease;
        }

        .ov-obj-item:last-child {
          border-bottom: none;
        }

        .ov-obj-item:hover {
          background: #faf9f7;
          margin-left: -1.5rem;
          margin-right: -1.5rem;
          padding-left: 1.5rem;
          padding-right: 1.5rem;
        }

        .ov-obj-num {
          font-family: var(--font-mono);
          font-size: 0.8rem;
          font-weight: 700;
          color: #d4cfc9;
          letter-spacing: 0.04em;
          min-width: 28px;
          padding-top: 0.1rem;
          flex-shrink: 0;
        }

        .ov-obj-body {
          flex: 1;
        }

        .ov-obj-head-row {
          display: flex;
          align-items: baseline;
          gap: 0.85rem;
          margin-bottom: 0.5rem;
          flex-wrap: wrap;
        }

        .ov-obj-title {
          font-size: 1.05rem;
          font-weight: 700;
          color: #0f172a;
          line-height: 1.3;
          letter-spacing: -0.02em;
        }

        .ov-obj-tag {
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

        .ov-obj-text {
          font-size: 0.935rem;
          color: #475569;
          line-height: 1.7;
          max-width: 820px;
        }

        /* ─────────────────────────────────────
           TEAM
        ───────────────────────────────────── */
        .ov-team {
          padding: 3rem 0;
          background: #faf9f7;
          border-top: 1px solid #ede9e3;
        }

        .ov-team-inner {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 3rem;
          align-items: start;
        }

        .ov-team-left {
          display: flex;
          flex-direction: column;
          gap: 0.3rem;
        }

        .ov-team-inst-row {
          display: flex;
          align-items: center;
          gap: 0.45rem;
          margin-bottom: 0.15rem;
        }

        .ov-team-inst-icon {
          color: #7c152a;
          flex-shrink: 0;
        }

        .ov-team-inst {
          font-size: 1rem;
          font-weight: 700;
          color: #0f172a;
        }

        .ov-team-dept {
          font-size: 0.85rem;
          color: #475569;
          line-height: 1.5;
        }

        .ov-team-campus {
          font-size: 0.82rem;
          color: #64748b;
          margin-bottom: 1.25rem;
        }

        .ov-guide-block {
          display: flex;
          flex-direction: column;
          gap: 0.18rem;
          padding-top: 1rem;
          border-top: 1px solid #ede9e3;
        }

        .ov-guide-role {
          font-size: 0.72rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: #7c152a;
        }

        .ov-guide-name {
          font-size: 0.975rem;
          font-weight: 700;
          color: #0f172a;
        }

        .ov-guide-desig {
          font-size: 0.82rem;
          color: #64748b;
        }

        /* Members */
        .ov-team-right {
          display: flex;
          flex-direction: column;
        }

        .ov-members-head {
          display: flex;
          align-items: center;
          gap: 0.45rem;
          font-size: 0.78rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.07em;
          color: #94a3b8;
          margin-bottom: 0.9rem;
          padding-bottom: 0.7rem;
          border-bottom: 1px solid #ede9e3;
        }

        .ov-members-list {
          list-style: none;
          display: flex;
          flex-direction: column;
        }

        .ov-member-row {
          display: grid;
          grid-template-columns: 28px 1fr auto;
          align-items: center;
          gap: 0.85rem;
          padding: 0.7rem 0;
          border-bottom: 1px solid #f3eeea;
        }

        .ov-member-row:last-child {
          border-bottom: none;
        }

        .ov-member-idx {
          font-family: var(--font-mono);
          font-size: 0.75rem;
          color: #cbd5e1;
          font-weight: 600;
        }

        .ov-member-name {
          font-size: 0.9rem;
          font-weight: 600;
          color: #1e293b;
        }

        .ov-member-reg {
          font-family: var(--font-mono);
          font-size: 0.75rem;
          color: #94a3b8;
          text-align: right;
        }

        /* ─────────────────────────────────────
           RESPONSIVE
        ───────────────────────────────────── */
        @media (max-width: 1060px) {
          .ov-title {
            font-size: 1.9rem;
            max-width: 100%;
          }

          .ov-team-inner {
            grid-template-columns: 1fr;
            gap: 2rem;
          }
        }

        @media (max-width: 640px) {
          .ov-hero {
            padding: 2.5rem 0 2rem;
          }

          .ov-title {
            font-size: 1.55rem;
          }

          .ov-summary-lead,
          .ov-summary-body {
            font-size: 0.95rem;
          }

          .ov-objectives {
            padding: 2.5rem 0;
          }

          .ov-obj-item {
            gap: 1rem;
          }

          .ov-obj-num {
            min-width: 22px;
          }

          .ov-member-row {
            grid-template-columns: 24px 1fr;
            gap: 0.6rem;
          }

          .ov-member-reg {
            display: none;
          }

          .ov-team {
            padding: 2rem 0;
          }
        }
      `}</style>
    </div>
  );
}
