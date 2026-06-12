# Decisions

This log records judgment calls made while building the public package.

| ID | Decision | Reason |
|---|---|---|
| D01 | Build the public repository in `C:\dev\governed-release-copilot` with a new root commit. | Keeps public history independent from private and OneDrive working folders. |
| D02 | Use the configured public Git identity with a GitHub-provided no-reply address. | Avoids exposing a personal or company mailbox in commit metadata. |
| D03 | Use Python 3.12 and pytest as the only application and test stack. | Meets the single-stack constraint and keeps local and CI behavior consistent. |
| D04 | Define four deterministic outcomes: `ReadyForApproval`, `NeedsInput`, `Duplicate`, and `Rejected`. | Makes fail-closed behavior testable without tenant access. |
| D05 | Treat missing evidence and not-run tests as `NeedsInput`. | The request may be repairable, but it must not progress to drafting or approval. |
| D06 | Treat schema errors, hash mismatch, failed tests, and unavailable rollback as `Rejected`. | These conditions are unsafe to promote and require a corrected submission. |
| D07 | Exclude `releaseId`, `timestamp`, and `changeHash` from the canonical hash. | Retries may receive a new envelope while the material change remains identical. |
| D08 | Keep every sample synthetic and require the `RN-SYNTH-` and `artifact://synthetic/` prefixes. | Makes accidental use of real release evidence easier to detect. |
| D09 | Represent the product with diagrams and evidence files, not generated product UI. | Avoids presenting fictional interfaces as working Microsoft product screens. |
| D10 | Use Gemini only for narration support and Veo only for optional intro or outro polish. | Keeps Google AI outside the product proof and makes the production method transparent. |
| D11 | Generate captions from frozen scene text and test word-for-word parity. | Prevents transcription drift in product terms such as `ReleaseChangeV1`. |
| D12 | Mark live Copilot Studio, SharePoint, Power Automate, and Work IQ proof as `OWNER-TODO`. | Tenant work is outside this public-package scope and must not be fabricated. |

## Owner TODO

- Capture sanitized live evidence of the Microsoft IQ integration.
- Add the final public demo-video URL to the submission form.
- Complete the hackathon form using [docs/submission.md](docs/submission.md).
