"""
Explainable Video Coach — FastAPI Backend
AI Builder Cup 2026

Routes:
- GET  /              : Service information
- GET  /api/health    : Health check for Cloud Run
- GET  /api/niches    : Available categories & simulated personas
- GET  /api/samples   : Curated sample videos for instant demo
- POST /api/analyze   : Gemini Call 1 (Master Analysis: Moments + Hook + Titles + Readiness)
- POST /api/panel     : Gemini Call 2 (Simulated Audience Panel + Disagreements)
"""

import logging
import os
import time
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from gemini_service import (
    analyze_audience_panel,
    analyze_video,
    generate_shorts_clips,
    translate_feedback,
)
from niches import NICHE_CONFIGS
from sample_data import SAMPLE_VIDEOS
from schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    PanelRequest,
    PanelResponse,
    ShortsRequest,
    ShortsResponse,
    TranslateRequest,
    TranslateResponse,
)

from pathlib import Path
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
load_dotenv(override=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("video_coach.api")

app = FastAPI(
    title="Explainable Video Coach API",
    description="Multi-niche video feedback & simulated audience panel powered by Gemini 2.5 Pro",
    version="1.1.0",
)

# ─── CORS Middleware ──────────────────────────────────────────────────────────
raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if "*" not in allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── In-Flight Request Deduplication ──────────────────────────────────────────
active_requests: dict[str, float] = {}
REQUEST_TIMEOUT_SECONDS = 180.0


def check_and_set_inflight(key: str):
    now = time.time()
    stale_keys = [k for k, start_time in active_requests.items() if now - start_time > REQUEST_TIMEOUT_SECONDS]
    for k in stale_keys:
        active_requests.pop(k, None)

    if key in active_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="An analysis for this video is already in progress. Please wait.",
        )
    active_requests[key] = now


def release_inflight(key: str):
    active_requests.pop(key, None)


# ─── Sliding Window IP Rate Limiter ──────────────────────────────────────────
ip_request_history: dict[str, list[float]] = {}
RATE_LIMIT_WINDOW_SECONDS = 60.0
MAX_REQUESTS_PER_WINDOW = 25  # Max 25 requests per minute per IP


def enforce_ip_rate_limit(request: Request):
    """
    Enforces sliding-window rate limit per client IP (25 requests per 60 seconds).
    Extracts IP from X-Forwarded-For if behind a reverse proxy/Cloud Run.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    elif request.client and request.client.host:
        client_ip = request.client.host
    else:
        client_ip = "127.0.0.1"

    now = time.time()
    cutoff = now - RATE_LIMIT_WINDOW_SECONDS

    # Prune old timestamps
    timestamps = [t for t in ip_request_history.get(client_ip, []) if t > cutoff]

    if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
        retry_after = int(RATE_LIMIT_WINDOW_SECONDS - (now - timestamps[0])) + 1
        logger.warning(f"Rate limit exceeded for client IP: {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded (max {MAX_REQUESTS_PER_WINDOW} req/min). Please wait {retry_after}s before trying again.",
            headers={"Retry-After": str(max(1, retry_after))},
        )

    timestamps.append(now)
    ip_request_history[client_ip] = timestamps


def is_response_cached(youtube_url: str) -> bool:
    """Helper to detect if response was served from pre-cached benchmark samples."""
    from sample_data import get_sample_by_id_or_url
    from gemini_service import get_gemini_client
    if os.getenv("USE_SAMPLE_CACHE_ONLY", "false").lower() == "true":
        return True
    if get_gemini_client() is None and get_sample_by_id_or_url(youtube_url):
        return True
    return False


# ─── Security: API Key Verification ──────────────────────────────────────────
EXPECTED_API_KEY = os.getenv("API_KEY")


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Validate X-API-Key header if API_KEY is set in environment.
    If API_KEY is not configured, bypasses check for simple local development.
    """
    if not EXPECTED_API_KEY:
        return True
    if not x_api_key or x_api_key != EXPECTED_API_KEY:
        logger.warning("Unauthorized access attempt: invalid or missing X-API-Key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return True



# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "service": "Explainable Video Coach API",
        "status": "online",
        "version": "1.1.0",
        "supported_niches": list(NICHE_CONFIGS.keys()),
        "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "model": os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
    }


@app.get("/api/niches")
def list_niches():
    """
    Returns available categories/niches and their 3 defined audience personas.
    Used by the frontend category dropdown.
    """
    result = {}
    for key, val in NICHE_CONFIGS.items():
        result[key] = {
            "key": key,
            "display_name": val["display_name"],
            "description": val["description"],
            "personas": [p["name"] for p in val["personas"]],
        }
    return {"niches": result}


