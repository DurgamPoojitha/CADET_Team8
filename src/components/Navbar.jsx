import React, { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { ShieldCheck, Github, Menu, X, ExternalLink } from 'lucide-react';
import { projectConfig } from '../config/projectConfig';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <header className="navbar-wrapper">
      <div className="container navbar-container">
        {/* Brand Branding */}
        <Link to="/" className="navbar-brand" onClick={closeMobileMenu}>
          <div className="brand-icon-box">
            <ShieldCheck size={22} className="brand-icon" />
          </div>
          <div className="brand-text">
            <div className="brand-title">
              {projectConfig.acronym}
              <span className="brand-badge">Research</span>
            </div>
            <div className="brand-subtitle">Explainable Bimodal Deepfake Detection</div>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="desktop-nav" aria-label="Main Navigation">
          <NavLink
            to="/"
            end
            className={({ isActive }) =>
              isActive ? 'nav-link active' : 'nav-link'
            }
          >
            Overview
          </NavLink>
          <NavLink
            to="/documentation"
            className={({ isActive }) =>
              isActive ? 'nav-link active' : 'nav-link'
            }
          >
            Documentation
          </NavLink>
          <NavLink
            to="/progress"
            className={({ isActive }) =>
              isActive ? 'nav-link active' : 'nav-link'
            }
          >
            Project Progress
            <span className="nav-tag">Planned</span>
          </NavLink>
        </nav>

        {/* Right CTA */}
        <div className="navbar-actions">
          <a
            href={projectConfig.urls.github}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary btn-sm nav-github-btn"
            title="View CADET on GitHub"
          >
            <Github size={16} />
            <span>Repository</span>
            <ExternalLink size={12} className="external-icon" />
          </a>

          {/* Mobile Menu Toggle Button */}
          <button
            type="button"
            className="mobile-menu-btn"
            onClick={toggleMobileMenu}
            aria-expanded={mobileMenuOpen}
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="mobile-drawer">
          <nav className="mobile-nav" aria-label="Mobile Navigation">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                isActive ? 'mobile-nav-link active' : 'mobile-nav-link'
              }
              onClick={closeMobileMenu}
            >
              Overview
            </NavLink>
            <NavLink
              to="/documentation"
              className={({ isActive }) =>
                isActive ? 'mobile-nav-link active' : 'mobile-nav-link'
              }
              onClick={closeMobileMenu}
            >
              Documentation
            </NavLink>
            <NavLink
              to="/progress"
              className={({ isActive }) =>
                isActive ? 'mobile-nav-link active' : 'mobile-nav-link'
              }
              onClick={closeMobileMenu}
            >
              Project Progress
              <span className="nav-tag">Planned</span>
            </NavLink>
            <div className="mobile-actions">
              <a
                href={projectConfig.urls.github}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary btn-sm w-full"
                onClick={closeMobileMenu}
              >
                <Github size={16} />
                <span>GitHub Repository</span>
                <ExternalLink size={12} />
              </a>
            </div>
          </nav>
        </div>
      )}

      <style>{`
        .navbar-wrapper {
          position: sticky;
          top: 0;
          z-index: 100;
          background: rgba(255, 255, 255, 0.95);
          backdrop-filter: blur(10px);
          border-bottom: 1px solid var(--color-border);
        }

        .navbar-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 72px;
        }

        .navbar-brand {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          color: var(--color-navy);
        }

        .brand-icon-box {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: var(--color-primary-subtle);
          border: 1px solid var(--color-primary-border);
          border-radius: var(--radius-sm);
          color: var(--color-primary);
        }

        .brand-text {
          display: flex;
          flex-direction: column;
        }

        .brand-title {
          font-size: 1.15rem;
          font-weight: 800;
          letter-spacing: -0.01em;
          color: var(--color-navy);
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .brand-badge {
          font-size: 0.65rem;
          text-transform: uppercase;
          font-weight: 700;
          letter-spacing: 0.05em;
          background: var(--color-primary-subtle);
          color: var(--color-primary);
          padding: 0.15rem 0.45rem;
          border-radius: var(--radius-full);
          border: 1px solid var(--color-primary-border);
        }

        .brand-subtitle {
          font-size: 0.75rem;
          color: var(--color-slate);
          font-weight: 500;
        }

        .desktop-nav {
          display: flex;
          align-items: center;
          gap: 1.75rem;
        }

        .nav-link {
          font-size: 0.925rem;
          font-weight: 600;
          color: var(--color-slate-dark);
          position: relative;
          padding: 0.5rem 0;
          display: inline-flex;
          align-items: center;
          gap: 0.4rem;
        }

        .nav-link:hover {
          color: var(--color-primary);
        }

        .nav-link.active {
          color: var(--color-primary);
        }

        .nav-link.active::after {
          content: '';
          position: absolute;
          bottom: -4px;
          left: 0;
          right: 0;
          height: 2px;
          background: var(--color-primary);
          border-radius: 2px;
        }

        .nav-tag {
          font-size: 0.65rem;
          font-weight: 600;
          color: var(--color-slate);
          background: var(--color-slate-subtle);
          padding: 0.1rem 0.35rem;
          border-radius: var(--radius-sm);
          border: 1px solid var(--color-border);
        }

        .navbar-actions {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .nav-github-btn {
          display: inline-flex;
        }

        .external-icon {
          opacity: 0.6;
        }

        .mobile-menu-btn {
          display: none;
          background: transparent;
          border: none;
          color: var(--color-navy);
          cursor: pointer;
          padding: 0.4rem;
        }

        .mobile-drawer {
          display: none;
          background: #ffffff;
          border-bottom: 1px solid var(--color-border);
          padding: 1rem 1.5rem 1.5rem;
        }

        .mobile-nav {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .mobile-nav-link {
          font-size: 1rem;
          font-weight: 600;
          color: var(--color-navy);
          padding: 0.6rem 0;
          border-bottom: 1px solid var(--color-border-subtle);
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .mobile-nav-link.active {
          color: var(--color-primary);
        }

        .mobile-actions {
          margin-top: 1rem;
        }

        .w-full {
          width: 100%;
        }

        @media (max-width: 860px) {
          .desktop-nav {
            display: none;
          }
          .nav-github-btn {
            display: none;
          }
          .mobile-menu-btn {
            display: flex;
          }
          .mobile-drawer {
            display: block;
          }
        }
      `}</style>
    </header>
  );
}
