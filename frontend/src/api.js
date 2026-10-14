/**
 * API client for Explainable Video Coach (HookScope)
 * Handles communication with the FastAPI backend on Google Cloud Run.
 */

const API_BASE = import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : '';
const API_KEY = import.meta.env.VITE_API_KEY || '';

/**
 * Helper for making authenticated requests to the backend.
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
    ...(options.headers || {}),
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorDetail = `Request failed with status ${response.status}`;
      try {
        const errorJson = await response.json();
        errorDetail = errorJson.detail || errorJson.error || errorDetail;
      } catch {
        // use default errorDetail
      }
      throw new Error(errorDetail);
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw error;
    }
    console.error(`API Error on [${options.method || 'GET'} ${endpoint}]:`, error);
    throw error;
  }
}

/**
 * Fetch supported niches and their simulated personas.
 */
export async function fetchNiches() {
  return request('/api/niches');
}

/**
 * Fetch pre-cached sample videos for instant demo buttons.
 */
export async function fetchSamples(category = null) {
  const query = category ? `?category=${encodeURIComponent(category)}` : '';
  return request(`/api/samples${query}`);
}

/**
 * Call 1: Master Video Analysis (Summary, Moments, Hook Rubric, Titles, Readiness).
 */
export async function analyzeVideo({ youtubeUrl, videoDuration, category = 'fitness', signal }) {
  return request('/api/analyze', {
    method: 'POST',
    signal,
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      video_duration: videoDuration || 0,
      category,
    }),
  });
}

/**
 * Call 2: Simulated Audience Panel (3 Personas + Disagreements Matrix).
 */
export async function analyzePanel({ youtubeUrl, analysisContext, videoDuration, category = 'fitness', signal }) {
  return request('/api/panel', {
    method: 'POST',
    signal,
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      analysis_context: analysisContext || '',
      video_duration: videoDuration || 0,
      category,
    }),
  });
}

/**
 * Tier 3: YouTube Shorts Clip Suggestions (<60s clips with hook captions).
 */
export async function fetchShorts({ youtubeUrl, analysisContext, videoDuration, category = 'fitness', signal }) {
  return request('/api/shorts', {
    method: 'POST',
    signal,
    body: JSON.stringify({
      youtube_url: youtubeUrl,
      analysis_context: analysisContext || '',
      video_duration: videoDuration || 0,
      category,
    }),
  });
}

/**
 * Tier 3: Multilingual Feedback Translation.
 */
export async function translateFeedback({ targetLanguage, summary, topImprovements, titleAlternatives, signal }) {
  return request('/api/translate', {
    method: 'POST',
    signal,
    body: JSON.stringify({
      target_language: targetLanguage,
      summary,
      top_improvements: topImprovements,
      title_alternatives: titleAlternatives || [],
    }),
  });
}