@app.get("/api/samples")
def list_samples(category: Optional[str] = Query(None, description="Optional category filter")):
    """
    Returns curated sample videos for the frontend 'Try Example' buttons.
    Allows judges and users to immediately demo the app with zero typing.
    """
    samples = []
    for key, item in SAMPLE_VIDEOS.items():
        if category and category.lower() not in item.get("category", "").lower():
            continue
        samples.append({
            "id": item["id"],
            "title": item["title"],
            "youtube_url": item["youtube_url"],
            "duration": item["duration"],
            "category": item["category"],
        })
    return {"samples": samples}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(payload: AnalyzeRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    """
    Gemini Call 1: Runs comprehensive Master Analysis covering:
    - Summary & key extracted moments with timestamps
    - Hook evaluation across 4 rubric dimensions
    - 3 alternative title suggestions with rubric evaluation
    - Content readiness score (0-100) and top improvements
    - Supports dynamic category selection (fitness, tech, cooking, education, general)
    """
    verify_api_key(x_api_key)
    enforce_ip_rate_limit(request)

    url = payload.youtube_url.strip()
    if not url:
        return AnalyzeResponse(
            success=False,
            error="Please provide a valid YouTube URL",
        )

    dedup_key = f"analyze:{url}"
    check_and_set_inflight(dedup_key)

    try:
        category_name = payload.category or "fitness"
        logger.info(f"Starting master analysis for: {url} (niche={category_name})")
        data, prompt_used, error_msg = analyze_video(
            youtube_url=url,
            video_duration=payload.video_duration,
            category=category_name,
        )

        cached_status = is_response_cached(url)

        if error_msg or data is None:
            logger.error(f"Analysis failed for {url}: {error_msg}")
            return AnalyzeResponse(
                success=False,
                error=error_msg or "Video analysis could not be completed.",
                prompt_used=prompt_used,
                model_used="gemini-3.8-flash",
                is_cached=cached_status,
            )

        logger.info(f"Master analysis completed successfully for: {url}")
        return AnalyzeResponse(
            success=True,
            data=data,
            prompt_used=prompt_used,
            model_used="gemini-3.8-flash",
            is_cached=cached_status,
        )
    finally:
        release_inflight(dedup_key)


@app.post("/api/panel", response_model=PanelResponse)
def audience_panel_endpoint(payload: PanelRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    """
    Gemini Call 2: Runs Simulated Audience Panel:
    - 3 Personas tailored to the chosen category
    - Highlights (positive) and concerns (constructive) per persona
    - Disagreement matrix highlighting trade-offs between audiences
    """
    verify_api_key(x_api_key)
    enforce_ip_rate_limit(request)

    url = payload.youtube_url.strip()
    if not url:
        return PanelResponse(
            success=False,
            error="Please provide a valid YouTube URL",
        )

    dedup_key = f"panel:{url}"
    check_and_set_inflight(dedup_key)

    try:
        category_name = payload.category or "fitness"
        logger.info(f"Starting audience panel analysis for: {url} (niche={category_name})")
        data, prompt_used, error_msg = analyze_audience_panel(
            youtube_url=url,
            analysis_context=payload.analysis_context,
            video_duration=payload.video_duration,
            category=category_name,
        )

        cached_status = is_response_cached(url)

        if error_msg or data is None:
            logger.error(f"Audience panel failed for {url}: {error_msg}")
            return PanelResponse(
                success=False,
                error=error_msg or "Audience panel simulation failed.",
                prompt_used=prompt_used,
                model_used="gemini-3.8-flash",
                is_cached=cached_status,
            )

        logger.info(f"Audience panel completed successfully for: {url}")
        return PanelResponse(
            success=True,
            data=data,
            prompt_used=prompt_used,
            model_used="gemini-3.8-flash",
            is_cached=cached_status,
        )
    finally:
        release_inflight(dedup_key)


@app.post("/api/shorts", response_model=ShortsResponse)
def shorts_endpoint(payload: ShortsRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    """
    Feature 8 (Tier 3): YouTube Shorts Clip Suggestions.
    Identifies 2-3 viral-worthy segments (<60s) with hook captions and rationale.
    """
    verify_api_key(x_api_key)
    enforce_ip_rate_limit(request)

    url = payload.youtube_url.strip()
    if not url:
        return ShortsResponse(
            success=False,
            error="Please provide a valid YouTube URL",
        )

    dedup_key = f"shorts:{url}"
    check_and_set_inflight(dedup_key)

    try:
        category_name = payload.category or "fitness"
        logger.info(f"Starting Shorts clip generation for: {url} (niche={category_name})")
        clips, prompt_used, error_msg = generate_shorts_clips(
            youtube_url=url,
            analysis_context=payload.analysis_context,
            video_duration=payload.video_duration,
            category=category_name,
        )

        cached_status = is_response_cached(url)

        if error_msg or clips is None:
            logger.error(f"Shorts generation failed for {url}: {error_msg}")
            return ShortsResponse(
                success=False,
                error=error_msg or "Failed to generate Shorts clips.",
                prompt_used=prompt_used,
                model_used="gemini-3.8-flash",
                is_cached=cached_status,
            )

        logger.info(f"Shorts clips generated successfully for: {url} ({len(clips)} clips)")
        return ShortsResponse(
            success=True,
            data=clips,
            prompt_used=prompt_used,
            model_used="gemini-3.8-flash",
            is_cached=cached_status,
        )
    finally:
        release_inflight(dedup_key)


@app.post("/api/translate", response_model=TranslateResponse)
def translate_endpoint(payload: TranslateRequest, request: Request, x_api_key: Optional[str] = Header(None)):
    """
    Feature 7 (Tier 3): Multilingual Feedback Translation.
    Translates English summary, improvements, and title alternatives to target language (e.g. Tamil, Hindi, Japanese, Spanish).
    """
    verify_api_key(x_api_key)
    enforce_ip_rate_limit(request)


    lang = payload.target_language.strip()
    if not lang:
        return TranslateResponse(
            success=False,
            error="Please specify a target language (e.g., 'hi' for Hindi, 'ja' for Japanese)",
        )

    logger.info(f"Translating video feedback into: {lang}")
    translated, error_msg = translate_feedback(
        target_language=lang,
        summary=payload.summary,
        top_improvements=payload.top_improvements,
        title_alternatives=payload.title_alternatives,
    )

    if error_msg or translated is None:
        logger.error(f"Translation failed: {error_msg}")
        return TranslateResponse(
            success=False,
            error=error_msg or "Translation service failed.",
        )

    return TranslateResponse(
        success=True,
        data=translated,
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
