import React, { useState } from 'react';
import { Users, ThumbsUp, AlertTriangle, Play, Sparkles, Scale } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

export default function AudiencePanel({ panelReactions, disagreements, onSeek }) {
  const [activePersonaIdx, setActivePersonaIdx] = useState(0);

  if (!panelReactions || panelReactions.length === 0) {
    return null;
  }

  const activePersona = panelReactions[activePersonaIdx] || panelReactions[0];

  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Users size={18} color="var(--cyan)" />
          <span>Simulated Audience Panel</span>
        </h3>
        <span className="section-tag" style={{ background: 'rgba(6, 182, 212, 0.15)', color: 'var(--cyan)' }}>
          ⭐ Key Innovation
        </span>
      </div>

      {/* Persona Selection Tabs */}
      <div className="persona-tabs">
        {panelReactions.map((p, idx) => (
          <button
            key={idx}
            type="button"
            className={`persona-tab-btn ${idx === activePersonaIdx ? 'active' : ''}`}
            onClick={() => setActivePersonaIdx(idx)}
          >
            {p.persona}
          </button>
        ))}
      </div>

      {/* Active Persona Details */}
      <div className="persona-card-content">
        <div style={{ padding: '0.75rem 1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <span style={{ fontSize: '0.7rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)' }}>
              Overall Persona Assessment:
            </span>
            <div style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-main)', marginTop: '0.15rem' }}>
              "{activePersona.overall_rating}"
            </div>
          </div>
        </div>

        {/* Positive Highlights */}
        {activePersona.highlights && activePersona.highlights.length > 0 && (
          <div>
            <div className="reactions-group-title" style={{ color: 'var(--emerald)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <ThumbsUp size={12} /> Positive Highlights
            </div>
            {activePersona.highlights.map((h, i) => (
              <div key={i} className="highlight-item">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                  <button
                    type="button"
                    className="btn btn-play-timestamp"
                    onClick={() => onSeek(h.timestamp_seconds)}
                    title={`Seek to ${formatTime(h.timestamp_seconds)}`}
                  >
                    <Play size={10} fill="currentColor" />
                    <span>{formatTime(h.timestamp_seconds)}</span>
                  </button>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Reaction</span>
                </div>
                <p style={{ color: 'var(--text-main)' }}>{h.reaction}</p>
              </div>
            ))}
          </div>
        )}

        {/* Constructive Concerns */}
        {activePersona.concerns && activePersona.concerns.length > 0 && (
          <div>
            <div className="reactions-group-title" style={{ color: 'var(--rose)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <AlertTriangle size={12} /> Friction Points & Friction
            </div>
            {activePersona.concerns.map((c, i) => (
              <div key={i} className="concern-item">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                  <button
                    type="button"
                    className="btn btn-play-timestamp"
                    onClick={() => onSeek(c.timestamp_seconds)}
                    title={`Seek to ${formatTime(c.timestamp_seconds)}`}
                  >
                    <Play size={10} fill="currentColor" />
                    <span>{formatTime(c.timestamp_seconds)}</span>
                  </button>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Friction Point</span>
                </div>
                <p style={{ color: 'var(--text-main)' }}>{c.reaction}</p>
                {c.suggestion && (
                  <p style={{ fontSize: '0.75rem', color: 'var(--rose)', marginTop: '0.35rem' }}>
                    <strong>Suggestion:</strong> {c.suggestion}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Disagreements Matrix Card */}
      {disagreements && disagreements.length > 0 && (
        <div className="disagreements-wrapper">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <Scale size={16} color="var(--amber)" />
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--amber)' }}>
              Audience Disagreements Matrix
            </h4>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            These moments reveal trade-offs between different viewer demographics. No choice is wrong, but each alienates or engages a different audience!
          </p>

          {disagreements.map((d, idx) => {
            // Support both dynamic (persona_1..3) and legacy persona fields
            const p1View = d.persona_1 || d.beginner;
            const p2View = d.persona_2 || d.experienced;
            const p3View = d.persona_3 || d.home_viewer;

            return (
              <div key={idx} className="disagreement-card">
                <div className="disagreement-topic">
                  <span>⚡ Conflict: {d.topic}</span>
                  <button
                    type="button"
                    className="btn btn-play-timestamp"
                    onClick={() => onSeek(d.timestamp_seconds)}
                    title={`Seek to ${formatTime(d.timestamp_seconds)}`}
                  >
                    <Play size={10} fill="currentColor" />
                    <span>{formatTime(d.timestamp_seconds)}</span>
                  </button>
                </div>

                <div className="disagreement-grid">
                  <div className="disagreement-cell">
                    <div className="persona-name-tag">{panelReactions[0]?.persona || 'Persona 1'}:</div>
                    <div>{p1View}</div>
                  </div>
                  <div className="disagreement-cell">
                    <div className="persona-name-tag">{panelReactions[1]?.persona || 'Persona 2'}:</div>
                    <div>{p2View}</div>
                  </div>
                  <div className="disagreement-cell">
                    <div className="persona-name-tag">{panelReactions[2]?.persona || 'Persona 3'}:</div>
                    <div>{p3View}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
