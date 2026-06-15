# Feature Contract

This document is the public, synthetic counterpart to the private ADO feature
ledger. It describes what the CLI-first plan must prove, what each feature
accepts, and what evidence a judge or reviewer should expect to see.

## Common Rules

- Inputs are `ReleaseChangeV1` payloads plus supporting evidence.
- Outputs are governed release drafts, approval states, published notes, and
  citation-backed Q&A.
- Owner is the smallest component that can enforce the rule: validator,
  submitter, flow, agent, SharePoint, or governance gate.
- Negative tests must prove fail-closed behavior.
- Evidence lives under `evidence/` in this repo or in the private ADO ledger.

## Feature Table

| ID | Purpose | Runtime scenario | Negative test | CLI assertion | UI assertion | Evidence / video |
|---|---|---|---|---|---|---|
| F01 | Validate schema and canonical hash before any submission | Submit a valid `ReleaseChangeV1` payload | Change the payload after hashing | `grc-validate` returns `0` for valid input and `2` on hash mismatch | The submitter blocks the request before POST | `evidence/01-static-checks/F01-schema-hash.md`, video `0:30-1:00` |
| F02 | Detect duplicates before AI runs | Re-submit the same `changeHash` in a batch or registry | Duplicate hash should not reach the AI bridge | Duplicate detection returns exit code `3` or flow duplicate status | The run history shows the AI node was skipped | `evidence/06-negative-tests/F02-duplicate-before-ai.md`, video `1:00-1:30` |
| F03 | Produce structured drafting through `Run an agent` | A new release is transformed into AI input | Malformed AI response or missing sections | Exported solution shows the structured-output bridge | The UI configuration exports cleanly and round-trips | `evidence/03-import-publish/F03-structured-drafting.md`, video `1:30-1:55` |
| F04 | Return `NeedsInput` and fail closed | Required evidence is missing | Missing evidence should not create approval or files | Flow output maps missing fields to `NeedsInput` | No approval card appears for the draft path | `evidence/05-needs-input/F04-needs-input.md`, video `1:55-2:10` |
| F05 | Require human approval before publication | A complete release reaches review | Rejected approval must not publish notes | Flow definition shows approval as the gate before publication | Approval history records the human decision | `evidence/03-import-publish/F05-approval-gate.md`, video `1:55-2:40` |
| F06 | Publish Markdown and citation-ready DOCX only after approval | Approved release is promoted | Approved files must not exist before approval | Read-back confirms `announcement.md`, `tech-summary.md`, `README.md`, and DOCX were created | Library view shows the approved folder only | `evidence/07-sharepoint-readback/F06-publication.md`, video `2:40-3:05` |
| F07 | Answer from approved SharePoint knowledge with citations | A fresh conversation asks what changed | Draft or rejected content must not be cited as truth | Knowledge source points to the approved library path only | Agent answers with a citation from approved notes | `evidence/08-citation/F07-approved-citation.md`, video `3:05-3:30` |
| F08 | Show Microsoft IQ integration evidence | Work IQ actions exist in the solution | Work IQ runtime retrieval can be blocked without failing the demo | Solution export contains Work IQ User and Work IQ Copilot actions | The UI shows the configured actions or test-canvas fallback | `evidence/09-work-iq/F08-work-iq-static.md`, video `3:30-3:45` |
| F09 | Preserve correlation and audit traceability | A single release needs end-to-end tracking | Missing correlation must not break the run | Flow export and read-back include `correlationId` handling | Run history and approval details show the same correlation ID | `evidence/04-ready-for-approval/F09-correlation.md`, video `1:30-2:40` |
| F10 | Enforce security, permissions, and DLP gates | The solution is prepared for runtime testing | Shared personal identities or blocked connectors must fail the gate | Static checks verify approved identities and connector scope | UI shows only approved connection references | `evidence/01-static-checks/F10-security-dlp.md`, video `4:10-4:30` |
| F11 | Keep synthetic data and privacy controls intact | The demo and repo are reviewed frame by frame | Any real UPN, email, tenant URL, or internal path fails review | Privacy scan and gitleaks pass before publish | Clean browser profile and DND stay visible in the final capture | `evidence/06-negative-tests/F11-privacy.md`, video `3:45-4:10` |

## Non-blocking Enhancements

- Local PowerShell loopback submission is public proof; live tenant orchestration remains an owner evidence track.
- Work IQ runtime retrieval, when policy allows it.
- Automated environment validation beyond the current CLI checks.
- Copilot Studio evaluation dashboards for richer regression review.
