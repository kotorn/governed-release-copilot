"""ReleaseChangeV1 schema and canonical-hash validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

HASH_EXCLUDED_FIELDS = frozenset({"releaseId", "timestamp", "changeHash"})


def canonical_hash_input(payload: dict[str, Any]) -> bytes:
    normalized = {
        key: value
        for key, value in payload.items()
        if key not in HASH_EXCLUDED_FIELDS
    }
    serialized = json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return serialized.encode("utf-8")


def canonical_change_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_hash_input(payload)).hexdigest()


def load_schema(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    Draft202012Validator.check_schema(schema)
    return schema


def schema_errors(
    payload: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    rendered: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        rendered.append(f"{location}: {error.message}")
    return rendered


def validate_payload(
    payload: dict[str, Any], schema: dict[str, Any]
) -> list[str]:
    errors = schema_errors(payload, schema)
    if errors:
        return errors

    if payload["changeHash"] != canonical_change_hash(payload):
        return ["changeHash: does not match canonical payload hash"]
    return []

