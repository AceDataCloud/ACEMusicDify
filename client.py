from __future__ import annotations

import json
import math
from pathlib import Path
from urllib.parse import urlsplit

import requests

BASE_URL = "https://api.acedata.cloud/acemusic"
MODELS = ("acemusic-v1.1", "acemusic-v1")

OPERATIONS = json.loads(
    Path(__file__).with_name("operations.json").read_text(encoding="utf-8")
)


def build_request(operation, values):
    spec = OPERATIONS[operation]
    body = spec["body"].copy()
    for field, entry in spec["fields"].items():
        value = values.get(field)
        if isinstance(value, str):
            value = value.strip()
        if value is None or value == "":
            if entry["required"]:
                raise ValueError(f"{field} is required")
            continue
        kind = entry["kind"]
        if kind in ("strength", "page", "size"):
            maximum = 10001 if kind == "page" else 100
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or not 1 <= value <= maximum
            ):
                raise ValueError(f"{field} must be between 1 and {maximum}")
            if kind != "strength":
                if value != int(value):
                    raise ValueError(f"{field} must be an integer")
                value = int(value)
        elif kind == "ids":
            if not isinstance(value, str):
                raise ValueError("Enter one task ID per line")
            value = [line.strip() for line in value.splitlines() if line.strip()]
            if not 1 <= len(value) <= 100:
                raise ValueError("Provide 1 to 100 task IDs")
        elif not isinstance(value, str) or len(value) > 20000:
            raise ValueError(f"Invalid {field}")
        elif kind == "model" and value not in MODELS:
            raise ValueError("Unknown ACE Music model")
        elif kind == "url":
            parsed = urlsplit(value)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username
                or parsed.password
            ):
                raise ValueError("Provide a public HTTPS MP3 URL")
        body[entry["key"]] = value
    if operation == "mashup":
        ids = [body.pop("first_audio_id"), body.pop("second_audio_id")]
        if ids[0] == ids[1]:
            raise ValueError("The two reference track IDs must be distinct")
        body["mashup_audio_ids"] = ids
    return spec["endpoint"], body


def invoke(token, operation, values):
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Configure an Ace Data Cloud application API key")
    endpoint, body = build_request(operation, values)
    try:
        response = requests.post(
            f"{BASE_URL}/{endpoint}",
            json=body,
            headers={"Authorization": f"Bearer {token.strip()}"},
            timeout=(10, 120),
            allow_redirects=False,
        )
    except requests.RequestException:
        raise RuntimeError(
            "The API response was interrupted. Check task history before submitting again."
        ) from None
    if not 200 <= response.status_code < 300:
        raise RuntimeError(
            f"ACE Music returned HTTP {response.status_code}. Check task history before resubmitting."
        )
    result = response.json()
    if not isinstance(result, dict):
        raise ValueError(
            "Unexpected ACE Music response. Check task history before submitting again."
        )
    return result
