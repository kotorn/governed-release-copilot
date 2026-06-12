from __future__ import annotations

from governed_release_copilot.policy import Decision, evaluate_release

from conftest import load_sample


def test_valid_payload_is_ready_for_approval(schema: dict) -> None:
    evaluation = evaluate_release(load_sample("valid.json"), schema)

    assert evaluation.decision is Decision.READY_FOR_APPROVAL


def test_missing_evidence_needs_input(schema: dict) -> None:
    evaluation = evaluate_release(load_sample("missing-fields.json"), schema)

    assert evaluation.decision is Decision.NEEDS_INPUT
    assert any("afterEvidence" in reason for reason in evaluation.reasons)


def test_duplicate_hash_is_blocked(schema: dict) -> None:
    valid = load_sample("valid.json")
    duplicate = load_sample("duplicate.json")

    evaluation = evaluate_release(
        duplicate,
        schema,
        accepted_hashes={valid["changeHash"]},
    )

    assert evaluation.decision is Decision.DUPLICATE


def test_failed_test_evidence_is_rejected(schema: dict) -> None:
    evaluation = evaluate_release(load_sample("rejected.json"), schema)

    assert evaluation.decision is Decision.REJECTED
    assert evaluation.reasons == ("test evidence contains a failed result",)


def test_schema_invalid_payload_fails_closed(schema: dict) -> None:
    evaluation = evaluate_release(load_sample("invalid.json"), schema)

    assert evaluation.decision in {Decision.NEEDS_INPUT, Decision.REJECTED}
    assert evaluation.decision is not Decision.READY_FOR_APPROVAL

