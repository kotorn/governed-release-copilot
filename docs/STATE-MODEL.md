# Release State Model

This repository uses canonical states so the public story, the flow contract,
and the SharePoint mapping stay aligned.

| Canonical state | Approval | Published files | Notes |
|---|---:|---:|---|
| `Received` | No | No | Payload accepted into the intake boundary |
| `DuplicateDetected` | No | No | Existing `changeHash` prevents a second run |
| `AIProcessing` | No | No | The agent is drafting or classifying the request |
| `NeedsInput` | No | No | Missing evidence is returned to the caller |
| `ReadyForApproval` | Not yet | No | The release is complete enough for review |
| `ApprovalPending` | Yes | No | Human review is in progress |
| `Approved` | Completed | Generation permitted | Publication can create notes and DOCX |
| `Rejected` | Completed | No | The request stops without published truth |
| `Published` | Completed | Yes | Approved notes are now the source for citation |
| `FailedClosed` | No | No | Validation or AI parsing failed safely |

## SharePoint Mapping

- `Draft` maps to `Received`, `NeedsInput`, `Rejected`, or `FailedClosed`.
- `Ready for Review` maps to `ReadyForApproval` and `ApprovalPending`.
- `Approved` maps to the approved and published states.
- If the current list choice does not expose `Rejected`, the approval status
  stays `N/A` and the rejection reason is captured in run history or audit
  metadata.

