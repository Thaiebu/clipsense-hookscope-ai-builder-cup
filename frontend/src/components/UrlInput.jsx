import React from 'react';
import { Search, Play, Loader2, XCircle } from 'lucide-react';

export default function UrlInput({
  url,
  setUrl,
  category,
  setCategory,
  niches,
  samples,
  isLoading,
  onSubmit,
  onCancel,
}) {
  const handleSampleClick = (sampleUrl, sampleCategory) => {
    setUrl(sampleUrl);
    if (sampleCategory && niches[sampleCategory.toLowerCase()]) {
      setCategory(sampleCategory.toLowerCase());
    }
  };

  return (
    <div className="input-hero-card">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onSubmit();
        }}
      >
        <div className="input-row">
          <div className="url-input-wrapper">
            <Search className="url-input-icon" size={18} />
            <input
              type="text"
              className="url-input"
              placeholder="Paste any YouTube video URL (e.g., https://youtu.be/...)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>

          <div className="category-select-wrapper">
            <select
              className="category-select"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              disabled={isLoading}
            >
              {Object.keys(niches).length > 0 ? (
                Object.entries(niches).map(([key, val]) => (
                  <option key={key} value={key}>
                    {val.display_name}
                  </option>
                ))
              ) : (
                <>
                  <option value="fitness">Fitness & Exercise</option>
                  <option value="tech">Tech & Programming</option>
                  <option value="cooking">Cooking & Recipes</option>
                  <option value="education">Education & Explainers</option>
                  <option value="general">General Video</option>
                </>
              )}
            </select>
          </div>

          {isLoading ? (
            <button
              type="button"
              className="btn btn-outline"
              onClick={onCancel}
              title="Cancel Analysis"
              style={{ color: 'var(--rose)' }}
            >
              <XCircle size={16} />
              <span>Cancel</span>
            </button>
          ) : (
            <button
              type="submit"
              className="btn btn-primary"
              disabled={!url.trim()}
            >
              <Play size={16} fill="currentColor" />
              <span>Analyze Video</span>
            </button>
          )}
        </div>

        {/* 1-Click Curated Demos */}
        {samples && samples.length > 0 && (
          <div className="samples-row">
            <span className="samples-label">⚡ 1-Click Demos:</span>
            {samples.map((s) => (
              <button
                key={s.id}
                type="button"
                className="sample-chip"
                onClick={() => handleSampleClick(s.youtube_url, 'fitness')}
                disabled={isLoading}
              >
                {s.title.length > 38 ? `${s.title.substring(0, 36)}...` : s.title}
              </button>
            ))}
          </div>
        )}
      </form>
    </div>
  );
}
