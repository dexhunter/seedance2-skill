#!/usr/bin/env python3
"""Submit an opt-in Seedance 2.0 video job to Atlas Cloud."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import Request, urlopen

API_ORIGIN = "https://api.atlascloud.ai"
CATALOG_URL = f"{API_ORIGIN}/api/v1/models"
GENERATE_URL = f"{API_ORIGIN}/api/v1/model/generateVideo"
PREDICTION_URL = f"{API_ORIGIN}/api/v1/model/prediction/{{prediction_id}}"
TEXT_MODEL = "bytedance/seedance-2.0/text-to-video"
REFERENCE_MODEL = "bytedance/seedance-2.0/reference-to-video"
TERMINAL_SUCCESSES = {"completed", "succeeded", "success"}
TERMINAL_FAILURES = {"failed", "timeout", "canceled", "cancelled"}
RESOLUTIONS = ("480p", "720p", "720p-SR", "1080p", "1080p-SR", "1440p-SR", "4k")
RATIOS = ("16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive")
MEDIA_LIMITS = {"image": 9, "video": 3, "audio": 3}
SIZE_LIMITS = {
    "image": 30 * 1024 * 1024,
    "video": 50 * 1024 * 1024,
    "audio": 15 * 1024 * 1024,
}
MIME_OVERRIDES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".mov": "video/quicktime",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
}


class AtlasError(RuntimeError):
    """A user-facing Atlas error that never includes credentials."""


class AtlasReadError(AtlasError):
    """A transient read error that prediction polling may retry."""


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=True).encode()


def request_json(
    method: str,
    url: str,
    *,
    payload: dict[str, Any] | None = None,
    api_key: str | None = None,
    timeout: float = 30,
    open_request: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    headers = {"Accept": "application/json", "User-Agent": "seedance2-skill/1.0"}
    data = None
    if payload is not None:
        data = _json_bytes(payload)
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url, data=data, headers=headers, method=method)
    try:
        with open_request(request, timeout=timeout) as response:
            raw = response.read()
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        error = AtlasReadError if method == "GET" else AtlasError
        raise error(f"{method} request failed: {type(exc).__name__}") from exc
    try:
        result = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AtlasError(f"{method} response was not valid JSON") from exc
    if not isinstance(result, dict):
        raise AtlasError(f"{method} response must be a JSON object")
    return result


def unwrap(response: dict[str, Any]) -> Any:
    if "code" not in response:
        return response
    if str(response.get("code")) != "200":
        raise AtlasError(str(response.get("message") or "Atlas request failed"))
    return response.get("data")


def ensure_schema_url(url: str) -> None:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "static.atlascloud.ai"
        or parsed.username
        or parsed.password
        or parsed.port not in (None, 443)
    ):
        raise AtlasError("model schema URL is not hosted by Atlas Cloud")


def load_live_schema(
    model_id: str, *, open_request: Callable[..., Any] = urlopen
) -> dict[str, Any]:
    catalog_data = unwrap(request_json("GET", CATALOG_URL, open_request=open_request))
    if not isinstance(catalog_data, list):
        raise AtlasError("Atlas model catalog returned an unexpected response")
    matches = [
        item
        for item in catalog_data
        if isinstance(item, dict) and item.get("model") == model_id
    ]
    if len(matches) != 1:
        raise AtlasError(f"model not found in live Atlas catalog: {model_id}")
    schema_url = matches[0].get("schema")
    if not isinstance(schema_url, str) or not schema_url:
        raise AtlasError(f"model has no input schema: {model_id}")
    ensure_schema_url(schema_url)
    schema = request_json("GET", schema_url, open_request=open_request)
    input_schema = schema.get("components", {}).get("schemas", {}).get("Input")
    if not isinstance(input_schema, dict):
        raise AtlasError("model schema does not define components.schemas.Input")
    return input_schema


def validate_against_schema(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    properties = schema.get("properties")
    required = schema.get("required", [])
    if not isinstance(properties, dict) or not isinstance(required, list):
        raise AtlasError("model input schema is malformed")
    missing = [name for name in required if name not in payload]
    if missing:
        raise AtlasError(f"missing required fields: {', '.join(sorted(missing))}")
    unknown = sorted(set(payload) - set(properties))
    if unknown:
        raise AtlasError(f"unsupported fields for model: {', '.join(unknown)}")
    for name, value in payload.items():
        definition = properties.get(name)
        if not isinstance(definition, dict):
            continue
        allowed = definition.get("enum")
        if isinstance(allowed, list) and value not in allowed:
            raise AtlasError(f"invalid {name}: {value!r}")
        if isinstance(value, list):
            minimum = definition.get("minItems")
            maximum = definition.get("maxItems")
            if isinstance(minimum, int) and len(value) < minimum:
                raise AtlasError(f"{name} requires at least {minimum} item(s)")
            if isinstance(maximum, int) and len(value) > maximum:
                raise AtlasError(f"{name} allows at most {maximum} item(s)")


REFERENCE_PATTERN = re.compile(
    r"@(Image|图片|图|Video|视频|Audio|音频)\s*(\d+)", re.IGNORECASE
)


def translate_references(prompt: str) -> str:
    names = {
        "image": "image",
        "图片": "image",
        "图": "image",
        "video": "video",
        "视频": "video",
        "audio": "audio",
        "音频": "audio",
    }

    def replace(match: re.Match[str]) -> str:
        return f"{names[match.group(1).lower()]} {match.group(2)}"

    return REFERENCE_PATTERN.sub(replace, prompt)


def validate_reference_indices(prompt: str, media: dict[str, list[str]]) -> None:
    names = {
        "image": "image",
        "图片": "image",
        "图": "image",
        "video": "video",
        "视频": "video",
        "audio": "audio",
        "音频": "audio",
    }
    for match in REFERENCE_PATTERN.finditer(prompt):
        kind = names[match.group(1).lower()]
        index = int(match.group(2))
        if index < 1 or index > len(media[kind]):
            raise AtlasError(
                f"prompt references {kind} {index}, but {len(media[kind])} "
                f"{kind} file(s) were provided"
            )


def _remote_media(value: str) -> str | None:
    parsed = urlsplit(value)
    if not parsed.scheme:
        return None
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise AtlasError("remote media must use an HTTPS URL without credentials")
    return value


def encode_media(value: str, kind: str) -> str:
    remote = _remote_media(value)
    if remote:
        return remote
    path = Path(value).expanduser()
    if not path.is_file():
        raise AtlasError(f"{kind} file not found: {value}")
    size = path.stat().st_size
    if size > SIZE_LIMITS[kind]:
        raise AtlasError(f"{kind} file exceeds the supported size limit: {value}")
    mime = MIME_OVERRIDES.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0]
    if not mime or not mime.startswith(f"{kind}/"):
        raise AtlasError(f"unsupported {kind} file type: {value}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    media = {
        "image": list(args.image or []),
        "video": list(args.video or []),
        "audio": list(args.audio or []),
    }
    for kind, values in media.items():
        if len(values) > MEDIA_LIMITS[kind]:
            raise AtlasError(f"too many {kind} references (max {MEDIA_LIMITS[kind]})")
    if sum(map(len, media.values())) > 12:
        raise AtlasError(
            "reference images, videos, and audio must total at most 12 files"
        )
    if media["audio"] and not (media["image"] or media["video"]):
        raise AtlasError("reference audio requires at least one image or video")

    has_media = any(media.values())
    if has_media:
        validate_reference_indices(args.prompt, media)
    payload: dict[str, Any] = {
        "model": REFERENCE_MODEL if has_media else TEXT_MODEL,
        "prompt": translate_references(args.prompt) if has_media else args.prompt,
        "duration": args.duration,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "bitrate_mode": args.bitrate_mode,
        "generate_audio": args.generate_audio,
        "watermark": args.watermark,
        "return_last_frame": args.return_last_frame,
    }
    if args.seed is not None:
        payload["seed"] = args.seed
    for kind, field in (
        ("image", "reference_images"),
        ("video", "reference_videos"),
        ("audio", "reference_audios"),
    ):
        if media[kind]:
            payload[field] = [encode_media(item, kind) for item in media[kind]]
    return payload


def redacted_plan(payload: dict[str, Any]) -> dict[str, Any]:
    plan = dict(payload)
    for name in ("reference_images", "reference_videos", "reference_audios"):
        values = plan.get(name)
        if isinstance(values, list):
            plan[name] = ["<embedded-media>" if item.startswith("data:") else item for item in values]
    return plan


def submit_once(
    payload: dict[str, Any], api_key: str, *, open_request: Callable[..., Any] = urlopen
) -> str:
    response = request_json(
        "POST", GENERATE_URL, payload=payload, api_key=api_key, open_request=open_request
    )
    data = unwrap(response)
    if not isinstance(data, dict):
        raise AtlasError("generation submission returned no prediction object")
    prediction_id = data.get("id") or data.get("prediction_id")
    if not isinstance(prediction_id, str) or not prediction_id:
        raise AtlasError("generation submission returned no prediction ID")
    return prediction_id


def poll_prediction(
    prediction_id: str,
    api_key: str,
    *,
    attempts: int,
    interval: float,
    open_request: Callable[..., Any] = urlopen,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    if attempts < 1 or interval < 0:
        raise AtlasError("poll attempts must be positive and interval non-negative")
    url = PREDICTION_URL.format(prediction_id=quote(prediction_id, safe=""))
    last_read_error: AtlasReadError | None = None
    for attempt in range(attempts):
        try:
            data = unwrap(request_json("GET", url, api_key=api_key, open_request=open_request))
            last_read_error = None
        except AtlasReadError as exc:
            last_read_error = exc
            data = None
        if data is not None:
            if not isinstance(data, dict):
                raise AtlasError("prediction read returned an unexpected response")
            status = str(data.get("status") or "").lower()
            if status in TERMINAL_SUCCESSES:
                outputs = data.get("outputs")
                if not isinstance(outputs, list) or not outputs:
                    raise AtlasError("completed prediction has no output URLs")
                return data
            if status in TERMINAL_FAILURES:
                raise AtlasError(str(data.get("error") or f"prediction ended with status {status}"))
        if attempt + 1 < attempts:
            sleep(min(interval * (2**attempt), 15.0))
    if last_read_error:
        raise AtlasError(f"prediction polling exhausted after {attempts} attempts") from last_read_error
    raise AtlasError(f"prediction did not complete after {attempts} reads")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--image", action="append", help="HTTPS URL or local image; repeat as needed")
    parser.add_argument("--video", action="append", help="HTTPS URL or local video; repeat as needed")
    parser.add_argument("--audio", action="append", help="HTTPS URL or local audio; repeat as needed")
    parser.add_argument("--duration", type=int, choices=(-1, *range(4, 16)), default=5)
    parser.add_argument("--resolution", choices=RESOLUTIONS, default="720p")
    parser.add_argument("--ratio", choices=RATIOS, default="adaptive")
    parser.add_argument("--bitrate-mode", choices=("standard", "high"), default="standard")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--generate-audio", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--watermark", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--return-last-frame", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--poll-attempts", type=int, default=60)
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--dry-run", action="store_true", help="print a redacted local plan without network calls")
    parser.add_argument("--confirm-submit", action="store_true", help="confirm the single billable POST")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        payload = build_payload(args)
        if args.dry_run:
            print(json.dumps(redacted_plan(payload), indent=2, ensure_ascii=False))
            return 0
        if not args.confirm_submit:
            raise AtlasError("review --dry-run output, then add --confirm-submit to send one billable POST")
        api_key = os.environ.get("ATLASCLOUD_API_KEY")
        if not api_key:
            raise AtlasError("ATLASCLOUD_API_KEY is required")
        schema = load_live_schema(payload["model"])
        validate_against_schema(payload, schema)
        prediction_id = submit_once(payload, api_key)
        print(json.dumps({"id": prediction_id, "status": "submitted"}))
        result = poll_prediction(
            prediction_id,
            api_key,
            attempts=args.poll_attempts,
            interval=args.poll_interval,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except AtlasError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
