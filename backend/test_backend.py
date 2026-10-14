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
        try:
            main.EXPECTED_API_KEY = "test-secret-key-12345"

            payload = {
                "youtube_url": "https://www.youtube.com/watch?v=U0bhE67HuDY",
                "video_duration": 620,
            }

            # 1. No key -> 401
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


if __name__ == "__main__":
    unittest.main()
