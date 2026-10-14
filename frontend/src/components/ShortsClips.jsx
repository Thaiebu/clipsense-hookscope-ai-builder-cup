import React from 'react';
import { Film, Play, Scissors, Sparkles } from 'lucide-react';

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

export default function ShortsClips({ clips, onSeek }) {
  if (!clips || clips.length === 0) return null;

  return (
    <div className="section-card">
      <div className="section-header">
        <h3 className="section-title">
          <Film size={18} color="var(--purple)" />
          <span>Viral YouTube Shorts Candidates</span>
        </h3>
        <span className="section-tag" style={{ background: 'rgba(168, 85, 247, 0.15)', color: 'var(--purple)' }}>
          &lt;60s Standalone
        </span>
      </div>

      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        Gemini scanned your video for high-retention segments that can be clipped directly into 9:16 vertical Shorts:
      </p>

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
                <span>{formatTime(clip.start_seconds)} - {formatTime(clip.end_seconds)}</span>
              </button>
            </div>

            <div style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--text-main)' }}>
              {clip.title}
            </div>

            <div className="short-caption-box">
              <span style={{ fontSize: '0.65rem', textTransform: 'uppercase', color: 'var(--purple)', fontWeight: 700, display: 'block' }}>
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
    </div>
  );
}
