import React from 'react';
import { Gauge, CheckSquare, ShieldCheck } from 'lucide-react';

export default function ReadinessScore({ readinessScore, scoreFactors, topImprovements, isCached, modelUsed }) {
  const score = readinessScore || 0;

  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Gauge size={18} color="var(--emerald)" />
          <span>Content Readiness Score</span>
        </h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          {isCached !== undefined && (
            <span
              className={`badge ${isCached ? 'badge-amber' : 'badge-emerald'}`}
              style={{ fontSize: '0.7rem', padding: '0.2rem 0.5rem' }}
            >
              {isCached ? '📦 Benchmark Sample' : `🟢 Live ${modelUsed || 'Gemini 3.8 Flash'}`}
            </span>
          )}
          <span className="section-tag" style={{ display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <ShieldCheck size={12} color="var(--emerald)" />
            Engagement Rubric
          </span>
        </div>
      </div>

      <div className="readiness-dashboard">
        <div className="score-circle-wrapper">
          <div className="big-score gradient-accent">{score}</div>
          <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700, letterSpacing: '0.05em' }}>
            Out of 100
          </div>
        </div>

        <div className="score-factors-list">
          {scoreFactors && scoreFactors.map((factor, idx) => {
            const pct = (factor.score / 25) * 100;
            return (
              <div key={idx} className="factor-row">
                <span className="factor-name">{factor.name}</span>
                <div className="factor-bar-track">
                  <div
                    className="factor-bar-fill"
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, width: '40px', textAlign: 'right' }}>
                  {factor.score}/25
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {topImprovements && topImprovements.length > 0 && (
        <div className="improvements-box">
          <div className="improvements-title">
            <CheckSquare size={14} color="var(--primary)" />
            <span>Top Prioritized Improvements:</span>
          </div>
          <ul className="improvements-list">
            {topImprovements.map((imp, idx) => (
              <li key={idx} className="improvement-item">
                <span>{imp}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
