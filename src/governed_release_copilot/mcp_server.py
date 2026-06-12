"""Model Context Protocol (MCP) server for Governed Release Copilot."""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .policy import evaluate_release
from .validator import load_schema

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schema" / "ReleaseChangeV1.schema.json"

mcp = FastMCP("Governed-Release-Copilot")


@mcp.tool()
def validate_release_change(payload_json: str) -> str:
    """Validate a ReleaseChangeV1 JSON payload for schema correctness and hash match.

    Args:
        payload_json: The raw JSON string of the ReleaseChangeV1 payload.

    Returns:
        A JSON string containing the validation result, listing any errors.
    """
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as err:
        return json.dumps({"valid": False, "errors": [f"Invalid JSON: {err}"]})

    try:
        schema = load_schema(SCHEMA_PATH)
    except Exception as err:
        return json.dumps(
            {"valid": False, "errors": [f"Failed to load schema: {err}"]}
        )

    from .validator import validate_payload

    errors = validate_payload(payload, schema)
    if errors:
        return json.dumps({"valid": False, "errors": errors})
    return json.dumps({"valid": True, "errors": []})


@mcp.tool()
def evaluate_release_decision(
    payload_json: str, registry_json: str = "[]"
) -> str:
    """Evaluate a ReleaseChangeV1 payload against the deterministic decision policy.

    Args:
        payload_json: The raw JSON string of the ReleaseChangeV1 payload.
        registry_json: An optional JSON string representing the array of already accepted hashes.

    Returns:
        A JSON string with the decision (ReadyForApproval, NeedsInput, Duplicate, Rejected)
        and reasons.
    """
    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as err:
        return json.dumps(
            {
                "decision": "Rejected",
                "reasons": [f"Invalid JSON: {err}"],
            }
        )

    try:
        accepted_hashes = json.loads(registry_json)
        if not isinstance(accepted_hashes, list):
            accepted_hashes = []
    except json.JSONDecodeError:
        accepted_hashes = []

    try:
        schema = load_schema(SCHEMA_PATH)
    except Exception as err:
        return json.dumps(
            {
                "decision": "Rejected",
                "reasons": [f"Failed to load schema: {err}"],
            }
        )

    evaluation = evaluate_release(payload, schema, accepted_hashes)
    return json.dumps(
        {
            "decision": evaluation.decision,
            "reasons": list(evaluation.reasons),
        }
    )


if __name__ == "__main__":
    mcp.run()
