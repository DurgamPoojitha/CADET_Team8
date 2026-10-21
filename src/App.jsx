import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Overview from './pages/Overview';
import Documentation from './pages/Documentation';
import UnimplementedNotice from './components/UnimplementedNotice';

/**
 * Application shell for the CADET documentation portal.
 * HashRouter is used to protect routes on GitHub Pages.
 * Page 1 renders the project overview.
 * Page 2 renders the technical documentation.
 * Page 3 renders a placeholder notice for progress.
 * UnimplementedNotice covers routes pending implementation.
 */
export default function App() {
  return (
    <HashRouter>
      <div className="app-root">
        <Navbar />
        <main className="main-content">
          <Routes>
            {/* Page 1: Project Overview (Fully Implemented) */}
            <Route path="/" element={<Overview />} />
            <Route path="/overview" element={<Navigate to="/" replace />} />

            {/* Page 2: Technical documentation (implemented). */}
            <Route path="/documentation" element={<Documentation />} />

            {/* Page 3 renders a placeholder notice for progress. */}
            <Route
              path="/progress"
              element={
                <UnimplementedNotice
                  title="Project Progress & Roadmap"
                  pageName="Progress"
                />
              }
            />

            {/* Catch-all redirect to Overview */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>

      <style>{`
        .app-root {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        .main-content {
          flex: 1 0 auto;
        }
      `}</style>
    </HashRouter>
  );
}
