import React, { useEffect, useRef, useState, useImperativeHandle, forwardRef } from 'react';
import { ExternalLink, AlertTriangle, Play } from 'lucide-react';

/**
 * Extracts YouTube video ID from standard watch URLs, short URLs, and embed URLs.
 */
function extractVideoId(url) {
  if (!url) return null;
  const cleanUrl = url.trim();
  const regExp = /(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w-]{11})/;
  const match = cleanUrl.match(regExp);
  return match && match[1] ? match[1] : null;
}

const VideoPlayer = forwardRef(({ url, onDurationDetected }, ref) => {
  const videoId = extractVideoId(url);
  const containerRef = useRef(null);
  const playerRef = useRef(null);
  const [embedError, setEmbedError] = useState(false);
  const [currentTimestamp, setCurrentTimestamp] = useState(null);

  // Load YouTube IFrame API script once
  useEffect(() => {
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      if (firstScriptTag && firstScriptTag.parentNode) {
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
      } else {
        document.head.appendChild(tag);
      }
    }
  }, []);

  // Update or initialize YouTube player when videoId changes
  useEffect(() => {
    if (!videoId) return;
    setEmbedError(false);
    setCurrentTimestamp(null);

    // If player already exists and is initialized, cue the new video directly!
    if (playerRef.current && typeof playerRef.current.cueVideoById === 'function') {
      try {
        playerRef.current.cueVideoById(videoId);
        return;
      } catch (err) {
        console.warn('Failed to cue video by ID, re-initializing player:', err);
      }
    }

    let isSubscribed = true;
    let pollInterval = null;

    function initPlayer() {
      if (!window.YT || !window.YT.Player) {
        return; // Will retry in interval
      }

      const targetEl = containerRef.current;
      if (!targetEl || !isSubscribed) return;

      clearInterval(pollInterval);

      try {
        playerRef.current = new window.YT.Player(targetEl, {
          videoId,
          playerVars: {
            enablejsapi: 1,
            origin: window.location.origin,
            modestbranding: 1,
            rel: 0,
          },
          events: {
            onReady: (event) => {
              try {
                const duration = Math.floor(event.target.getDuration());
                if (duration > 0 && onDurationDetected) {
                  onDurationDetected(duration);
                }
              } catch (e) {
                console.warn('Could not read duration from player:', e);
              }
            },
            onError: (e) => {
              console.warn('YouTube Player error code:', e.data);
              // Error codes 101 and 150 mean embedding is disabled by video owner
              if (e.data === 101 || e.data === 150) {
                setEmbedError(true);
              }
            },
          },
        });
      } catch (err) {
        console.error('Failed to instantiate YouTube player:', err);
      }
    }

    if (window.YT && window.YT.Player) {
      initPlayer();
    } else {
      pollInterval = setInterval(initPlayer, 200);
    }

    return () => {
      isSubscribed = false;
      if (pollInterval) clearInterval(pollInterval);
    };
  }, [videoId]);

  // Expose seekTo function to parent/other components
  useImperativeHandle(ref, () => ({
    seekTo: (seconds) => {
      // 3-second pre-roll buffer (per design spec)
      const targetTime = Math.max(0, seconds - 3);
      setCurrentTimestamp(seconds);

      if (playerRef.current && typeof playerRef.current.seekTo === 'function') {
        playerRef.current.seekTo(targetTime, true);
        if (typeof playerRef.current.playVideo === 'function') {
          playerRef.current.playVideo();
        }
      }

      // Smooth scroll the player into view if needed
      if (containerRef.current) {
        containerRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    },
  }));

  if (!videoId) {
    return (
      <div className="player-card" style={{ padding: '3rem 1.5rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Paste a YouTube link above or click a 1-Click Demo to load the video preview.</p>
      </div>
    );
  }

  return (
    <div className="player-card">
      <div className="video-responsive-wrapper">
        <div ref={containerRef} />
      </div>

      <div className="player-info-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Play size={14} color="var(--cyan)" fill="var(--cyan)" />
          <span style={{ color: 'var(--text-secondary)' }}>
            {currentTimestamp !== null ? (
              <>
                Jumped to <strong style={{ color: 'var(--cyan)' }}>{formatTime(currentTimestamp)}</strong> (3s pre-roll buffer)
              </>
            ) : (
              'Click any timestamp moment below to seek'
            )}
          </span>
        </div>

        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-outline btn-sm"
          style={{ padding: '0.2rem 0.5rem' }}
        >
          <span>Watch on YouTube</span>
          <ExternalLink size={12} />
        </a>
      </div>

      {embedError && (
        <div style={{ padding: '1rem', background: 'rgba(244, 63, 94, 0.1)', borderTop: '1px solid var(--rose)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <AlertTriangle size={18} color="var(--rose)" />
          <p style={{ fontSize: '0.8rem', color: 'var(--rose)' }}>
            This video owner disabled third-party embedding (Code 150/101). You can still analyze it and click out to YouTube!
          </p>
        </div>
      )}
    </div>
  );
});

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s < 10 ? '0' : ''}${s}`;
}

export default VideoPlayer;
