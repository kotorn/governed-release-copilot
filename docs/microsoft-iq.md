# Microsoft IQ Integration

The Copilot Studio solution includes two Work IQ actions:

- Work IQ Copilot, for organizational Copilot context.
- Work IQ User, for user-scoped organizational context.

Both actions are represented as Model Context Protocol task dialogs and remain
inside the solution when the release-note instructions are imported.

## Retrieval Decision Tree

1. When Work IQ retrieval is available, use it to locate supporting context and
   answer with a citation to the approved release note.
2. When policy blocks retrieval, retain the Work IQ configuration as integration
   evidence and use the approved SharePoint knowledge source.
3. When channel publication is blocked, demonstrate the same behavior in the
   Copilot Studio test canvas.

Work IQ is never allowed to convert a Draft or rejected record into published
truth.

For the hackathon submission, the static solution export is enough to prove
Microsoft IQ integration even if live retrieval is policy-blocked. Runtime
retrieval is a bonus, not a blocking dependency.
