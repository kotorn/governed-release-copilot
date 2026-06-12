from __future__ import annotations

import json
from conftest import load_sample
from governed_release_copilot.mcp_server import (
    validate_release_change,
    evaluate_release_decision,
)


def test_mcp_validate_valid_payload() -> None:
    payload = load_sample("valid.json")
    payload_str = json.dumps(payload)

    result_str = validate_release_change(payload_str)
    result = json.loads(result_str)

    assert result["valid"] is True
    assert result["errors"] == []


def test_mcp_validate_invalid_payload() -> None:
    payload = load_sample("valid.json")
    payload["changeHash"] = "incorrecthash123"
    payload_str = json.dumps(payload)

    result_str = validate_release_change(payload_str)
    result = json.loads(result_str)

    assert result["valid"] is False
    assert len(result["errors"]) > 0


def test_mcp_evaluate_decision_ready() -> None:
    payload = load_sample("valid.json")
    payload_str = json.dumps(payload)

    result_str = evaluate_release_decision(payload_str, "[]")
    result = json.loads(result_str)

    assert result["decision"] == "ReadyForApproval"
    assert len(result["reasons"]) > 0


def test_mcp_evaluate_decision_duplicate() -> None:
    payload = load_sample("valid.json")
    payload_str = json.dumps(payload)
    registry_str = json.dumps([payload["changeHash"]])

    result_str = evaluate_release_decision(payload_str, registry_str)
    result = json.loads(result_str)

    assert result["decision"] == "Duplicate"
