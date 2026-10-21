import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowLeft,
  CheckCircle2,
  FileText,
  Layers3,
  UsersRound
} from 'lucide-react';

const TASK_GROUPS = [
  {
    category: 'Data Pipeline',
    tasks: ['Dataset', 'Preprocessing & Splitting']
  },
  {
    category: 'Architecture',
    tasks: ['Detection', 'Grad-CAM', 'Adversarial']
  },
  {
    category: 'Training Loop',
    tasks: ['Loss', 'Optimizer & Checkpointing', 'Cross-Dataset']
  }
];

const TEAM_MEMBERS = [
  {
    name: 'Durgam Poojitha',
    registerNumber: 'CB.SC.U4CSE23320',
    responsibilities: [
      'Implemented ART in the Video Detector.',
      'Contributed to research paper writing.'
    ]
  },
  {
    name: 'Alana Mariya P C',
    registerNumber: 'CB.SC.U4CSE23205',
    responsibilities: [
      'Implemented ART in the Image Detector.',
      'Contributed to research paper writing.'
    ]
  },
  {
    name: 'Sidharth S Nair',
    registerNumber: 'CB.SC.U4CSE23443',
    responsibilities: [
      'Implemented the Image Detector.',
      'Worked on cross-dataset evaluation.'
    ]
  },
  {
    name: 'Akshay Krishna P S',
    registerNumber: 'CB.SC.U4CSE23403',
    responsibilities: [
      'Implemented the Video Detector.',
      'Worked on cross-dataset evaluation.',
      'Contributed to research paper writing.'
    ]
  },
  {
    name: 'Kalyani H Karuvelil',
    registerNumber: 'CB.SC.U4CSE23423',
    responsibilities: [
      'Implemented the Video Detector.',
      'Worked on ART in the Video Detector.'
    ]
  }
];

const IMPLEMENTED_UPDATES = [
  'Image deepfake detection pipeline implemented.',
  'Video deepfake detection pipeline implemented.',
  'Compression-aware preprocessing implemented.',
  'Cross-dataset evaluation incorporated.',
  'Adversarial Robustness Training (ART) implemented in the image and video detector workflows.',
  'Grad-CAM-based explainability included in the project methodology.',
  'Research paper writing undertaken by the relevant team members.'
];

const taskCount = TASK_GROUPS.reduce((count, group) => count + group.tasks.length, 0);
const completedTaskCount = taskCount;
const completionPercent = Math.round((completedTaskCount / taskCount) * 100);

