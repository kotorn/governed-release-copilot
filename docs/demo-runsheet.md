# Demo Run-Sheet

Hard limit: five minutes. Use only synthetic release identifiers and hide
notifications, browser profiles, tenant addresses, and user identities.
Use the approved DOCX for the citation shot; Markdown files are the human
summary, not the grounding source for the demo capture.

| Time | Screen | Narration |
|---|---|---|
| 0:00 | Problem and architecture | Release evidence, communication, and approval are usually fragmented. |
| 0:30 | `ReleaseChangeV1` schema | The contract requires before and after evidence, tests, impact, risk, rollback, and a canonical hash. |
| 1:00 | Validation and hash failure | Invalid or modified evidence is blocked before a network request. |
| 1:30 | Submit the synthetic payload | The intake flow returns `202`, creates one review item, and uses the hash as its idempotency key. |
| 2:05 | Human approval and register | Approval is explicit; the register becomes Approved only after the decision. |
| 2:40 | Three Markdown files | Show the announcement, technical summary, and release README with the same release ID and hash. |
| 3:15 | Agent Q&A | Ask what changed and the rollback plan. Show the approved-note citation from the approved DOCX or the prepared fallback evidence. |
| 3:45 | Reliability montage | Duplicate, hash mismatch, unauthorized `401`, and green CI appear as fast proof shots. |
| 4:15 | Work IQ and governance | Show Work IQ actions, Needs Input, duplicate protection, and approved-only truth. |
| 4:40 | Close | Summarize why the same governed pattern can be reused across BPA changes. |

## Recording Checklist

1. Record a backup take before polishing transitions.
2. Pre-stage the approved synthetic release and its three files.
3. Keep a Draft Needs Input item ready for the governance shot.
4. Prepare a broken payload under the operating system temporary directory.
5. Use a neutral terminal path and hide the clock and notifications.
6. If Work IQ retrieval is policy-blocked, show its configured actions and use
   the approved-note fallback.
7. If channel publication is blocked, use the Copilot Studio test canvas.
8. Freeze the narration script before generating captions.
9. Run the judge comprehension test before final export.
10. If fresh tenant evidence is unavailable, say `not live-verified in final run`
    instead of implying that a newer publish or citation test happened.
