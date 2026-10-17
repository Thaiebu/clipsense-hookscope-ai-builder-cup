"""
Comprehensive automated tests for Explainable Video Coach Backend.
Tests all endpoints:
- GET  /
- GET  /api/health
- GET  /api/niches   (Dynamic categories)
- GET  /api/samples
- POST /api/analyze (Call 1 with dynamic category)
- POST /api/panel   (Call 2 with dynamic category)
- API Key authentication & X-API-Key header handling
- Schema validation
"""

import os
import unittest
from fastapi.testclient import TestClient

# Ensure test uses sample cache fallback
os.environ["USE_SAMPLE_CACHE_ONLY"] = "true"

from main import app
from schemas import MasterAnalysisResponse, AudiencePanelResponse


class TestBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("service", data)
        self.assertIn("supported_niches", data)

    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("timestamp", data)

    def test_list_niches(self):
        response = self.client.get("/api/niches")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("niches", data)
        niches = data["niches"]
        for expected in ["fitness", "tech", "cooking", "education", "general"]:
            self.assertIn(expected, niches)
            self.assertIn("display_name", niches[expected])
            self.assertEqual(len(niches[expected]["personas"]), 3)

    def test_list_samples(self):
        response = self.client.get("/api/samples")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("samples", data)
        self.assertEqual(len(data["samples"]), 3)
        sample = data["samples"][0]
        self.assertIn("id", sample)
        self.assertIn("title", sample)
        self.assertIn("youtube_url", sample)
        self.assertIn("duration", sample)

    def test_analyze_endpoint_sample_success(self):
        payload = {
            "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
            "video_duration": 620,
            "category": "fitness",
        }
        response = self.client.post("/api/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertTrue(body["success"])
        self.assertIsNotNone(body["data"])
        self.assertIsNotNone(body["prompt_used"])

        # Validate with Pydantic model directly
        validated = MasterAnalysisResponse.model_validate(body["data"])
        self.assertGreater(len(validated.moments), 0)
        self.assertEqual(len(validated.hook_dimensions), 4)
        self.assertEqual(len(validated.title_alternatives), 3)
        self.assertEqual(len(validated.score_factors), 4)
        self.assertGreaterEqual(validated.readiness_score, 0)
        self.assertLessEqual(validated.readiness_score, 100)

        # Inspect AI reasoning prompt check
        self.assertIn("TASK:", body["prompt_used"])
        self.assertIn("rubric", body["prompt_used"].lower())

    def test_analyze_endpoint_missing_url(self):
        payload = {
            "youtube_url": "   ",
        }
        response = self.client.post("/api/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertIn("valid YouTube URL", body["error"])

    def test_audience_panel_endpoint_sample_success(self):
        payload = {
            "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
            "analysis_context": "A foundational full-body dumbbell workout designed for beginners.",
            "video_duration": 620,
            "category": "fitness",
        }
        response = self.client.post("/api/panel", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertTrue(body["success"])
        self.assertIsNotNone(body["data"])
        self.assertIsNotNone(body["prompt_used"])

        # Validate with Pydantic model directly
        validated = AudiencePanelResponse.model_validate(body["data"])
        self.assertEqual(len(validated.panel_reactions), 3)

        # Check disagreements (key differentiator)
        self.assertGreater(len(validated.disagreements), 0)
        first_disagreement = validated.disagreements[0]
        self.assertIsNotNone(first_disagreement.topic)

    def test_api_key_auth(self):
        import main
        original_key = main.EXPECTED_API_KEY
        original_req = main.REQUIRE_API_KEY
        try:
            main.EXPECTED_API_KEY = "test-secret-key-12345"
            main.REQUIRE_API_KEY = True

            payload = {
                "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
                "video_duration": 620,
            }

            # 1. No key -> 401 when REQUIRE_API_KEY is True
            resp_no_key = self.client.post("/api/analyze", json=payload)
            self.assertEqual(resp_no_key.status_code, 401)

            # 2. Wrong key -> 401
            resp_wrong_key = self.client.post(
                "/api/analyze",
                json=payload,
                headers={"X-API-Key": "wrong-key"}
            )
            self.assertEqual(resp_wrong_key.status_code, 401)

            # 3. Correct key -> 200
            resp_correct = self.client.post(
                "/api/analyze",
                json=payload,
                headers={"X-API-Key": "test-secret-key-12345"}
            )
            self.assertEqual(resp_correct.status_code, 200)
            self.assertTrue(resp_correct.json()["success"])

        finally:
            main.EXPECTED_API_KEY = original_key
            main.REQUIRE_API_KEY = original_req

    def test_timestamp_duration_clamping(self):
        from schemas import MasterAnalysisResponse, Moment, HookDimension, TitleAlternative, ScoreFactor

        # Create response with an out-of-bounds moment (800s in a 300s video)
        resp = MasterAnalysisResponse(
            summary="A short video demonstration.",
            moments=[
                Moment(timestamp_seconds=10, title="Intro", description="Intro segment"),
                Moment(timestamp_seconds=800, title="Out of bounds", description="Way past video end"),
            ],
            hook_score=8.5,
            hook_dimensions=[
                HookDimension(name="Clarity", score=9, timestamp_seconds=45, observation="Good", suggestion="Keep it"),
                HookDimension(name="Curiosity", score=8, timestamp_seconds=5, observation="Hook", suggestion="Good"),
                HookDimension(name="Pacing", score=8, timestamp_seconds=15, observation="Fast", suggestion="Good"),
                HookDimension(name="Payoff Promise", score=9, timestamp_seconds=20, observation="Clear", suggestion="Good"),
            ],
            current_title_assessment="Decent title",
            title_alternatives=[
                TitleAlternative(title="Alt 1", strengths="Clear", weaknesses="None", rubric_score=8),
                TitleAlternative(title="Alt 2", strengths="Engaging", weaknesses="None", rubric_score=9),
                TitleAlternative(title="Alt 3", strengths="Catchy", weaknesses="None", rubric_score=8),
            ],
            recommended_title_index=1,
            readiness_score=85,
            score_factors=[
                ScoreFactor(name="Hook Strength", score=22, evidence="Strong"),
                ScoreFactor(name="Content Structure", score=21, evidence="Solid"),
                ScoreFactor(name="Pacing", score=21, evidence="Good"),
                ScoreFactor(name="Title Fit", score=21, evidence="Accurate"),
            ],
            top_improvements=["Shorten intro", "Add visual cues", "Clearer outro"],
        )

        resp.clamp_to_duration(300)
        # Moment 800s must be clamped to 300s
        self.assertEqual(resp.moments[1].timestamp_seconds, 300)
        # Hook dimension at 45s must be clamped to min(300, 30) = 30s
        self.assertEqual(resp.hook_dimensions[0].timestamp_seconds, 30)

    def test_resolve_video_title(self):
        from main import resolve_video_title

        # 1. Provided title
        title1 = resolve_video_title("https://www.youtube.com/watch?v=123", "My Real Workout Title")
        self.assertEqual(title1, "My Real Workout Title")

        # 2. Known sample URL
        title2 = resolve_video_title("https://www.youtube.com/watch?v=U0bhE67HuDY")
        self.assertEqual(title2, "5 Essential Dumbbell Exercises for Beginners | Full Body Routine")

    def test_shorts_endpoint_sample_success(self):
        payload = {
            "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
            "video_duration": 620,
            "category": "fitness",
        }
        response = self.client.post("/api/shorts", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertIsNotNone(body["data"])
        self.assertGreater(len(body["data"]), 0)

        clip = body["data"][0]
        self.assertIn("start_seconds", clip)
        self.assertIn("end_seconds", clip)
        self.assertIn("duration_seconds", clip)
        self.assertLessEqual(clip["duration_seconds"], 60)
        self.assertIn("title", clip)
        self.assertIn("hook_caption", clip)
        self.assertIn("reason_standalone", clip)

    def test_translate_endpoint_validation(self):
        # Empty language returns error
        payload = {
            "target_language": "  ",
            "summary": "Sample summary",
            "top_improvements": ["Improve hook"],
        }
        response = self.client.post("/api/translate", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertFalse(body["success"])
        self.assertIn("specify a target language", body["error"])

    def test_translate_tamil_authentic_script(self):
        payload = {
            "target_language": "Tamil",
            "summary": "A foundational full-body dumbbell workout designed for beginners.",
            "top_improvements": [
                "Replace placeholder title with descriptive title.",
                "Eliminate the 10-second opening static title cards."
            ],
            "title_alternatives": ["Build Full-Body Strength With Just 2 Dumbbells"]
        }
        response = self.client.post("/api/translate", json=payload)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        data = body["data"]
        self.assertEqual(data["target_language"], "Tamil")
        self.assertTrue(len(data["translated_summary"]) > 0)

        # Verify authentic Tamil Unicode range (\u0B80-\u0BFF) is present
        has_tamil = any("\u0b80" <= char <= "\u0bff" for char in data["translated_summary"])
        self.assertTrue(has_tamil, "Translated summary must contain authentic Tamil script characters")


if __name__ == "__main__":
    unittest.main()
