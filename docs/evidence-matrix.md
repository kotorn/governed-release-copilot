# Evidence Matrix

This matrix is the source of truth for claims used in the public narration.
Tenant behavior is never claimed from synthetic evidence.

| Claim ID | Narration claim | Evidence type | Evidence |
|---|---|---|---|
| C01 | Release evidence is normalized into one versioned contract. | Schema and sample | [ReleaseChangeV1 schema](../schema/ReleaseChangeV1.schema.json), [valid sample](../samples/valid.json) |
| C02 | The architecture separates validation, AI drafting, human approval, publication, and Q&A. | Architecture | [Mermaid source](architecture.mmd), [rendered PNG](architecture.png) |
| C03 | Schema and canonical hash checks run before a request is ready for approval. | Source and test | [Validator](../src/governed_release_copilot/validator.py), [validator tests](../tests/test_validator.py) |
| C03b | The supplemental PowerShell submitter blocks invalid payloads before any POST. | Source and test | [Submit-BpaReleaseChange module](../src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psm1), [Pester tests](../tests/powershell/SubmitBpaReleaseChange.Tests.ps1) |
| C04 | Missing evidence returns `NeedsInput`; failed evidence returns `Rejected`. | Source and test | [Policy](../src/governed_release_copilot/policy.py), [policy tests](../tests/test_policy.py) |
| C05 | A duplicate canonical hash is blocked as `Duplicate`. | Test and fixture | [Duplicate policy test](../tests/test_policy.py), [duplicate sample](../samples/duplicate.json) |
| C06 | `ReadyForApproval` still requires a human decision before publication. | Architecture and decision log | [Architecture](architecture.mmd), [decision D04](../DECISIONS.md) |
| C07 | Approved SharePoint notes are the intended knowledge boundary for citation-backed Q&A. | Architecture | [Architecture](architecture.mmd) |
| C08 | Work IQ supplies context but does not replace approved release evidence. | Architecture and scope decision | [Architecture](architecture.mmd), [decision D12](../DECISIONS.md) |
| C09 | The public package is synthetic and guarded by privacy, pytest, and gitleaks checks. | Source, tests, and CI | [Privacy scanner](../scripts/privacy_scan.py), [privacy tests](../tests/test_privacy_scan.py), [CI workflow](../.github/workflows/verify.yml) |
| C10 | Narration and captions come from the same frozen text. | Assets and test | [Video package](video/README.md), [documentation tests](../tests/test_docs.py) |
| C11 | Gemini and Veo are production aids, not evidence of product behavior. | Transparency decision | [README transparency note](../README.md), [decision D10](../DECISIONS.md) |
| C12 | Live Microsoft tenant and IQ proof remains an owner-supplied submission artifact. | Scope decision | [Owner TODO](../DECISIONS.md), [submission draft](submission.md) |
| C13 | Fresh tenant proof must be labeled honestly when it is not re-verified in the final run. | Scope decision | [Decision D21](../DECISIONS.md), [submission draft](submission.md) |

## Narration Coverage

| Scene | Claims |
|---|---|
| [01 Problem](video/scene-01-problem.txt) | C01, C09 |
| [02 Architecture](video/scene-02-architecture.txt) | C02, C06 |
| [03 Validation](video/scene-03-validation.txt) | C03, C03b, C05 |
| [04 AI reasoning](video/scene-04-ai-reasoning.txt) | C04, C06 |
| [05 Approval](video/scene-05-approval.txt) | C06 |
| [06 Published knowledge](video/scene-06-published-knowledge.txt) | C07 |
| [07 Agent and Work IQ](video/scene-07-agent-work-iq.txt) | C07, C08, C12, C13 |
| [08 Reliability and close](video/scene-08-reliability-close.txt) | C09, C10, C11, C13 |
