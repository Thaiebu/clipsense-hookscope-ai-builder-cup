import React from 'react';
import { Film, Play, Sparkles, Loader2, Scissors } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

export default function ShortsClips({
  clips,
  onSeek,
  onGenerateShorts,
  isGenerating,
  error,
}) {
  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Film size={18} color="var(--purple)" />
          <span>Viral YouTube Shorts Candidates</span>
        </h3>
        <span
          className="section-tag"
          style={{ background: 'rgba(168, 85, 247, 0.15)', color: 'var(--purple)' }}
        >
          Tier 3 • On-Demand
        </span>
      </div>

      <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '1.25rem', lineHeight: 1.5 }}>
        Scan your video for self-contained high-retention segments (&lt;60s) with 0–3s hook captions, ideal for 9:16 vertical Shorts, Reels, or TikToks.
      </p>

      {/* When clips are not generated yet, show the explicit on-demand button */}
      {(!clips || clips.length === 0) && (
        <div className="shorts-cta-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--purple)', fontWeight: 700 }}>
            <Scissors size={20} />
            <span>Generate 2–3 Standalone Shorts Clips</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', maxWidth: '420px', margin: '0 auto' }}>
            Click below to run a dedicated Gemini model call that extracts viral moments without bloating initial analysis time.
          </p>

          <button
            type="button"
            className="btn btn-outline"
            style={{
              borderColor: 'var(--purple)',
              color: 'var(--text-main)',
              background: 'rgba(168, 85, 247, 0.12)',
              marginTop: '0.5rem',
            }}
            onClick={onGenerateShorts}
            disabled={isGenerating}
          >
            {isGenerating ? (
              <>
                <Loader2 size={16} className="spin-animation" color="var(--purple)" />
                <span>Scanning Video for Shorts (&lt;60s)...</span>
              </>
            ) : (
              <>
                <Sparkles size={16} color="var(--purple)" />
                <span>⚡ Generate Viral Shorts Candidates</span>
              </>
            )}
          </button>

          {error && (
            <div style={{ color: 'var(--rose)', fontSize: '0.78rem', marginTop: '0.5rem' }}>
              ⚠️ {error}
            </div>
          )}
        </div>
      )}

      {/* When clips exist, display the cards */}
      {clips && clips.length > 0 && (
        <div className="shorts-grid">
          {clips.map((clip, idx) => (
            <div key={idx} className="short-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className="short-duration-tag">
                  ⏱️ {clip.duration_seconds}s Duration
                </span>

                <button
                  type="button"
                  className="btn btn-play-timestamp"
                  onClick={() => onSeek(clip.start_seconds)}
                  title={`Seek to ${formatTime(clip.start_seconds)}`}
                >
                  <Play size={10} fill="currentColor" />
                  <span>
                    {formatTime(clip.start_seconds)} - {formatTime(clip.end_seconds)}
                  </span>
                </button>
              </div>

              <div style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)' }}>
                {clip.title}
              </div>

              <div className="short-caption-box">
                <span
                  style={{
                    fontSize: '0.65rem',
                    textTransform: 'uppercase',
                    color: 'var(--purple)',
                    fontWeight: 700,
                    display: 'block',
                  }}
                >
                  On-Screen Hook Caption (0-3s):
                </span>
                "{clip.hook_caption}"
              </div>

              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: 'auto' }}>
                <strong>Why it works:</strong> {clip.reason_standalone}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
