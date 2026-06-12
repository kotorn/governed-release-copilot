"""Deterministic, fail-closed release decision policy."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Collection

from .validator import validate_payload


class Decision(StrEnum):
    READY_FOR_APPROVAL = "ReadyForApproval"
    NEEDS_INPUT = "NeedsInput"
    DUPLICATE = "Duplicate"
    REJECTED = "Rejected"


@dataclass(frozen=True)
class Evaluation:
    decision: Decision
    reasons: tuple[str, ...]


EVIDENCE_FIELDS = ("beforeEvidence", "afterEvidence", "testEvidence")


def _missing_evidence(payload: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for field in EVIDENCE_FIELDS:
        if not payload.get(field):
            missing.append(field)
    if not payload.get("businessReason"):
        missing.append("businessReason")
    if not payload.get("rollback"):
        missing.append("rollback")
    return missing


def evaluate_release(
    payload: dict[str, Any],
    schema: dict[str, Any],
    accepted_hashes: Collection[str] = (),
) -> Evaluation:
    missing = _missing_evidence(payload)
    if missing:
        return Evaluation(
            Decision.NEEDS_INPUT,
            tuple(f"missing evidence: {field}" for field in missing),
        )

    errors = validate_payload(payload, schema)
    if errors:
        return Evaluation(Decision.REJECTED, tuple(errors))

    if payload["changeHash"] in accepted_hashes:
        return Evaluation(
            Decision.DUPLICATE,
            ("changeHash already accepted",),
        )

    statuses = {
        item["status"] for item in payload.get("testEvidence", [])
    }
    if "failed" in statuses:
        return Evaluation(
            Decision.REJECTED,
            ("test evidence contains a failed result",),
        )
    if "not-run" in statuses:
        return Evaluation(
            Decision.NEEDS_INPUT,
            ("test evidence contains a not-run result",),
        )
    if not payload["rollback"]["available"]:
        return Evaluation(
            Decision.REJECTED,
            ("rollback is unavailable",),
        )

    return Evaluation(
        Decision.READY_FOR_APPROVAL,
        ("schema, hash, evidence, tests, and rollback checks passed",),
    )

