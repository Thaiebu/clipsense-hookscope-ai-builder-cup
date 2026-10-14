import React, { useState } from 'react';
import { Languages, Loader2, Globe } from 'lucide-react';
import { translateFeedback } from '../api';

const SUPPORTED_LANGUAGES = [
  { code: 'Hindi', label: '🇮🇳 Hindi (हिन्दी)' },
  { code: 'Japanese', label: '🇯🇵 Japanese (日本語)' },
  { code: 'Spanish', label: '🇪🇸 Spanish (Español)' },
  { code: 'German', label: '🇩🇪 German (Deutsch)' },
  { code: 'French', label: '🇫🇷 French (Français)' },
];

export default function LanguageTranslate({ summary, topImprovements, titleAlternatives }) {
  const [selectedLang, setSelectedLang] = useState('Hindi');
  const [isTranslating, setIsTranslating] = useState(false);
  const [translatedData, setTranslatedData] = useState(null);
  const [error, setError] = useState(null);

  const handleTranslate = async () => {
    if (!summary) return;
    setIsTranslating(true);
    setError(null);

    try {
      const titles = (titleAlternatives || []).map((t) => t.title);
      const res = await translateFeedback({
        targetLanguage: selectedLang,
        summary,
        topImprovements: topImprovements || [],
        titleAlternatives: titles,
      });

      if (res.success && res.data) {
        setTranslatedData(res.data);
      } else {
        setError(res.error || 'Translation failed.');
      }
    } catch (err) {
      setError(err.message || 'Translation request failed.');
    } finally {
      setIsTranslating(false);
    }
  };

  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Languages size={18} color="var(--emerald)" />
          <span>Multilingual Creator Feedback</span>
        </h3>
        <span className="section-tag">Tier 3 • Global Reach</span>
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center', flexWrap: 'wrap', marginBottom: '1.25rem' }}>
        <select
          className="category-select"
          style={{ maxWidth: '240px', padding: '0.5rem 0.85rem', fontSize: '0.85rem' }}
          value={selectedLang}
          onChange={(e) => setSelectedLang(e.target.value)}
          disabled={isTranslating}
        >
          {SUPPORTED_LANGUAGES.map((l) => (
            <option key={l.code} value={l.code}>
              {l.label}
            </option>
          ))}
        </select>

        <button
          type="button"
          className="btn btn-outline btn-sm"
          onClick={handleTranslate}
          disabled={isTranslating || !summary}
        >
          {isTranslating ? (
            <>
              <Loader2 size={14} className="spin-animation" />
              <span>Translating...</span>
            </>
          ) : (
            <>
              <Globe size={14} />
              <span>Translate Feedback</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div style={{ color: 'var(--rose)', fontSize: '0.8rem', marginBottom: '1rem' }}>
          ⚠️ {error}
        </div>
      )}

      {translatedData && (
        <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-lg)', padding: '1.25rem' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--emerald)', marginBottom: '0.5rem' }}>
            {translatedData.target_language} Translation:
          </div>

          <div style={{ marginBottom: '1rem', fontSize: '0.85rem', color: 'var(--text-main)', lineHeight: 1.6 }}>
            {translatedData.translated_summary}
          </div>

          {translatedData.translated_improvements && translatedData.translated_improvements.length > 0 && (
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '0.35rem' }}>
                Key Improvements ({translatedData.target_language}):
              </div>
              <ul style={{ listStyle: 'disc inside', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                {translatedData.translated_improvements.map((imp, idx) => (
                  <li key={idx} style={{ marginBottom: '0.25rem' }}>
                    {imp}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
