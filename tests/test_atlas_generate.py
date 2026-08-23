import argparse
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import atlas_generate as atlas


class Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def args(**overrides):
    values = {
        "prompt": "Use @Image1 as the opening frame",
        "image": [],
        "video": [],
        "audio": [],
        "duration": 5,
        "resolution": "720p",
        "ratio": "adaptive",
        "bitrate_mode": "standard",
        "seed": None,
        "generate_audio": True,
        "watermark": False,
        "return_last_frame": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class AtlasGenerateTests(unittest.TestCase):
    def test_translates_skill_references_for_atlas(self):
        self.assertEqual(
            atlas.translate_references("@Image1 @图片2 @图3 @Video1 @视频2 @Audio1 @音频2"),
            "image 1 image 2 image 3 video 1 video 2 audio 1 audio 2",
        )

    def test_text_payload_keeps_prompt_and_uses_text_model(self):
        payload = atlas.build_payload(args(prompt="A quiet lake"))
        self.assertEqual(payload["model"], atlas.TEXT_MODEL)
        self.assertEqual(payload["prompt"], "A quiet lake")
        self.assertNotIn("reference_images", payload)

    def test_reference_payload_encodes_local_media_and_rewrites_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "frame.png"
            image.write_bytes(b"png")
            payload = atlas.build_payload(
                args(prompt="Use @Image1 as the opening frame", image=[str(image)])
            )
        self.assertEqual(payload["model"], atlas.REFERENCE_MODEL)
        self.assertEqual(payload["prompt"], "Use image 1 as the opening frame")
        self.assertTrue(payload["reference_images"][0].startswith("data:image/png;base64,"))

    def test_audio_requires_visual_reference(self):
        with self.assertRaisesRegex(atlas.AtlasError, "requires at least one"):
            atlas.build_payload(args(audio=["https://example.com/music.mp3"]))

    def test_rejects_reference_without_matching_media(self):
        with self.assertRaisesRegex(atlas.AtlasError, "references video 2"):
            atlas.build_payload(
                args(
                    prompt="Use @Video2 for motion",
                    image=["https://example.com/frame.png"],
                )
            )

    def test_rejects_non_https_remote_media(self):
        with self.assertRaisesRegex(atlas.AtlasError, "must use an HTTPS"):
            atlas.build_payload(args(image=["http://example.com/frame.png"]))

    def test_submit_once_performs_one_post(self):
        calls = []

        def opener(request, timeout):
            calls.append((request.method, timeout))
            return Response({"code": 200, "data": {"id": "pred-1"}})

        self.assertEqual(atlas.submit_once({"model": "m"}, "secret", open_request=opener), "pred-1")
        self.assertEqual(calls, [("POST", 30)])

    def test_post_transport_error_is_not_retryable(self):
        calls = []

        def opener(_request, timeout):
            calls.append(timeout)
            raise URLError("offline")

        with self.assertRaises(atlas.AtlasError):
            atlas.submit_once({"model": "m"}, "secret", open_request=opener)
        self.assertEqual(len(calls), 1)

    def test_poll_retries_get_and_returns_completed_prediction(self):
        responses = iter(
            [
                URLError("temporary"),
                Response({"code": 200, "data": {"id": "pred-1", "status": "running"}}),
                Response({"id": "pred-1", "status": "completed", "outputs": ["https://example.com/out.mp4"]}),
            ]
        )
        sleeps = []

        def opener(_request, timeout):
            result = next(responses)
            if isinstance(result, Exception):
                raise result
            return result

        result = atlas.poll_prediction(
            "pred-1", "secret", attempts=3, interval=1, open_request=opener, sleep=sleeps.append
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(sleeps, [1, 2])

    def test_live_schema_requires_trusted_host(self):
        responses = iter(
            [Response({"code": 200, "data": [{"model": atlas.TEXT_MODEL, "schema": "https://evil.example/schema.json"}]})]
        )
        with self.assertRaisesRegex(atlas.AtlasError, "not hosted"):
            atlas.load_live_schema(atlas.TEXT_MODEL, open_request=lambda *_args, **_kwargs: next(responses))

    def test_schema_validation_rejects_unknown_fields(self):
        schema = {"required": ["model"], "properties": {"model": {"type": "string"}}}
        with self.assertRaisesRegex(atlas.AtlasError, "unsupported fields"):
            atlas.validate_against_schema({"model": "m", "extra": True}, schema)


if __name__ == "__main__":
    unittest.main()
