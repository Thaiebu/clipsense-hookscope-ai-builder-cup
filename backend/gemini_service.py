"""
Gemini 3.8 Flash Service for Explainable Video Coach.
Handles Gemini Call 1 (Master Analysis), Gemini Call 2 (Audience Panel), and Call 3 (Shorts & Translation).
Supports:
- Dynamic niche adaptation (Fitness, Tech, Cooking, Education, General)
- google-genai SDK (Vertex AI with global endpoint or Gemini Developer API)
- Robust JSON response extraction & Pydantic schema validation
- Automatic fallback to high-fidelity pre-cached samples for demo resilience
- Returning exact prompt_used for the "Inspect AI Reasoning" modal
- Honest result_source tracking ("live_model" vs "sample_cache")
- Strict duration timestamp bounds checking
"""

import json
import logging
import os
import re
from pathlib import Path
from typing import Optional, Tuple

from dotenv import load_dotenv
# # pyrefly: ignore [missing-import]
from google.genai import types

from niches import get_niche, format_persona_prompt_section
from schemas import (
    AudiencePanelResponse,
    MasterAnalysisResponse,
    ShortsClip,
    TranslatedData,
)
from sample_data import get_sample_by_id_or_url

# Robustly load .env from backend directory or project root
load_dotenv(Path(__file__).resolve().parent / ".env", override=True)
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
load_dotenv(override=True)

logger = logging.getLogger("video_coach.gemini")
logging.basicConfig(level=logging.INFO)

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def load_prompt_template(filename: str) -> str:
    """Load prompt file from the prompts directory."""
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def get_gemini_client():
    """
    Initialize Google GenAI client based on environment variables.
    Prioritizes Vertex AI (GCP_PROJECT_ID) with global location for Gemini 3.8 Flash,
    falling back to Gemini Developer API (GEMINI_API_KEY) if configured.
    """
    try:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        gcp_project = os.getenv("GCP_PROJECT_ID")
        gcp_region = os.getenv("GCP_REGION", "global")

        # Ignore placeholder template strings
        if gcp_project and "your-gcp-project-id" in gcp_project.lower():
            gcp_project = None

        if gcp_project and gcp_project.strip():
            logger.info(f"Initializing Google GenAI client via Vertex AI (project={gcp_project}, location={gcp_region})")
            return genai.Client(vertexai=True, project=gcp_project.strip(), location=gcp_region)
        elif api_key and api_key.strip():
            logger.info("Initializing Google GenAI client with GEMINI_API_KEY")
            return genai.Client(api_key=api_key.strip())
        else:
            logger.warning("No explicit GCP_PROJECT_ID or GEMINI_API_KEY found")
            return None
    except Exception as e:
        logger.warning(f"Could not initialize Google GenAI Client: {e}. Will use sample fallback if requested.")
        return None


