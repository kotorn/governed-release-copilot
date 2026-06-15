# Privacy Scan Rules

The public repository and final rough cut must stay synthetic. The scan rules
exist to stop accidental leakage before review or submission.

## Blocked Content

- Real email addresses and UPNs
- Tenant domains, tenant URLs, and environment URLs
- Canonical Microsoft GUIDs that identify real environments, sites, or apps
- Absolute internal filesystem paths
- Credentials, PATs, tokens, keys, certificates, or connection strings
- Production screenshots, bookmarks, notifications, avatars, or browser
  profile names that expose real identities
- Real ticket numbers or live business identifiers that are not meant for
  public release

## Review Rules

- Public samples use `RN-SYNTH-` identifiers only.
- Frame-level privacy review must inspect tab title, browser profile, avatar,
  bookmarks, and notification area.
- A screenshot is not enough if the frame contains a risky browser state.
- If a field looks like production data, treat it as sensitive until proven
  otherwise.

## Tooling Rules

- `scripts/privacy_scan.py` is the primary public gate.
- `scripts/verify.ps1` is the PowerShell wrapper for the same acceptance gate.
- `gitleaks` covers the working tree and history.
- The final video uses a clean Chrome profile and Windows Do Not Disturb.
