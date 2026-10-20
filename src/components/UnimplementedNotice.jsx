import React from 'react';
import { Link } from 'react-router-dom';
import { Construction, ArrowLeft, Clock } from 'lucide-react';

export default function UnimplementedNotice({ title, pageName }) {
  return (
    <div className="unimplemented-wrapper">
      <div className="container">
        <div className="unimplemented-card">
          <div className="icon-badge">
            <Construction size={32} />
          </div>
          <div className="status-pill">
            <Clock size={14} />
            <span>Phase Scope: Page Unimplemented</span>
          </div>
          <h1 className="unimplemented-title">{title}</h1>
          <p className="unimplemented-description">
            In accordance with project portal requirements, <strong>{pageName}.jsx</strong> is strictly preserved as an empty placeholder file in the repository structure.
          </p>
          <div className="info-box">
            <code>src/pages/{pageName}.jsx</code>
            <p>File content: 0 bytes (Empty placeholder reserved for future implementation phase).</p>
          </div>
          <Link to="/" className="btn btn-primary">
            <ArrowLeft size={16} />
            <span>Return to Project Overview</span>
          </Link>
        </div>
      </div>

      <style>{`
        .unimplemented-wrapper {
          min-height: calc(80vh - 72px);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 4rem 1.5rem;
          background: var(--color-bg-base);
        }

        .unimplemented-card {
          max-width: 620px;
          margin: 0 auto;
          background: #ffffff;
          border: 1px solid var(--color-border);
          border-radius: var(--radius-lg);
          padding: 3rem 2.5rem;
          text-align: center;
          box-shadow: var(--shadow-sm);
        }

        .icon-badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 64px;
          height: 64px;
          border-radius: var(--radius-full);
          background: var(--color-primary-subtle);
          color: var(--color-primary);
          margin-bottom: 1.5rem;
        }

        .status-pill {
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
          font-size: 0.8rem;
          font-weight: 600;
          color: var(--color-slate);
          background: var(--color-slate-subtle);
          border: 1px solid var(--color-border);
          padding: 0.3rem 0.8rem;
          border-radius: var(--radius-full);
          margin-bottom: 1.25rem;
        }

        .unimplemented-title {
          font-size: 1.85rem;
          font-weight: 800;
          color: var(--color-navy);
          margin-bottom: 0.85rem;
        }

        .unimplemented-description {
          font-size: 1rem;
          color: var(--color-slate);
          line-height: 1.6;
          margin-bottom: 1.75rem;
        }

        .info-box {
          background: var(--color-slate-subtle);
          border: 1px dashed var(--color-border);
          border-radius: var(--radius-sm);
          padding: 1rem 1.25rem;
          margin-bottom: 2rem;
          font-size: 0.85rem;
          color: var(--color-slate-dark);
        }

        .info-box code {
          display: inline-block;
          font-family: var(--font-mono);
          font-weight: 600;
          color: var(--color-primary);
          margin-bottom: 0.35rem;
        }
      `}</style>
    </div>
  );
}