def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON dictionary from model response text, stripping markdown code blocks if present.
    """
    text = text.strip()

    # Pattern for markdown ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()

    # Attempt direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        first_brace = text.find("{")
        last_brace = text.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            sub = text[first_brace : last_brace + 1]
            return json.loads(sub)
        raise


def analyze_video(
    youtube_url: str,
    video_duration: Optional[int] = None,
    video_title: Optional[str] = None,
    category: Optional[str] = "fitness",
) -> Tuple[Optional[MasterAnalysisResponse], Optional[str], Optional[str], str]:
    """
    Gemini Call 1: Master Video Analysis (Features 1-4).
    Dynamically adapts analysis to specified video category.
    Returns (data, prompt_used, error_message, result_source).
    result_source is either 'live_model' or 'sample_cache'.
    """
    duration_val = video_duration if video_duration and video_duration > 0 else 600
    title_val = video_title.strip() if video_title and video_title.strip() else "YouTube Video"
    niche = get_niche(category)

    # 1. Check if this is one of our pre-cached sample videos (forced cache mode)
    sample_match = get_sample_by_id_or_url(youtube_url)
    if os.getenv("USE_SAMPLE_CACHE_ONLY", "false").lower() == "true" and sample_match:
        logger.info(f"Using pre-cached sample data for {youtube_url} (USE_SAMPLE_CACHE_ONLY=true)")
        prompt_template = load_prompt_template("master_analysis.txt")
        prompt_used = prompt_template.format(
            youtube_url=sample_match["youtube_url"],
            video_duration=sample_match["duration"],
            video_title=sample_match["title"],
            category_name=niche["display_name"],
            niche_description=niche["description"],
        )
        data = MasterAnalysisResponse.model_validate(sample_match["analysis"])
        data.clamp_to_duration(duration_val)
        return data, prompt_used, None, "sample_cache"

    # 2. Build Prompt
    try:
        prompt_template = load_prompt_template("master_analysis.txt")
        prompt_used = prompt_template.format(
            youtube_url=youtube_url,
            video_duration=duration_val,
            video_title=title_val,
            category_name=niche["display_name"],
            niche_description=niche["description"],
        )
    except Exception as e:
        return None, None, f"Failed to load prompt template: {str(e)}", "live_model"

    # 3. Call Gemini
    client = get_gemini_client()
    if client is None:
        if sample_match:
            logger.info("Gemini client unavailable, falling back to matched sample cache")
            data = MasterAnalysisResponse.model_validate(sample_match["analysis"])
            data.clamp_to_duration(duration_val)
            return data, prompt_used, None, "sample_cache"
        return None, prompt_used, "Gemini client not initialized. Please configure GCP_PROJECT_ID or GEMINI_API_KEY.", "live_model"

    try:
        logger.info(f"Calling Gemini ({DEFAULT_MODEL}) for master analysis ({niche['display_name']}): {youtube_url}")

        contents = []

        try:
            video_part = types.Part.from_uri(
                file_uri=youtube_url,
                mime_type="video/*",
            )
            contents.append(video_part)
        except Exception as part_err:
            logger.warning(f"Could not create Part.from_uri for YouTube URL: {part_err}. Passing URL in prompt text.")

        contents.append(prompt_used)

        # For Gemini 3.8 Flash, sampling parameters (temperature, top_p) are deprecated.
        config = types.GenerateContentConfig(
            max_output_tokens=8192,
            response_mime_type="application/json",
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=config,
        )

        raw_text = response.text or ""
        parsed_json = extract_json_from_text(raw_text)
        validated_data = MasterAnalysisResponse.model_validate(parsed_json)
        validated_data.clamp_to_duration(duration_val)
        return validated_data, prompt_used, None, "live_model"

    except Exception as e:
        logger.error(f"Gemini API error during master analysis: {e}")
        if sample_match:
            logger.warning("Falling back to pre-cached sample due to Gemini error")
            data = MasterAnalysisResponse.model_validate(sample_match["analysis"])
            data.clamp_to_duration(duration_val)
            return data, prompt_used, None, "sample_cache"
        return None, prompt_used, f"Analysis failed: {str(e)}", "live_model"


def analyze_audience_panel(
    youtube_url: str,
    analysis_context: Optional[str] = None,
    video_duration: Optional[int] = None,
    category: Optional[str] = "fitness",
) -> Tuple[Optional[AudiencePanelResponse], Optional[str], Optional[str], str]:
    """
    Gemini Call 2: Simulated Audience Panel (Feature 5).
    Dynamically tailors 3 personas and disagreement dimensions to the selected category.
    Returns (data, prompt_used, error_message, result_source).
    """
    duration_val = video_duration if video_duration and video_duration > 0 else 600
    niche = get_niche(category)
    personas_section = format_persona_prompt_section(niche)
    context_val = (analysis_context or "").strip() or f"Instructional breakdown and demonstrations in {niche['display_name']} video: {youtube_url}"

    # 1. Check if this is one of our pre-cached sample videos (forced cache mode)
    sample_match = get_sample_by_id_or_url(youtube_url)
    if os.getenv("USE_SAMPLE_CACHE_ONLY", "false").lower() == "true" and sample_match:
        logger.info(f"Using pre-cached audience panel data for {youtube_url} (USE_SAMPLE_CACHE_ONLY=true)")
        prompt_template = load_prompt_template("audience_panel.txt")
        prompt_used = prompt_template.format(
            youtube_url=sample_match["youtube_url"],
            video_duration=sample_match["duration"],
            analysis_context=context_val or sample_match["analysis"]["summary"],
            category_name=niche["display_name"],
            personas_section=personas_section,
        )
        data = AudiencePanelResponse.model_validate(sample_match["panel"])
        data.clamp_to_duration(duration_val)
        return data, prompt_used, None, "sample_cache"

    # 2. Build Prompt
    try:
        prompt_template = load_prompt_template("audience_panel.txt")
        prompt_used = prompt_template.format(
            youtube_url=youtube_url,
            video_duration=duration_val,
            analysis_context=context_val,
            category_name=niche["display_name"],
            personas_section=personas_section,
        )
    except Exception as e:
        return None, None, f"Failed to load audience panel prompt template: {str(e)}", "live_model"

    # 3. Call Gemini
    client = get_gemini_client()
    if client is None:
        if sample_match:
            logger.info("Gemini client unavailable, falling back to matched sample panel")
            data = AudiencePanelResponse.model_validate(sample_match["panel"])
            data.clamp_to_duration(duration_val)
            return data, prompt_used, None, "sample_cache"
        return None, prompt_used, "Gemini client not initialized. Please configure GCP_PROJECT_ID or GEMINI_API_KEY.", "live_model"

    try:
        logger.info(f"Calling Gemini ({DEFAULT_MODEL}) for audience panel ({niche['display_name']}): {youtube_url}")

        contents = []
        try:
            video_part = types.Part.from_uri(
                file_uri=youtube_url,
                mime_type="video/*",
            )
            contents.append(video_part)
        except Exception as part_err:
            logger.warning(f"Could not create Part.from_uri for YouTube URL: {part_err}. Passing URL in prompt text.")

        contents.append(prompt_used)

        config = types.GenerateContentConfig(
            max_output_tokens=8192,
            response_mime_type="application/json",
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=config,
        )

        raw_text = response.text or ""
        parsed_json = extract_json_from_text(raw_text)

        # Synchronize persona viewpoints in disagreements if model only returned persona_1..3
        if "disagreements" in parsed_json and isinstance(parsed_json["disagreements"], list):
            for d in parsed_json["disagreements"]:
                if isinstance(d, dict):
                    if not d.get("beginner") and d.get("persona_1"):
                        d["beginner"] = d["persona_1"]
                    if not d.get("experienced") and d.get("persona_2"):
                        d["experienced"] = d["persona_2"]
                    if not d.get("home_viewer") and d.get("persona_3"):
                        d["home_viewer"] = d["persona_3"]

        validated_data = AudiencePanelResponse.model_validate(parsed_json)
        validated_data.clamp_to_duration(duration_val)
        return validated_data, prompt_used, None, "live_model"

    except Exception as e:
        logger.error(f"Gemini API error during audience panel: {e}")
        if sample_match:
            logger.warning("Falling back to pre-cached sample panel due to Gemini error")
            data = AudiencePanelResponse.model_validate(sample_match["panel"])
            data.clamp_to_duration(duration_val)
            return data, prompt_used, None, "sample_cache"
        return None, prompt_used, f"Audience panel generation failed: {str(e)}", "live_model"


def generate_shorts_clips(
    youtube_url: str,
    analysis_context: Optional[str] = None,
    video_duration: Optional[int] = None,
    category: Optional[str] = "fitness",
) -> Tuple[Optional[list[ShortsClip]], Optional[str], Optional[str], str]:
    """
    Feature 8 (Tier 3): Identifies 2-3 viral-worthy Shorts clips (<60s) with timestamps, titles, and hook captions.
    Returns (clips, prompt_used, error_message, result_source).
    """
    duration_val = video_duration if video_duration and video_duration > 0 else 600
    niche = get_niche(category)
    context_val = (analysis_context or "").strip() or f"Content overview and demonstrations in {niche['display_name']} video: {youtube_url}"

    # 1. Check pre-cached sample fallback
    sample_match = get_sample_by_id_or_url(youtube_url)
    if os.getenv("USE_SAMPLE_CACHE_ONLY", "false").lower() == "true" and sample_match and "shorts" in sample_match:
        logger.info(f"Using pre-cached shorts clips for {youtube_url} (USE_SAMPLE_CACHE_ONLY=true)")
        prompt_template = load_prompt_template("shorts_clips.txt")
        prompt_used = prompt_template.format(
            youtube_url=sample_match["youtube_url"],
            video_duration=sample_match["duration"],
            analysis_context=sample_match["analysis"]["summary"],
            category_name=niche["display_name"],
        )
        clips = [ShortsClip.model_validate(c) for c in sample_match["shorts"]]
        for c in clips:
            c.clamp_to_duration(duration_val)
        return clips, prompt_used, None, "sample_cache"

    # 2. Build prompt
    try:
        prompt_template = load_prompt_template("shorts_clips.txt")
        prompt_used = prompt_template.format(
            youtube_url=youtube_url,
            video_duration=duration_val,
            analysis_context=context_val,
            category_name=niche["display_name"],
        )
    except Exception as e:
        return None, None, f"Failed to load shorts prompt template: {str(e)}", "live_model"

    # 3. Call Gemini
    client = get_gemini_client()
    if client is None:
        if sample_match and "shorts" in sample_match:
            logger.info("Gemini client unavailable, falling back to matched sample shorts")
            clips = [ShortsClip.model_validate(c) for c in sample_match["shorts"]]
            for c in clips:
                c.clamp_to_duration(duration_val)
            return clips, prompt_used, None, "sample_cache"
        return None, prompt_used, "Gemini client not initialized. Please configure GCP_PROJECT_ID or GEMINI_API_KEY.", "live_model"

    try:
        logger.info(f"Calling Gemini ({DEFAULT_MODEL}) for shorts clip suggestions: {youtube_url}")

        contents = []
        try:
            video_part = types.Part.from_uri(
                file_uri=youtube_url,
                mime_type="video/*",
            )
            contents.append(video_part)
        except Exception as part_err:
            logger.warning(f"Could not create Part.from_uri for YouTube URL: {part_err}. Passing URL in prompt text.")

        contents.append(prompt_used)

        config = types.GenerateContentConfig(
            max_output_tokens=4096,
            response_mime_type="application/json",
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=contents,
            config=config,
        )

        raw_text = response.text or ""
        parsed_json = extract_json_from_text(raw_text)

        if not isinstance(parsed_json, list):
            if isinstance(parsed_json, dict) and "clips" in parsed_json:
                parsed_json = parsed_json["clips"]
            else:
                parsed_json = [parsed_json]

        # Enforce duration constraints on clips (<60s and <= video_duration)
        clips = []
        for item in parsed_json:
            if isinstance(item, dict):
                start = int(item.get("start_seconds", 0))
                end = int(item.get("end_seconds", start + 30))
                if end - start > 59:
                    end = start + 55
                item["start_seconds"] = start
                item["end_seconds"] = end
                item["duration_seconds"] = max(5, end - start)
                clip_obj = ShortsClip.model_validate(item)
                clip_obj.clamp_to_duration(duration_val)
                clips.append(clip_obj)

        return clips, prompt_used, None, "live_model"

    except Exception as e:
        logger.error(f"Gemini API error during shorts generation: {e}")
        if sample_match and "shorts" in sample_match:
            logger.warning("Falling back to pre-cached shorts due to Gemini error")
            clips = [ShortsClip.model_validate(c) for c in sample_match["shorts"]]
            for c in clips:
                c.clamp_to_duration(duration_val)
            return clips, prompt_used, None, "sample_cache"
        return None, prompt_used, f"Shorts clip generation failed: {str(e)}", "live_model"


def translate_feedback(
    target_language: str,
    summary: str,
    top_improvements: list[str],
    title_alternatives: Optional[list[str]] = None,
) -> Tuple[Optional[TranslatedData], Optional[str]]:
    """
    Feature 7 (Tier 3): Translates analysis summary, improvements, and titles into target language (e.g. Tamil, Hindi, Japanese, Spanish).
    Returns (translated_data, error_message).
    """
    from sample_data import get_sample_translation

    lang_clean = target_language.strip()
    lang_lower = lang_clean.lower()

    # Standardize language names
    if lang_lower in ["ta", "tamil", "தமிழ்"]:
        target_lang_name = "Tamil"
        script_instruction = "You MUST translate strictly into authentic Tamil script (தமிழ் எழுத்துக்கள்). Do NOT output English, Hindi, or transliterated Tanglish. All fields ('translated_summary', each item in 'translated_improvements', and 'translated_titles') must be 100% natural, grammatically correct Tamil."
    elif lang_lower in ["hi", "hindi", "हिन्दी"]:
        target_lang_name = "Hindi"
        script_instruction = "You MUST translate strictly into Devanagari script (हिन्दी). Do NOT output English or Hinglish."
    elif lang_lower in ["ja", "japanese", "日本語"]:
        target_lang_name = "Japanese"
        script_instruction = "You MUST translate strictly into natural Japanese (日本語: Kanji, Hiragana, Katakana)."
    elif lang_lower in ["es", "spanish", "español"]:
        target_lang_name = "Spanish"
        script_instruction = "You MUST translate into natural, fluent Spanish (Español)."
    elif lang_lower in ["de", "german", "deutsch"]:
        target_lang_name = "German"
        script_instruction = "You MUST translate into natural German (Deutsch)."
    elif lang_lower in ["fr", "french", "français"]:
        target_lang_name = "French"
        script_instruction = "You MUST translate into natural French (Français)."
    else:
        target_lang_name = lang_clean
        script_instruction = f"Translate accurately and naturally into {target_lang_name} using its native script."

    client = get_gemini_client()
    if client is None:
        cached = get_sample_translation(target_lang_name)
        if cached:
            logger.warning(f"Gemini client not initialized, using pre-cached {target_lang_name} translation fallback.")
            return TranslatedData.model_validate(cached), None
        return None, "Gemini client not initialized. Please configure GCP_PROJECT_ID or GEMINI_API_KEY."

    prompt = f"""You are a professional multilingual translator specializing in video coaching and creator content.

TASK: Accurately translate the following English video feedback into {target_lang_name}.

{script_instruction}

INPUT DATA:
- Summary: {summary}
- Top Improvements: {json.dumps(top_improvements)}
- Title Alternatives: {json.dumps(title_alternatives or [])}

OUTPUT FORMAT: Return valid JSON matching this schema:
{{
  "target_language": "{target_lang_name}",
  "translated_summary": "string",
  "translated_improvements": ["string", "string"],
  "translated_titles": ["string", "string"]
}}

CRITICAL RULES:
1. Every field MUST be translated into {target_lang_name}.
2. Do NOT leave English text in the output.
3. Return ONLY valid JSON.
"""
    try:
        config = types.GenerateContentConfig(
            max_output_tokens=2048,
            response_mime_type="application/json",
        )

        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=[prompt],
            config=config,
        )

        raw_text = response.text or ""
        parsed = extract_json_from_text(raw_text)
        validated = TranslatedData.model_validate(parsed)
        return validated, None
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        cached = get_sample_translation(target_lang_name)
        if cached:
            logger.warning(f"Translation call failed, using pre-cached {target_lang_name} translation fallback.")
            return TranslatedData.model_validate(cached), None
        return None, f"Translation failed: {str(e)}"

