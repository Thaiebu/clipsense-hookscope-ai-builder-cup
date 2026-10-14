import React, { useState } from 'react';
import { X, Copy, Check, Terminal, ShieldAlert } from 'lucide-react';

export default function InspectReasoningModal({ prompts, onClose }) {
  const [copiedKey, setCopiedKey] = useState(null);
  const [activeTab, setActiveTab] = useState(Object.keys(prompts)[0] || 'call1');

  const handleCopy = (key, text) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const tabs = [
    { key: 'call1', label: 'Call 1: Master Analysis' },
    { key: 'call2', label: 'Call 2: Audience Panel' },
    { key: 'shorts', label: 'Feature 8: Shorts Clips' },
  ].filter((t) => Boolean(prompts[t.key]));

  const currentPromptText = prompts[activeTab] || Object.values(prompts)[0] || '';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <Terminal size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
              Inspect AI Reasoning & Prompts
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
          <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', gap: '0.4rem' }}>
              {tabs.map((t) => (
                <button
                  key={t.key}
                  type="button"
                  className={`persona-tab-btn ${activeTab === t.key ? 'active' : ''}`}
                  style={{ fontSize: '0.75rem', padding: '0.3rem 0.75rem' }}
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
                  <span style={{ color: 'var(--emerald)' }}>Copied!</span>
                </>
              ) : (
                <>
                  <Copy size={14} />
                  <span>Copy Prompt</span>
                </>
              )}
            </button>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem', padding: '0.6rem 0.85rem', background: 'rgba(99, 102, 241, 0.08)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-accent)' }}>
            <ShieldAlert size={16} color="var(--primary)" />
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Full transparency proof: Below is the exact prompt and schema instruction transmitted to Gemini 2.5 on Google Cloud.
            </p>
          </div>

          <pre className="code-pre">{currentPromptText}</pre>
        </div>
      </div>
    </div>
  );
}
