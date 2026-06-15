# Hackathon Submission Draft

## Project Title

Governed Release Copilot

## Tagline

Evidence in. Approval enforced. Trusted answers out.

## Problem Solved

Business application changes often leave evidence across workflow tools,
forms, SharePoint, and database work. Release communication then becomes slow,
inconsistent, and difficult to audit. Governed Release Copilot creates one
evidence-backed path from a structured change contract to approved knowledge
and citation-backed answers.

## Features And Functionality

- `ReleaseChangeV1` JSON Schema for normalized change evidence.
- Canonical SHA-256 hash for retry-safe duplicate detection.
- Deterministic fail-closed outcomes for ready, missing, duplicate, and
  rejected submissions.
- Optional PowerShell submission boundary that validates the public contract
  before any POST.
- Model Context Protocol (MCP) server exposing validation and decision tools.
- Declarative Agent app package (manifest.json, declarativeAgent.json, API plugin, OpenAPI spec) for Teams / Microsoft 365 sideloading.
- Microsoft 365 Agents Toolkit configuration for developer experience.
- Structured AI drafting boundary followed by human approval.
- Approved SharePoint release notes as the intended knowledge source.
- Copilot Studio Q&A with citations from approved notes.
- Python pytest, privacy scanning, and all-ref gitleaks CI.

## Microsoft Technologies And IQ

The target enterprise architecture uses Microsoft 365 Copilot with the Microsoft 365 Agents Toolkit (ATK) for Declarative Agent (DA) and Model Context Protocol (MCP) integration, Copilot Studio for agent experiences, Power Automate for orchestration and approval, SharePoint for approved publication, and Work IQ for organizational context. Work IQ may enrich retrieval, but it does not override the approved release-note boundary.

**OWNER-TODO:** attach sanitized live evidence of the Microsoft IQ
configuration and citation behavior before submission.

If that evidence is not refreshed in the final run, describe it as
`not live-verified in final run`.

## Reliability And Safety

The public implementation validates schema and canonical hash before
`ReadyForApproval`, blocks duplicate hashes, returns `NeedsInput` for
incomplete evidence, and rejects failed tests. Public fixtures are synthetic.
Privacy and secret scans run locally and in CI.

## Public Repository

https://github.com/kotorn/governed-release-copilot

## Architecture Image

`docs/architecture.png`

## Demo Video

**OWNER-TODO:** add the final public video URL.

Use the existing backup MP4 first if no polished cut is ready. The public repo
must not claim a fresher tenant demo than the owner can actually provide.

## Team And Learning Profile

**OWNER-TODO:** add the participant and Microsoft Learn profile information in
the official form.
