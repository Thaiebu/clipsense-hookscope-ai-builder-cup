import React from 'react';
import { Clock, Play, List } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

export default function MomentCard({ summary, moments, onSeek }) {
  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <List size={18} color="var(--cyan)" />
          <span>Timeline Chapters & Summary</span>
        </h3>
        <span className="section-tag">{moments?.length || 0} Moments</span>
      </div>

      {summary && (
        <div style={{ marginBottom: '1.25rem', padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: 1.6 }}>
            {summary}
          </p>
        </div>
      )}

      <div className="moments-list">
        {moments && moments.map((m, idx) => (
          <div key={idx} className="moment-item">
            <button
              type="button"
              className="btn btn-play-timestamp"
              onClick={() => onSeek(m.timestamp_seconds)}
              title={`Seek to ${formatTime(m.timestamp_seconds)}`}
            >
              <Play size={10} fill="currentColor" />
              <span>{formatTime(m.timestamp_seconds)}</span>
            </button>

            <div className="moment-content">
              <div className="moment-title">{m.title}</div>
              <div className="moment-desc">{m.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
