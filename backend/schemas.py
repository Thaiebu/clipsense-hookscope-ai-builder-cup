"""
Pydantic response schemas for the Explainable Video Coach API.
All Gemini responses are validated against these models before returning to the frontend.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional


# ─── Feature 1: Video Understanding & Moment Extraction ─────────────────────

class Moment(BaseModel):
    timestamp_seconds: int = Field(..., ge=0, description="Timestamp in seconds from start of video")
    title: str = Field(..., description="Short title for this moment")
    description: str = Field(..., description="What happens at this moment")


# ─── Feature 2: Hook Analysis ───────────────────────────────────────────────

class HookDimension(BaseModel):
    name: str = Field(..., description="Rubric dimension: Clarity, Curiosity, Pacing, or Payoff Promise")
    score: int = Field(..., ge=0, le=10, description="Score out of 10")
    timestamp_seconds: int = Field(..., ge=0, description="Supporting timestamp")
    observation: str = Field(..., description="What was observed at this timestamp")
    suggestion: str = Field(..., description="Actionable improvement suggestion")

    @model_validator(mode="before")
    @classmethod
    def normalize_dimension(cls, data):
        if isinstance(data, dict):
            if "name" not in data and "dimension" in data:
                data["name"] = data["dimension"]
        return data


# ─── Feature 3: Title Alternatives ──────────────────────────────────────────

class TitleAlternative(BaseModel):
    title: str = Field(..., description="Alternative title suggestion")
    strengths: str = Field(..., description="Why this title works under the rubric")
    weaknesses: str = Field(..., description="Potential downsides of this title")
    rubric_score: int = Field(..., ge=0, le=10, description="Estimated rubric fit score")


# ─── Feature 4: Readiness Score ─────────────────────────────────────────────

class ScoreFactor(BaseModel):
    name: str = Field(..., description="Factor name: Hook Strength, Content Structure, Pacing, Title Fit")
    score: int = Field(..., ge=0, le=25, description="Score out of 25")
    evidence: str = Field(..., description="Key evidence supporting this score")

    @model_validator(mode="before")
    @classmethod
    def normalize_factor(cls, data):
        if isinstance(data, dict):
            if "name" not in data and "factor" in data:
                data["name"] = data["factor"]
            elif "name" not in data and "title" in data:
                data["name"] = data["title"]
        return data


# ─── Master Analysis Response (Gemini Call 1) ───────────────────────────────

class MasterAnalysisResponse(BaseModel):
    """Combined response from Gemini Call 1 — Features 1-4 in one request."""

    # Feature 1: Video summary + moments
    summary: str = Field(..., description="2-3 sentence video summary")
    moments: list[Moment] = Field(..., description="6-10 key moments with timestamps")

    # Feature 2: Hook analysis
    hook_score: float = Field(..., ge=0, le=10, description="Overall hook quality score")
    hook_dimensions: list[HookDimension] = Field(..., description="4 rubric dimension scores with evidence")

    # Feature 3: Title alternatives
    current_title_assessment: str = Field(..., description="Brief assessment of the current title")
    title_alternatives: list[TitleAlternative] = Field(..., description="3 alternative title suggestions")
    recommended_title_index: int = Field(..., ge=0, le=2, description="Index of the best-fit title (0-2)")

    # Feature 4: Readiness score
    readiness_score: int = Field(..., ge=0, le=100, description="Overall content readiness score (0-100)")
    score_factors: list[ScoreFactor] = Field(..., description="4 contributing factors with evidence")
    top_improvements: list[str] = Field(..., description="Top 3 prioritized improvements")

    @field_validator("top_improvements", mode="before")
    @classmethod
    def normalize_improvements(cls, v):
        if not isinstance(v, list):
            return v
        normalized = []
        for item in v:
            if isinstance(item, dict):
                val = (
                    item.get("improvement")
                    or item.get("suggestion")
                    or item.get("text")
                    or item.get("description")
                    or next((str(x) for x in item.values() if isinstance(x, str)), str(item))
                )
                normalized.append(str(val))
            else:
                normalized.append(str(item))
        return normalized


# ─── Feature 5: Audience Panel (Gemini Call 2) ──────────────────────────────

class PersonaReaction(BaseModel):
    timestamp_seconds: int = Field(..., ge=0)
    reaction: str
    sentiment: str = Field(..., description="positive, negative, or neutral")
    suggestion: Optional[str] = Field(None, description="Improvement suggestion if sentiment is negative")


class PanelPersona(BaseModel):
    persona: str = Field(..., description="Name of the persona (e.g., Gym Beginner, Junior Developer, Novice Cook)")
    overall_rating: str = Field(..., description="Overall assessment from this persona's perspective")
    highlights: list[PersonaReaction] = Field(..., description="Positive moments")
    concerns: list[PersonaReaction] = Field(..., description="Negative or unclear moments")


class Disagreement(BaseModel):
    timestamp_seconds: int = Field(..., ge=0)
    topic: str = Field(..., description="What the personas disagree about")
    persona_1: Optional[str] = Field(None, description="Perspective of persona 1")
    persona_2: Optional[str] = Field(None, description="Perspective of persona 2")
    persona_3: Optional[str] = Field(None, description="Perspective of persona 3")
    # Backwards compatibility fields for fitness specific persona names
    beginner: Optional[str] = Field(None, description="Perspective of persona 1 / beginner")
    experienced: Optional[str] = Field(None, description="Perspective of persona 2 / experienced")
    home_viewer: Optional[str] = Field(None, description="Perspective of persona 3 / practical")


class AudiencePanelResponse(BaseModel):
    """Response from Gemini Call 2 — 3-persona audience panel."""
    panel_reactions: list[PanelPersona] = Field(..., description="Reactions from each persona")
    disagreements: list[Disagreement] = Field(..., description="Moments where personas disagree")


# ─── API Request Models ─────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    youtube_url: str = Field(..., description="Full YouTube URL to analyze")
    video_duration: Optional[int] = Field(None, ge=0, description="Video duration in seconds from frontend player")
    category: Optional[str] = Field("fitness", description="Video niche/category: 'fitness', 'tech', 'cooking', 'education', or 'general'")


class PanelRequest(BaseModel):
    youtube_url: str = Field(..., description="Same YouTube URL")
    analysis_context: Optional[str] = Field(None, description="Summary from Call 1 (optional, will use default context if omitted)")
    video_duration: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field("fitness", description="Video niche/category: 'fitness', 'tech', 'cooking', 'education', or 'general'")


# ─── API Response Wrappers ──────────────────────────────────────────────────

class AnalyzeResponse(BaseModel):
    success: bool
    data: Optional[MasterAnalysisResponse] = None
    error: Optional[str] = None
    prompt_used: Optional[str] = Field(None, description="The prompt sent to Gemini (for Inspect AI Reasoning modal)")


class PanelResponse(BaseModel):
    success: bool
    data: Optional[AudiencePanelResponse] = None
    error: Optional[str] = None
    prompt_used: Optional[str] = None


# ─── Feature 7: Multilingual Feedback (Tier 3) ──────────────────────────────

class TranslateRequest(BaseModel):
    target_language: str = Field(..., description="Target language code or name, e.g., 'hi' (Hindi), 'ja' (Japanese), 'es' (Spanish), 'de' (German)")
    summary: str = Field(..., description="English summary to translate")
    top_improvements: list[str] = Field(..., description="Key improvement recommendations to translate")
    title_alternatives: Optional[list[str]] = Field(default_factory=list, description="Title suggestions to translate")


class TranslatedData(BaseModel):
    target_language: str
    translated_summary: str
    translated_improvements: list[str]
    translated_titles: list[str] = Field(default_factory=list)


class TranslateResponse(BaseModel):
    success: bool
    data: Optional[TranslatedData] = None
    error: Optional[str] = None


# ─── Feature 8: YouTube Shorts Clip Suggestions (Tier 3) ────────────────────

class ShortsClip(BaseModel):
    start_seconds: int = Field(..., ge=0, description="Start timestamp in seconds")
    end_seconds: int = Field(..., ge=0, description="End timestamp in seconds")
    duration_seconds: int = Field(..., ge=5, le=60, description="Duration in seconds (strictly <60s)")
    title: str = Field(..., description="Punchy, click-worthy Shorts clip title")
    hook_caption: str = Field(..., description="On-screen text caption for the first 3 seconds of the Short")
    reason_standalone: str = Field(..., description="Why this exact segment works as an independent viral Short")


class ShortsRequest(BaseModel):
    youtube_url: str = Field(..., description="Same YouTube URL")
    analysis_context: Optional[str] = Field(None, description="Video summary or key moments context")
    video_duration: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field("fitness", description="Video niche/category")


class ShortsResponse(BaseModel):
    success: bool
    data: Optional[list[ShortsClip]] = None
    error: Optional[str] = None
    prompt_used: Optional[str] = None
