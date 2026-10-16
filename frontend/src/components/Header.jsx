import React from 'react';
import { Sparkles, Terminal } from 'lucide-react';

export default function Header({ onOpenPromptModal, hasPrompts, isCached, hasAnalysis, modelUsed }) {
  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-icon">
          <span>🎯</span>
        </div>
        <div>
          <div className="brand-title">
            <span>HookScope</span>
            <span className="brand-badge">Gemini 3.8 Flash</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Explainable Video Feedback & Audience Simulation Engine • Google Cloud Run
          </p>
        </div>
      </div>

      <div className="header-actions">
        {hasAnalysis && isCached !== undefined && (
          <div
            className={`badge ${isCached ? 'badge-amber' : 'badge-emerald'}`}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '0.3rem 0.65rem',
              fontSize: '0.75rem',
              fontWeight: 600,
            }}
          >
            {isCached ? (
              <>
                <span>📦</span>
                <span>Pre-cached Benchmark</span>
              </>
            ) : (
              <>
                <span style={{ display: 'inline-block', width: '7px', height: '7px', borderRadius: '50%', backgroundColor: 'var(--emerald)', boxShadow: '0 0 6px var(--emerald)' }}></span>
                <span>Live {modelUsed || 'Gemini 3.8 Flash'}</span>
              </>
            )}
          </div>
        )}

        {hasPrompts && (
          <button
            onClick={onOpenPromptModal}
            className="btn btn-outline btn-sm"
            title="Inspect underlying prompts, model metadata, and scoring rubric"
          >
            <Terminal size={14} color="var(--primary)" />
            <span>Inspect AI Prompts & Scoring</span>
          </button>
        )}
        <div className="btn btn-outline btn-sm" style={{ cursor: 'default', opacity: 0.85 }}>
          <Sparkles size={14} color="var(--cyan)" />
          <span>AI Builder Cup 2026</span>
        </div>
      </div>
    </header>
  );
}
