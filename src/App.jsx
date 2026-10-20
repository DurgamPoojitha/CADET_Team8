import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Overview from './pages/Overview';
import UnimplementedNotice from './components/UnimplementedNotice';

/**
 * App Component - CADET Documentation Portal
 * 
 * Routing Architecture:
 * - HashRouter is utilized to ensure 100% compatibility with GitHub Pages static hosting,
 *   preventing 404 Not Found errors on page refresh without requiring complex server-side redirects.
 * 
 * Page Implementation Scope:
 * - Page 1 (Overview): Fully implemented and styled in src/pages/Overview.jsx
 * - Page 2 (Documentation): Kept strictly as an empty placeholder file in src/pages/Documentation.jsx
 * - Page 3 (Progress): Kept strictly as an empty placeholder file in src/pages/Progress.jsx
 * - UnimplementedNotice provides a safe, route-compatible placeholder so the app compiles
 *   and executes without modifying the empty files.
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

            {/* Page 2: Documentation (Empty Placeholder preserved) */}
            <Route
              path="/documentation"
              element={
                <UnimplementedNotice
                  title="Technical Documentation"
                  pageName="Documentation"
                />
              }
            />

            {/* Page 3: Project Progress (Empty Placeholder preserved) */}
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
