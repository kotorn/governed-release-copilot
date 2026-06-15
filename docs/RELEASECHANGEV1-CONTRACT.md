# ReleaseChangeV1 Contract

The public contract stays flat and synthetic. It matches the existing schema
and validator and does not introduce nested evidence sections or speculative
fields.

This is the active submission contract for the public repository. Broader
production-oriented profiles remain future work and must not replace this
schema on the submission branch.

## Required Fields

- `releaseId`
- `timestamp`
- `changeHash`
- `source`
- `environment`
- `changeType`
- `component`
- `businessReason`
- `beforeEvidence`
- `afterEvidence`
- `testEvidence`
- `impact`
- `risk`
- `rollback`

## Optional Fields

- `metadata`

The `metadata` object is optional and string-valued. It may carry helper
values such as `metadata.correlationId`, but it must not become a new required
input for the public contract.

## Canonical Hash Rules

- `changeHash` is the idempotency key.
- Canonical hashing excludes only the top-level fields `releaseId`,
  `timestamp`, and `changeHash`.
- The validator recomputes the canonical SHA-256 from the remaining top-level
  payload and rejects mismatches before any network request.
- `metadata.correlationId`, when present, remains part of the canonical hash
  because it is not excluded.

## AI Bridge Rules

- The Flow ignores caller-supplied `metadata.aiDecision`.
- The AI bridge returns `ReadyForApproval` or `NeedsInput`.
- `NeedsInput` must list missing evidence rather than inventing it.
- `ReadyForApproval` must be evidence-based and complete.

## Versioning

- Any change to required fields, canonical hashing, or duplicate rules is a
  versioned contract change.
- Compatibility tests must prove the new version still round-trips through the
  validator, submitter, flow, and approval boundary.
