import React, { useState } from 'react';
import { X, Copy, Check, Terminal, ShieldAlert, Cpu, Database, Award } from 'lucide-react';

export default function InspectReasoningModal({
  prompts,
  modelUsed = 'gemini-3.8-flash',
  isCached = false,
  onClose,
}) {
  const [copiedKey, setCopiedKey] = useState(null);
  const [activeTab, setActiveTab] = useState(Object.keys(prompts)[0] || 'call1');
  const [showRubricInfo, setShowRubricInfo] = useState(true);

  const handleCopy = (key, text) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const tabs = [
    { key: 'call1', label: 'Call 1: Master Video Analysis' },
    { key: 'call2', label: 'Call 2: Audience Panel Simulation' },
    { key: 'shorts', label: 'Call 3: Viral Shorts Extraction' },
  ].filter((t) => Boolean(prompts[t.key]));

  const currentPromptText = prompts[activeTab] || Object.values(prompts)[0] || '';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '820px' }}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Terminal size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
              Inspect AI Prompts & Scoring
            </h3>
          </div>
          <button
            type="button"
            className="btn btn-outline btn-sm"
            style={{ padding: '0.25rem 0.5rem', borderRadius: 'var(--radius-full)' }}
            onClick={onClose}
          >
            <X size={16} />
          </button>
        </div>

        <div className="modal-body">
          {/* Metadata Badges */}
          <div
            style={{
              display: 'flex',
              gap: '0.75rem',
              alignItems: 'center',
              flexWrap: 'wrap',
              marginBottom: '1rem',
              padding: '0.65rem 0.85rem',
              background: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.78rem', color: 'var(--text-main)' }}>
              <Cpu size={14} color="var(--primary)" />
              <span>Model:</span>
              <strong style={{ color: 'var(--cyan)' }}>{modelUsed}</strong>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.78rem', color: 'var(--text-main)' }}>
              <Database size={14} color="var(--emerald)" />
              <span>Data Origin:</span>
              {isCached ? (
                <span className="badge badge-amber" style={{ fontSize: '0.7rem' }}>
                  📦 Pre-cached Benchmark Sample
                </span>
              ) : (
                <span className="badge badge-emerald" style={{ fontSize: '0.7rem' }}>
                  🟢 Live Gemini API Inference
                </span>
              )}
            </div>

            <button
              type="button"
              className="btn btn-outline btn-sm"
              style={{ marginLeft: 'auto', fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
              onClick={() => setShowRubricInfo(!showRubricInfo)}
            >
              <Award size={13} color="var(--amber)" />
              <span>{showRubricInfo ? 'Hide Scoring Rubric' : 'Show Scoring Rubric'}</span>
            </button>
          </div>

          {/* Scoring Rubric Definitions */}
          {showRubricInfo && (
            <div
              style={{
                marginBottom: '1.25rem',
                padding: '0.85rem 1rem',
                background: 'rgba(99, 102, 241, 0.05)',
                border: '1px solid var(--border-accent)',
                borderRadius: 'var(--radius-md)',
              }}
            >
              <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--primary)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                Deterministic Hook Scoring Rubric (0–10 Scale)
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.65rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                <div>
                  <strong style={{ color: 'var(--text-main)' }}>1. Clarity:</strong> Topic stated clearly within the first 10 seconds.
                </div>
                <div>
                  <strong style={{ color: 'var(--text-main)' }}>2. Curiosity:</strong> Creates tension, a question, or intrigue before resolution.
                </div>
                <div>
                  <strong style={{ color: 'var(--text-main)' }}>3. Pacing:</strong> Minimizes dead air, throat-clearing, and slow setup.
                </div>
                <div>
                  <strong style={{ color: 'var(--text-main)' }}>4. Payoff Promise:</strong> States what the viewer will gain by watching.
                </div>
              </div>
            </div>
          )}

          {/* Prompt Tabs and Copy Action */}
          <div style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
              {tabs.map((t) => (
                <button
                  key={t.key}
                  type="button"
                  className={`persona-tab-btn ${activeTab === t.key ? 'active' : ''}`}
                  style={{ fontSize: '0.75rem', padding: '0.35rem 0.8rem' }}
                  onClick={() => setActiveTab(t.key)}
                >
                  {t.label}
                </button>
              ))}
            </div>

            <button
              type="button"
              className="btn btn-outline btn-sm"
              onClick={() => handleCopy(activeTab, currentPromptText)}
            >
              {copiedKey === activeTab ? (
                <>
                  <Check size={14} color="var(--emerald)" />
                  <span style={{ color: 'var(--emerald)' }}>Copied Prompt!</span>
                </>
              ) : (
                <>
                  <Copy size={14} />
                  <span>Copy System Prompt</span>
                </>
              )}
            </button>
          </div>

          <pre className="code-pre">{currentPromptText}</pre>
        </div>
      </div>
    </div>
  );
}
