import React from 'react';
import { Target, Play, Lightbulb } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

function getScoreClass(score) {
  if (score >= 8) return 'score-high';
  if (score >= 5) return 'score-mid';
  return 'score-low';
}

export default function HookAnalysis({ hookScore, hookDimensions, onSeek }) {
  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Target size={18} color="var(--primary)" />
          <span>Hook Analysis (First 30 Seconds)</span>
        </h3>
        <span className={`score-badge ${getScoreClass(hookScore)}`}>
          Overall Hook: {hookScore ? Number(hookScore).toFixed(1) : 0}/10
        </span>
      </div>

      <div className="hook-grid">
        {hookDimensions && hookDimensions.map((dim, idx) => (
          <div key={idx} className="hook-dimension-card">
            <div className="dim-header">
              <span className="dim-name">{dim.name}</span>
              <span className={`score-badge ${getScoreClass(dim.score)}`}>
                {dim.score}/10
              </span>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', margin: '0.25rem 0' }}>
              <button
                type="button"
                className="btn btn-play-timestamp"
                onClick={() => onSeek(dim.timestamp_seconds)}
                title={`Seek to evidence at ${formatTime(dim.timestamp_seconds)}`}
              >
                <Play size={10} fill="currentColor" />
                <span>{formatTime(dim.timestamp_seconds)}</span>
              </button>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Evidence Moment</span>
            </div>

            <p className="dim-evidence">
              "{dim.observation}"
            </p>

            {dim.suggestion && (
              <div className="dim-suggestion">
                <strong>Fix:</strong> {dim.suggestion}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
