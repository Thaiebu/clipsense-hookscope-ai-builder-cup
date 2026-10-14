import React from 'react';
import { Type, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';

export default function TitleComparison({ currentAssessment, alternatives, recommendedIndex }) {
  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Type size={18} color="var(--purple)" />
          <span>Title & Hook Alternatives</span>
        </h3>
        <span className="section-tag">Rubric Evaluated</span>
      </div>

      {currentAssessment && (
        <div style={{ marginBottom: '1.25rem', padding: '0.85rem 1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)' }}>
            Current Title Diagnosis:
          </span>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
            {currentAssessment}
          </p>
        </div>
      )}

      <div className="titles-list">
        {alternatives && alternatives.map((alt, idx) => {
          const isRecommended = idx === recommendedIndex;
          return (
            <div
              key={idx}
              className={`title-card ${isRecommended ? 'recommended' : ''}`}
            >
              {isRecommended && (
                <div className="recommended-pill">
                  <Sparkles size={10} style={{ display: 'inline', marginRight: '3px' }} />
                  Best Fit Under Rubric
                </div>
              )}

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
                <div className="alt-title-text">
                  "{alt.title}"
                </div>
                <span className="score-badge score-high" style={{ fontSize: '0.7rem' }}>
                  Rubric: {alt.rubric_score}/10
                </span>
              </div>

              <div className="pros-cons-grid">
                <div className="pro-box">
                  <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <CheckCircle2 size={12} /> Strengths
                  </span>
                  <p style={{ marginTop: '0.2rem', color: 'var(--text-secondary)' }}>
                    {alt.strengths}
                  </p>
                </div>

                <div className="con-box">
                  <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <AlertCircle size={12} /> Trade-offs
                  </span>
                  <p style={{ marginTop: '0.2rem', color: 'var(--text-secondary)' }}>
                    {alt.weaknesses}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
