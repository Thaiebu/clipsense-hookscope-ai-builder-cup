import React from 'react';
import { Eye, Sparkles, Terminal } from 'lucide-react';

export default function Header({ onOpenPromptModal, hasPrompts }) {
  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-icon">
          <span>🎯</span>
        </div>
        <div>
          <div className="brand-title">
            <span>HookScope</span>
            <span className="brand-badge">Gemini 2.5 Pro</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Explainable Video Feedback & Audience Simulation Engine • Google Cloud Run
          </p>
        </div>
      </div>

      <div className="header-actions">
        {hasPrompts && (
          <button
            onClick={onOpenPromptModal}
            className="btn btn-outline btn-sm"
            title="Inspect the exact structured prompts sent to Gemini"
          >
            <Terminal size={14} />
            <span>Inspect AI Reasoning</span>
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
