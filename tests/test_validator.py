from __future__ import annotations

import copy

from governed_release_copilot.validator import (
    canonical_change_hash,
    validate_payload,
)

from conftest import load_sample


def test_valid_sample_matches_schema_and_hash(schema: dict) -> None:
    assert validate_payload(load_sample("valid.json"), schema) == []


def test_duplicate_sample_has_same_canonical_hash(schema: dict) -> None:
    valid = load_sample("valid.json")
    duplicate = load_sample("duplicate.json")

    assert validate_payload(duplicate, schema) == []
    assert canonical_change_hash(valid) == canonical_change_hash(duplicate)


def test_release_id_and_timestamp_do_not_change_hash() -> None:
    payload = load_sample("valid.json")
    changed = copy.deepcopy(payload)
    changed["releaseId"] = "RN-SYNTH-0099"
    changed["timestamp"] = "2026-06-14T00:00:00Z"

    assert canonical_change_hash(payload) == canonical_change_hash(changed)


def test_business_change_invalidates_stale_hash(schema: dict) -> None:
    payload = load_sample("valid.json")
    payload["businessReason"] = "A changed reason must produce a new canonical hash."

    assert validate_payload(payload, schema) == [
        "changeHash: does not match canonical payload hash"
    ]

