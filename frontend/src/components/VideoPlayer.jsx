import React, { useEffect, useRef, useState, useImperativeHandle, forwardRef } from 'react';
import { ExternalLink, AlertTriangle, Play } from 'lucide-react';

/**
 * Extracts YouTube video ID from standard watch URLs, short URLs, and embed URLs.
 */
function extractVideoId(url) {
  if (!url) return null;
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return match && match[2].length === 11 ? match[2] : null;
}

const VideoPlayer = forwardRef(({ url, onDurationDetected }, ref) => {
  const videoId = extractVideoId(url);
  const iframeRef = useRef(null);
  const playerRef = useRef(null);
  const [embedError, setEmbedError] = useState(false);
  const [currentTimestamp, setCurrentTimestamp] = useState(null);

  // Load YouTube IFrame API script once
  useEffect(() => {
    if (!window.YT) {
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
  }, []);

  // Initialize YouTube Player when videoId changes
  useEffect(() => {
    if (!videoId) return;
    setEmbedError(false);

    let isSubscribed = true;

    function initPlayer() {
      if (!window.YT || !window.YT.Player) {
        setTimeout(initPlayer, 200);
        return;
      }

      if (!isSubscribed) return;

      try {
        if (playerRef.current && typeof playerRef.current.destroy === 'function') {
          playerRef.current.destroy();
        }

        playerRef.current = new window.YT.Player(`yt-player-container`, {
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

    initPlayer();

    return () => {
      isSubscribed = false;
    };
  }, [videoId]);

  // Expose seekTo function to parent/other components
  useImperativeHandle(ref, () => ({
    seekTo: (seconds) => {
      // 3-second pre-roll buffer (per plan loophole #3)
      const targetTime = Math.max(0, seconds - 3);
      setCurrentTimestamp(seconds);

      if (playerRef.current && typeof playerRef.current.seekTo === 'function') {
        playerRef.current.seekTo(targetTime, true);
        if (typeof playerRef.current.playVideo === 'function') {
          playerRef.current.playVideo();
        }
      }

      // Smooth scroll the player into view if needed
      if (iframeRef.current) {
        iframeRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    },
  }));

  if (!videoId) {
    return (
      <div className="player-card" style={{ padding: '3rem 1.5rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Paste a YouTube link above to load the video preview.</p>
      </div>
    );
  }

  return (
    <div className="player-card" ref={iframeRef}>
      <div className="video-responsive-wrapper">
        <div id="yt-player-container" />
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