export default function Progress() {
  return (
    <div className="progress-page">
      <section className="progress-hero">
        <div className="container progress-hero-inner">
          <span className="section-tag">
            <Layers3 size={14} />
            Team 08 · Project status
          </span>
          <h1 className="progress-title">Project Progress &amp; Roadmap</h1>
          <p className="progress-lead">
            A clear record of completed CADET implementation work, team
            responsibilities, and project updates.
          </p>
          <div className="progress-summary" role="status">
            <CheckCircle2 size={19} />
            <span>
              The image and video implementation tasks listed below are complete.
            </span>
          </div>
          <p className="phase-note">
            Phase 2 implementation remains completed as documented.
          </p>
        </div>
      </section>

      <section className="progress-section" aria-labelledby="dashboard-title">
        <div className="container">
          <div className="section-header">
            <span className="section-tag">Implementation status</span>
            <h2 className="section-title" id="dashboard-title">
              Project Progress
            </h2>
            <p className="section-description">
              Status of the project components shown in the implementation
              overview.
            </p>
          </div>

          <div className="progress-dashboard">
            <article className="research-card progress-overview-card">
              <div className="completion-heading">
                <div>
                  <span className="completion-label">Listed task completion</span>
                  <p className="completion-value">
                    {completedTaskCount} of {taskCount} tasks
                  </p>
                </div>
                <strong className="completion-percent">{completionPercent}%</strong>
              </div>
              <div
                className="completion-track"
                role="progressbar"
                aria-label="Project task completion"
                aria-valuenow={completionPercent}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <span style={{ width: `${completionPercent}%` }} />
              </div>
              <div className="completion-legend">
                <span>
                  <CheckCircle2 size={15} />
                  {completedTaskCount} completed
                </span>
              </div>
            </article>

            <div className="task-groups">
              {TASK_GROUPS.map((group) => (
                <section className="research-card task-group" key={group.category}>
                  <h3>{group.category}</h3>
                  <ul>
                    {group.tasks.map((task) => (
                      <li className="task-row" key={task}>
                        <span className="task-status-icon" aria-hidden="true">
                          <CheckCircle2 size={17} />
                        </span>
                        <span className="task-name">{task}</span>
                        <span className="badge badge-success">Completed</span>
                      </li>
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="progress-section progress-section--tinted" aria-labelledby="team-title">
        <div className="container">
          <div className="section-header">
            <span className="section-tag">
              <UsersRound size={14} />
              Team 08
            </span>
            <h2 className="section-title" id="team-title">
              Team Responsibilities
            </h2>
            <p className="section-description">
              Contributions recorded for each member of the project team.
            </p>
          </div>

          <div className="team-grid">
            {TEAM_MEMBERS.map((member, index) => (
              <article className="research-card team-card" key={member.registerNumber}>
                <div className="team-card-heading">
                  <span className="team-number">{String(index + 1).padStart(2, '0')}</span>
                  <div>
                    <h3>{member.name}</h3>
                    <p className="team-register">{member.registerNumber}</p>
                  </div>
                </div>
                <h4 className="responsibility-label">Responsibilities</h4>
                <ul className="responsibility-list">
                  {member.responsibilities.map((responsibility) => (
                    <li key={responsibility}>
                      <CheckCircle2 size={15} />
                      <span>{responsibility}</span>
                    </li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="progress-section" aria-labelledby="updates-title">
        <div className="container">
          <div className="section-header">
            <span className="section-tag">
              <FileText size={14} />
              Project update
            </span>
            <h2 className="section-title" id="updates-title">
              Final Project Updates
            </h2>
            <p className="section-description">
              Implemented functionality and the remaining scope at a glance.
            </p>
          </div>

          <div className="updates-grid">
            <article className="research-card updates-card">
              <div className="updates-heading">
                <CheckCircle2 size={20} />
                <h3>Implemented</h3>
              </div>
              <ul className="updates-list">
                {IMPLEMENTED_UPDATES.map((update) => (
                  <li key={update}>
                    <CheckCircle2 size={16} />
                    <span>{update}</span>
                  </li>
                ))}
              </ul>
            </article>
          </div>

          <div className="progress-return">
            <Link to="/" className="btn btn-primary">
              <ArrowLeft size={16} />
              <span>Return to Project Overview</span>
            </Link>
          </div>
        </div>
      </section>

      <style>{`
        .progress-page {
          background: var(--color-bg-base);
        }

        .progress-hero {
          padding: 4.5rem 0 3rem;
          background: linear-gradient(135deg, #fff 0%, #fdf5f6 100%);
          border-bottom: 1px solid var(--color-border);
        }

        .progress-hero-inner {
          max-width: 960px;
        }

        .progress-title {
          max-width: 850px;
          margin: 0 0 1rem;
          font-size: clamp(2rem, 4vw, 3.1rem);
          color: var(--color-navy);
        }

        .progress-lead {
          max-width: 760px;
          color: var(--color-slate);
          font-size: 1.1rem;
        }

        .progress-summary {
          display: flex;
          align-items: flex-start;
          gap: 0.75rem;
          max-width: 850px;
          margin-top: 1.75rem;
          padding: 1rem 1.2rem;
          color: var(--color-success);
          background: var(--color-success-bg);
          border: 1px solid var(--color-success-border);
          border-radius: var(--radius-md);
          font-weight: 600;
        }

        .progress-summary svg {
          flex: 0 0 auto;
          margin-top: 0.15rem;
        }

        .phase-note {
          margin-top: 0.9rem;
          color: var(--color-slate);
          font-size: 0.9rem;
        }

        .progress-section {
          padding: 4rem 0;
        }

        .progress-section--tinted {
          background: #f4f2ef;
          border-top: 1px solid var(--color-border-subtle);
          border-bottom: 1px solid var(--color-border-subtle);
        }

        .progress-dashboard {
          display: grid;
          grid-template-columns: minmax(240px, 0.75fr) minmax(0, 1.7fr);
          gap: 1.25rem;
          align-items: start;
        }

        .progress-overview-card {
          position: sticky;
          top: 96px;
        }

        .completion-heading {
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 1rem;
        }

        .completion-label {
          color: var(--color-slate);
          font-size: 0.85rem;
          font-weight: 600;
        }

        .completion-value {
          margin-top: 0.4rem;
          color: var(--color-navy);
          font-size: 1.1rem;
          font-weight: 700;
        }

        .completion-percent {
          color: var(--color-success);
          font-size: 1.7rem;
        }

        .completion-track {
          height: 10px;
          margin: 1.25rem 0 0.85rem;
          overflow: hidden;
          background: var(--color-slate-subtle);
          border-radius: var(--radius-full);
        }

        .completion-track span {
          display: block;
          height: 100%;
          background: var(--color-success);
          border-radius: inherit;
        }

        .completion-legend {
          display: flex;
          flex-wrap: wrap;
          gap: 0.8rem 1rem;
          color: var(--color-success);
          font-size: 0.82rem;
          font-weight: 600;
        }

        .completion-legend span {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
        }

        .task-groups {
          display: grid;
          gap: 1rem;
        }

        .task-group {
          padding: 1.25rem 1.5rem;
        }

        .task-group h3 {
          margin-bottom: 0.6rem;
          font-size: 1rem;
        }

        .task-group ul,
        .responsibility-list,
        .updates-list {
          list-style: none;
        }

        .task-row {
          display: flex;
          align-items: center;
          gap: 0.7rem;
          min-height: 45px;
          border-top: 1px solid var(--color-border-subtle);
        }

        .task-status-icon {
          display: inline-flex;
          color: var(--color-success);
        }

        .task-name {
          flex: 1;
          color: var(--color-slate-dark);
        }

        .task-row .badge {
          flex: 0 0 auto;
        }

        .team-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 1rem;
        }

        .team-card {
          padding: 1.5rem;
        }

        .team-card-heading {
          display: flex;
          align-items: flex-start;
          gap: 0.85rem;
        }

        .team-number {
          display: inline-flex;
          flex: 0 0 auto;
          align-items: center;
          justify-content: center;
          width: 38px;
          height: 38px;
          color: var(--color-primary);
          background: var(--color-primary-subtle);
          border: 1px solid var(--color-primary-border);
          border-radius: var(--radius-full);
          font-size: 0.85rem;
          font-weight: 700;
        }

        .team-card-heading h3 {
          margin: 0.1rem 0 0.2rem;
          font-size: 1.08rem;
        }

        .team-register {
          color: var(--color-slate);
          font-family: var(--font-mono);
          font-size: 0.78rem;
          overflow-wrap: anywhere;
        }

        .responsibility-label {
          margin: 1.25rem 0 0.6rem;
          color: var(--color-slate);
          font-size: 0.78rem;
          letter-spacing: 0.06em;
          text-transform: uppercase;
        }

        .responsibility-list,
        .updates-list {
          display: grid;
          gap: 0.65rem;
        }

        .responsibility-list li,
        .updates-list li {
          display: flex;
          align-items: flex-start;
          gap: 0.55rem;
          color: var(--color-slate-dark);
          font-size: 0.92rem;
        }

        .responsibility-list svg,
        .updates-list svg {
          flex: 0 0 auto;
          margin-top: 0.2rem;
          color: var(--color-success);
        }

        .updates-card {
          padding: 1.75rem;
        }

        .updates-grid {
          display: grid;
          grid-template-columns: minmax(0, 1fr);
        }

        .updates-heading {
          display: flex;
          align-items: center;
          gap: 0.6rem;
          margin-bottom: 1.15rem;
        }

        .updates-heading svg {
          color: var(--color-success);
        }

        .updates-heading h3 {
          font-size: 1.15rem;
        }

        .progress-return {
          display: flex;
          justify-content: center;
          margin-top: 2.5rem;
        }

        @media (max-width: 800px) {
          .progress-dashboard {
            grid-template-columns: 1fr;
          }

          .progress-overview-card {
            position: static;
          }

          .team-grid {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 640px) {
          .progress-hero {
            padding: 3rem 0 2.25rem;
          }

          .progress-section {
            padding: 3rem 0;
          }

          .progress-lead {
            font-size: 1rem;
          }

          .updates-grid {
            grid-template-columns: 1fr;
          }

          .task-group {
            padding: 1rem;
          }

          .task-row {
            gap: 0.45rem;
          }

          .task-row .badge {
            padding: 0.28rem 0.5rem;
            font-size: 0.7rem;
          }
        }
      `}</style>
    </div>
  );
}
