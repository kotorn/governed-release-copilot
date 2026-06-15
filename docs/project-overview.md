# Project Overview

## Governed Release Copilot

Governed Release Copilot turns evidence-backed change requests into a governed
release story.

**Change Evidence → Deterministic Validation → Governed AI Draft → Human Approval → Approved Knowledge → Citation-Grounded Q&A**

The implementation is CLI-first. The private ADO ledger stores the baseline,
feature contract, and exported solution source of truth, while Copilot Studio
UI is treated as a controlled gate for the few actions that cannot be authored
reliably through source files alone.

It is built for BPA work where workflow changes, form updates, SharePoint list
changes, and database changes need the same controlled path:

1. validate evidence
2. draft with governed AI
3. require human approval
4. publish approved notes
5. answer questions from approved knowledge with citations

Azure DevOps keeps the private engineering ledger. SharePoint keeps the
approved publication and the knowledge source that the agent can cite.

## Why It Exists

- Release evidence is often scattered across tools.
- Manual notes are slow to draft and easy to drift.
- AI is useful only when the input, approval, and published truth are governed.
- The competition story must show enterprise reliability, not just a prompt.
- Every UI change must be exported, unpacked, reviewed, and committed before it
  is considered implemented.

## What The Demo Proves

- A synthetic `ReleaseChangeV1` payload is validated before any network call.
- Duplicate hashes stop the flow before damage.
- AI returns structured drafting or `NeedsInput` only after deterministic validation passes.
- Human approval controls publication.
- Approved SharePoint notes become the source for citation-backed Q&A.
- Work IQ adds context without overriding approved truth.
- The repo also documents the feature contract, state model, privacy rules,
  and PR checklist so the story stays repeatable.

## What Judges Should Remember

Evidence in. Approval enforced. Trusted answers out.
