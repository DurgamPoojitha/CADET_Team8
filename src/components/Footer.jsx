import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Github, ExternalLink, GraduationCap, Award } from 'lucide-react';
import { projectConfig } from '../config/projectConfig';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer-wrapper">
      <div className="container footer-container">
        <div className="footer-top">
          {/* Project Info Column */}
          <div className="footer-col footer-col-primary">
            <div className="footer-brand">
              <div className="footer-brand-icon">
                <ShieldCheck size={20} />
              </div>
              <span className="footer-brand-name">{projectConfig.acronym}</span>
            </div>
            <p className="footer-title">{projectConfig.title}</p>
            <p className="footer-description">
              An academic research initiative investigating compression-aware, explainable deepfake detection across image and video modalities.
            </p>
            <div className="footer-status-pill">
              <span className="status-dot"></span>
              <span>{projectConfig.status.state} (100% Completed)</span>
            </div>
          </div>

          {/* Academic Context Column */}
          <div className="footer-col">
            <h4 className="footer-heading">
              <GraduationCap size={16} />
              <span>Academic Context</span>
            </h4>
            <ul className="footer-list">
              <li>{projectConfig.academic.school}</li>
              <li>{projectConfig.academic.department}</li>
              <li>{projectConfig.academic.institution}</li>
              <li>{projectConfig.academic.campus}</li>
              <li className="text-highlight">
                {projectConfig.academic.phase} &bull; Team Number: {projectConfig.academic.teamNumber}
              </li>
            </ul>
          </div>

          {/* Quick Links Column */}
          <div className="footer-col">
            <h4 className="footer-heading">
              <Award size={16} />
              <span>Project Portal</span>
            </h4>
            <ul className="footer-links">
              <li>
                <Link to="/">Project Overview</Link>
              </li>
              <li>
                <Link to="/documentation">Documentation</Link>
              </li>
              <li>
                <Link to="/progress">Project Progress (Planned)</Link>
              </li>
              <li>
                <a
                  href={projectConfig.urls.github}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="footer-ext-link"
                >
                  <Github size={14} />
                  <span>GitHub Repository</span>
                  <ExternalLink size={11} />
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom / Copyright */}
        <div className="footer-bottom">
          <div className="footer-copy">
            &copy; {currentYear} {projectConfig.acronym} Research Team &bull; {projectConfig.academic.institution}. Academic Documentation Portal.
          </div>
          <div className="footer-note">
            {projectConfig.academic.phase} &bull; Team Number: {projectConfig.academic.teamNumber} &bull; Guide: {projectConfig.academic.guide.name}
          </div>
        </div>
      </div>

      <style>{`
        .footer-wrapper {
          background-color: var(--color-navy);
          color: #94a3b8;
          border-top: 1px solid rgba(255, 255, 255, 0.08);
          margin-top: auto;
          padding-top: 4rem;
          padding-bottom: 2.5rem;
          font-size: 0.9rem;
        }

        .footer-container {
          display: flex;
          flex-direction: column;
          gap: 3rem;
        }

        .footer-top {
          display: grid;
          grid-template-columns: 2fr 1.2fr 1fr;
          gap: 3rem;
        }

        .footer-brand {
          display: flex;
          align-items: center;
          gap: 0.6rem;
          margin-bottom: 0.85rem;
        }

        .footer-brand-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border-radius: var(--radius-sm);
          background: rgba(124, 21, 42, 0.4);
          color: #fca5a5;
          border: 1px solid rgba(244, 205, 212, 0.2);
        }

        .footer-brand-name {
          font-size: 1.15rem;
          font-weight: 800;
          color: #ffffff;
          letter-spacing: -0.01em;
        }

        .footer-title {
          font-size: 0.95rem;
          font-weight: 600;
          color: #f1f5f9;
          line-height: 1.45;
          margin-bottom: 0.75rem;
          max-width: 460px;
        }

        .footer-description {
          font-size: 0.85rem;
          color: #94a3b8;
          line-height: 1.6;
          margin-bottom: 1.2rem;
          max-width: 480px;
        }

        .footer-status-pill {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: var(--radius-full);
          padding: 0.3rem 0.75rem;
          font-size: 0.75rem;
          color: #e2e8f0;
        }

        .status-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #34d399;
        }

        .footer-heading {
          font-size: 0.95rem;
          font-weight: 700;
          color: #ffffff;
          margin-bottom: 1.25rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .footer-list {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 0.55rem;
          font-size: 0.85rem;
        }

        .footer-list .text-highlight {
          color: #cbd5e1;
          font-weight: 600;
          margin-top: 0.25rem;
        }

        .footer-links {
          list-style: none;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }

        .footer-links a {
          color: #94a3b8;
          transition: var(--transition-default);
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
        }

        .footer-links a:hover {
          color: #ffffff;
          transform: translateX(2px);
        }

        .footer-ext-link {
          gap: 0.4rem;
        }

        .footer-bottom {
          border-top: 1px solid rgba(255, 255, 255, 0.08);
          padding-top: 1.5rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 1rem;
          font-size: 0.8rem;
          color: #64748b;
        }

        .footer-copy {
          color: #94a3b8;
        }

        @media (max-width: 900px) {
          .footer-top {
            grid-template-columns: 1fr;
            gap: 2rem;
          }
          .footer-bottom {
            flex-direction: column;
            align-items: flex-start;
          }
        }
      `}</style>
    </footer>
  );
}
