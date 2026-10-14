import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import UrlInput from './components/UrlInput';
import VideoPlayer from './components/VideoPlayer';
import ProgressTracker from './components/ProgressTracker';
import MomentCard from './components/MomentCard';
import HookAnalysis from './components/HookAnalysis';
import TitleComparison from './components/TitleComparison';
import ReadinessScore from './components/ReadinessScore';
import AudiencePanel from './components/AudiencePanel';
import ShortsClips from './components/ShortsClips';
import LanguageTranslate from './components/LanguageTranslate';
import InspectReasoningModal from './components/InspectReasoningModal';
import ErrorBoundary from './components/ErrorBoundary';

import {
  fetchNiches,
  fetchSamples,
  analyzeVideo,
  analyzePanel,
  fetchShorts,
} from './api';

export default function App() {
  const [url, setUrl] = useState('');
  const [category, setCategory] = useState('fitness');
  const [videoDuration, setVideoDuration] = useState(0);
  const [niches, setNiches] = useState({});
  const [samples, setSamples] = useState([]);

  // Loading and progressive steps
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);

  // Analysis Results
  const [masterData, setMasterData] = useState(null);
  const [panelData, setPanelData] = useState(null);
  const [shortsData, setShortsData] = useState(null);
  const [isGeneratingShorts, setIsGeneratingShorts] = useState(false);
  const [shortsError, setShortsError] = useState(null);

  // Model & Execution Metadata
  const [modelUsed, setModelUsed] = useState('gemini-3.8-flash');
  const [isCached, setIsCached] = useState(false);

  // AI Prompts for Modal
  const [prompts, setPrompts] = useState({});
  const [isPromptModalOpen, setIsPromptModalOpen] = useState(false);

  // Video Player Ref to trigger seekTo
  const playerRef = useRef(null);
  const abortControllerRef = useRef(null);

  // Load initial niches and sample videos
  useEffect(() => {
    async function loadInitialData() {
      try {
        const [nichesRes, samplesRes] = await Promise.all([
          fetchNiches().catch(() => ({ niches: {} })),
          fetchSamples().catch(() => ({ samples: [] })),
        ]);

        if (nichesRes?.niches) setNiches(nichesRes.niches);
        if (samplesRes?.samples) {
          setSamples(samplesRes.samples);
          // Set initial demo video if URL is empty
          if (samplesRes.samples.length > 0 && !url) {
            setUrl(samplesRes.samples[0].youtube_url);
            setCategory('fitness');
          }
        }
      } catch (err) {
        console.warn('Initial setup fetch error:', err);
      }
    }
    loadInitialData();
  }, []);

  // Cancel in-flight analysis
  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsLoading(false);
    setCurrentStep(0);
  };

  // Main Submit Pipeline (Calls 1 & 2 only)
  const handleAnalyze = async (overrideUrl = null, overrideCategory = null) => {
    const targetUrl = (overrideUrl || url).trim();
    const targetCategory = overrideCategory || category;
    if (!targetUrl) return;

    // Reset previous states
    setError(null);
    setIsLoading(true);
    setCurrentStep(1); // Step 1: Video Ingestion
    setMasterData(null);
    setPanelData(null);
    setShortsData(null);
    setShortsError(null);
    const collectedPrompts = {};

    abortControllerRef.current = new AbortController();
    const { signal } = abortControllerRef.current;

    try {
      // Step 2: Call 1 — Master Analysis
      setCurrentStep(2);
      const res1 = await analyzeVideo({
        youtubeUrl: targetUrl,
        videoDuration,
        category: targetCategory,
        signal,
      });

      if (!res1.success || !res1.data) {
        throw new Error(res1.error || 'Master analysis failed to produce data.');
      }

      setMasterData(res1.data);
      if (res1.model_used) setModelUsed(res1.model_used);
      if (res1.is_cached !== undefined) setIsCached(res1.is_cached);
      if (res1.prompt_used) {
        collectedPrompts.call1 = res1.prompt_used;
      }

      // Step 3: Call 2 — Audience Panel (grounded in summary from Call 1)
      setCurrentStep(3);
      const res2 = await analyzePanel({
        youtubeUrl: targetUrl,
        analysisContext: res1.data.summary,
        videoDuration,
        category: targetCategory,
        signal,
      });

      if (res2.success && res2.data) {
        setPanelData(res2.data);
        if (res2.prompt_used) {
          collectedPrompts.call2 = res2.prompt_used;
        }
      }

      setPrompts(collectedPrompts);
      setCurrentStep(4); // Completed!
    } catch (err) {
      if (err.name === 'AbortError') {
        console.log('Analysis request was aborted by user.');
      } else {
        console.error('Analysis pipeline failed:', err);
        setError(err.message || 'An unexpected error occurred during analysis.');
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  // Instant 1-Click Demo Handler
  const handleSelectSample = (sample) => {
    setUrl(sample.youtube_url);
    setCategory('fitness');
    handleAnalyze(sample.youtube_url, 'fitness');
  };


  // On-Demand Shorts Generation (Call 3)
  const handleGenerateShorts = async () => {
    if (!masterData?.summary) return;
    setIsGeneratingShorts(true);
    setShortsError(null);

    try {
      const res3 = await fetchShorts({
        youtubeUrl: url,
        analysisContext: masterData.summary,
        videoDuration,
        category,
      });

      if (res3.success && res3.data) {
        setShortsData(res3.data);
        if (res3.prompt_used) {
          setPrompts((prev) => ({ ...prev, shorts: res3.prompt_used }));
        }
      } else {
        setShortsError(res3.error || 'Failed to generate Shorts.');
      }
    } catch (err) {
      setShortsError(err.message || 'Shorts extraction failed.');
    } finally {
      setIsGeneratingShorts(false);
    }
  };

  // Handler for timestamp clicks across all insight cards
  const handleSeek = (seconds) => {
    if (playerRef.current && typeof playerRef.current.seekTo === 'function') {
      playerRef.current.seekTo(seconds);
    }
  };

  return (
    <div className="app-container">
      <Header
        onOpenPromptModal={() => setIsPromptModalOpen(true)}
        hasPrompts={Object.keys(prompts).length > 0}
      />

      {/* Hero Video Input */}
      <UrlInput
        url={url}
        setUrl={setUrl}
        category={category}
        setCategory={setCategory}
        niches={niches}
        samples={samples}
        isLoading={isLoading}
        onSubmit={handleAnalyze}
        onCancel={handleCancel}
        onSelectSample={handleSelectSample}
      />


      {/* Progressive Step Tracker & Circular Loader (visible while analyzing) */}
      {isLoading && <ProgressTracker currentStep={currentStep} />}

      {/* Global Error Banner */}
      {error && (
        <div style={{ padding: '1rem 1.5rem', background: 'rgba(244, 63, 94, 0.1)', border: '1px solid var(--rose)', borderRadius: 'var(--radius-lg)', color: 'var(--rose)', marginBottom: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span>⚠️ {error}</span>
          <button
            type="button"
            className="btn btn-outline btn-sm"
            style={{ color: 'var(--rose)', borderColor: 'var(--rose)' }}
            onClick={() => setError(null)}
          >
            Dismiss
          </button>
        </div>
      )}

      {/* 2-Column Responsive Layout */}
      <div className="content-grid">
        {/* Left Column: Embedded Player & Timeline Chapters */}
        <div className="video-column">
          <ErrorBoundary title="Video Player">
            <VideoPlayer
              ref={playerRef}
              url={url}
              onDurationDetected={(dur) => setVideoDuration(dur)}
            />
          </ErrorBoundary>

          {masterData && (
            <ErrorBoundary title="Timeline Moments">
              <MomentCard
                summary={masterData.summary}
                moments={masterData.moments}
                onSeek={handleSeek}
              />
            </ErrorBoundary>
          )}
        </div>

        {/* Right Column: Deep Explainable Feedback Modules */}
        <div className="analysis-column">
          {masterData ? (
            <>
              {/* Feature 4: Content Readiness Score Dashboard */}
              <ErrorBoundary title="Readiness Score">
                <ReadinessScore
                  readinessScore={masterData.readiness_score}
                  scoreFactors={masterData.score_factors}
                  topImprovements={masterData.top_improvements}
                />
              </ErrorBoundary>

              {/* Feature 2: Hook Rubric Assessment */}
              <ErrorBoundary title="Hook Analysis">
                <HookAnalysis
                  hookScore={masterData.hook_score}
                  hookDimensions={masterData.hook_dimensions}
                  onSeek={handleSeek}
                />
              </ErrorBoundary>

              {/* Feature 3: Title & Alternative Comparisons */}
              <ErrorBoundary title="Title Comparison">
                <TitleComparison
                  currentTitleAssessment={masterData.current_title_assessment}
                  titleAlternatives={masterData.title_alternatives}
                  recommendedIndex={masterData.recommended_title_index}
                />
              </ErrorBoundary>

              {/* Feature 5: Simulated Audience Panel & Disagreements */}
              {panelData && (
                <ErrorBoundary title="Audience Panel">
                  <AudiencePanel
                    panelReactions={panelData.panel_reactions}
                    disagreements={panelData.disagreements}
                    onSeek={handleSeek}
                  />
                </ErrorBoundary>
              )}

              {/* Feature 8: YouTube Shorts Candidates (Tier 3 - On-Demand) */}
              <ErrorBoundary title="Shorts Candidates">
                <ShortsClips
                  clips={shortsData}
                  onSeek={handleSeek}
                  onGenerateShorts={handleGenerateShorts}
                  isGenerating={isGeneratingShorts}
                  error={shortsError}
                />
              </ErrorBoundary>

              {/* Feature 7: Multilingual Translation (Tier 3) */}
              <ErrorBoundary title="Multilingual Translation">
                <LanguageTranslate
                  summary={masterData.summary}
                  topImprovements={masterData.top_improvements}
                  titleAlternatives={masterData.title_alternatives}
                />
              </ErrorBoundary>
            </>
          ) : !isLoading ? (
            <div className="section-card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🚀</div>
              <h3 style={{ marginBottom: '0.5rem' }}>Ready to Analyze</h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', maxWidth: '420px', margin: '0 auto' }}>
                Select a 1-click demo sample above or paste any YouTube URL to receive timestamp-linked explainable coaching and simulated audience reactions.
              </p>
            </div>
          ) : null}
        </div>
      </div>

      {/* Inspect AI Prompts & Scoring Modal */}
      {isPromptModalOpen && (
        <InspectReasoningModal
          prompts={prompts}
          modelUsed={modelUsed}
          isCached={isCached}
          onClose={() => setIsPromptModalOpen(false)}
        />
      )}
    </div>
  );
}
