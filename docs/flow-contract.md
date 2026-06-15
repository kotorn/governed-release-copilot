# Flow Contract

The tenant implementation keeps the public `ReleaseChangeV1` contract intact.
Power Automate adapts the flat evidence-backed payload into the release drafting
and approval workflow, and the exported definition in ADO is the canonical
source of truth after any UI-only configuration.

## Processing Order

1. Receive a schema-compatible payload over an authenticated or signed request.
2. Read `metadata.correlationId`, or create a run correlation identifier.
3. Validate the schema and recompute the canonical hash.
4. Query the release register by `changeHash` before any AI call.
5. Return the existing item when the hash is already registered.
6. Transform the evidence into the `Run an agent` bridge input.
7. Create a Draft item when the AI decision is `NeedsInput`.
8. Otherwise create a Ready for Review item and return HTTP `202`.
9. Wait for human approval after the caller has received the response.
10. Publish `announcement.md`, `tech-summary.md`, `README.md`, and the
    citation-ready DOCX only after approval.
11. Return rejected items to Draft without publishing files.

## Response Semantics

| Code | Meaning |
|---:|---|
| `202` | Ready for Review or Needs Input |
| `200` | Duplicate hash; the existing item is reused |
| `400` | The request does not satisfy the trigger schema |
| `401` or `403` | The request is not authorized |
| `500` | Processing failed; production responses expose only correlation data |

## Duplicate Protection

The flow queries by `changeHash` before creation. The register also enforces a
unique, indexed `ChangeHash` field as the final concurrency guard.

The public validator remains the authoritative canonical hash implementation.
The PowerShell submitter runs it before any network request.

## Canonical States

See [docs/STATE-MODEL.md](STATE-MODEL.md) for the canonical state model and
SharePoint choice mapping. The important invariant is that `Rejected` and
`NeedsInput` never become published truth.

## AI Bridge Rules

- `metadata.aiDecision` is ignored by the Flow.
- Duplicate detection happens before the AI bridge.
- If the AI response cannot be parsed or does not match the expected shape, the
  run fails closed and creates no approval or files.
- `Run an agent` is the preferred bridge. If the UI must configure that node,
  the exported definition becomes canonical immediately after the change.
