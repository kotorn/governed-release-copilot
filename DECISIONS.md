# Decisions

This log records judgment calls made while building the public package.

| ID | Decision | Reason |
|---|---|---|
| D01 | Build the public repository in `C:\dev\governed-release-copilot` with a new root commit. | Keeps public history independent from private and OneDrive working folders. |
| D02 | Use the configured public Git identity with a GitHub-provided no-reply address. | Avoids exposing a personal or company mailbox in commit metadata. |
| D03 | Use Python 3.12 and pytest as the primary application stack, then add a small PowerShell submission boundary with Pester integration tests. | Keeps the public core deterministic while proving the CLI-first submission path expected by the BPA workflow. |
| D04 | Define four deterministic outcomes: `ReadyForApproval`, `NeedsInput`, `Duplicate`, and `Rejected`. | Makes fail-closed behavior testable without tenant access. |
| D05 | Treat missing evidence and not-run tests as `NeedsInput`. | The request may be repairable, but it must not progress to drafting or approval. |
| D06 | Treat schema errors, hash mismatch, failed tests, and unavailable rollback as `Rejected`. | These conditions are unsafe to promote and require a corrected submission. |
| D07 | Exclude `releaseId`, `timestamp`, and `changeHash` from the canonical hash. | Retries may receive a new envelope while the material change remains identical. |
| D08 | Keep every sample synthetic and require the `RN-SYNTH-` and `artifact://synthetic/` prefixes. | Makes accidental use of real release evidence easier to detect. |
| D09 | Represent the product with diagrams and evidence files, not generated product UI. | Avoids presenting fictional interfaces as working Microsoft product screens. |
| D10 | Use Gemini only for narration support and Veo only for optional intro or outro polish. | Keeps Google AI outside the product proof and makes the production method transparent. |
| D11 | Generate captions from frozen scene text and test word-for-word parity. | Prevents transcription drift in product terms such as `ReleaseChangeV1`. |
| D12 | Mark live Copilot Studio, SharePoint, Power Automate, and Work IQ proof as `OWNER-TODO`. | Tenant work is outside this public-package scope and must not be fabricated. |
| D13 | Package the validation and policy engines as a Python MCP server and a Declarative Agent app package. | Fits the hackathon's "Enterprise Agents" track requirements and earns higher rating by showing ATK compatibility. |
| D14 | Treat the Copilot Studio `ContentValidationError` at `2026-06-13T00:08:03.750Z` as a failed release gate. | Literal JSON braces in Agent instructions were parsed as expression segments and prevented a valid runtime response. |
| D15 | Specify structured Agent output as brace-free required fields rather than embedding a literal JSON object in instructions. | Preserves the JSON response contract without triggering Copilot Studio expression parsing. |
| D16 | Require zero Agent diagnostics before publish and a parseable response before recording a test as passed. | Successfully submitting a prompt does not prove the Agent executed the contract. |
| D17 | Stop Antigravity evidence capture immediately on `ExpressionSegment` or `ContentValidationError`. | Invalid Agent configuration must not be represented as working tenant evidence. |
| D18 | Use `kotorn/governed-release-copilot` as the single public submission repository and treat `bpa-release-note-agent` as an allowlisted donor only. | Avoids deadline risk, split storytelling, and mixed public histories. |
| D19 | Keep the governed synthetic `ReleaseChangeV1` schema as the active public contract. | Prevents last-minute schema broadening and keeps canonical hash behavior stable. |
| D20 | Add `Submit-BpaReleaseChange` as a supplemental PowerShell submission boundary rather than the primary product story. | Preserves the deterministic MCP and Declarative Agent package as the public center while still proving the local loopback submission path. |
| D21 | Label live Copilot Studio publish, fresh SharePoint citation, and Work IQ runtime retrieval as `not live-verified in final run` unless owner-supplied evidence refreshes them. | Submission honesty matters more than over-claiming tenant behavior under deadline pressure. |

## Owner TODO

- Capture sanitized live evidence of the Microsoft IQ integration.
- Add the final public demo-video URL to the submission form.
- Complete the hackathon form using [docs/submission.md](docs/submission.md).
