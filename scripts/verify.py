"""Run the complete local verification gate without downloading dependencies."""

from __future__ import annotations

import shutil
import subprocess
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / ".pytest-results.xml"
REQUIRED_FILES = [
    "README.md",
    "DECISIONS.md",
    "accepted-hashes.json",
    "docs/architecture.mmd",
    "docs/architecture.png",
    "docs/evidence-matrix.md",
    "docs/submission.md",
    "docs/project-overview.md",
    "docs/FEATURES.md",
    "docs/RELEASECHANGEV1-CONTRACT.md",
    "docs/STATE-MODEL.md",
    "docs/PRIVACY-SCAN-RULES.md",
    "docs/PR-CHECKLIST.md",
    "docs/flow-contract.md",
    "docs/demo-runsheet.md",
    "docs/judging-evidence-matrix.md",
    "docs/microsoft-iq.md",
    "docs/agent-instructions.md",
    "docs/video/README.md",
    "schema/ReleaseChangeV1.schema.json",
    "src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psd1",
    "src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psm1",
    "tests/helpers/mock_trigger.py",
    "tests/powershell/SubmitBpaReleaseChange.Tests.ps1",
]


def run(*command: str) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def verify_required_files() -> None:
    missing = [
        path for path in REQUIRED_FILES if not (ROOT / path).exists()
    ]
    if missing:
        raise SystemExit(
            "required file gate failed: " + ", ".join(sorted(missing))
        )


def verify_pytest() -> None:
    run(
        sys.executable,
        "-m",
        "pytest",
        "-q",
        f"--junitxml={RESULTS}",
    )
    root = ET.parse(RESULTS).getroot()
    skipped = sum(
        int(suite.attrib.get("skipped", "0"))
        for suite in root.iter("testsuite")
    )
    failures = sum(
        int(suite.attrib.get("failures", "0"))
        + int(suite.attrib.get("errors", "0"))
        for suite in root.iter("testsuite")
    )
    RESULTS.unlink(missing_ok=True)
    if skipped or failures:
        raise SystemExit(
            f"pytest gate failed: failures={failures}, skipped={skipped}"
        )


def verify_pester() -> None:
    if not (ROOT / "tests" / "powershell").exists():
        return

    executable = shutil.which("pwsh")
    if not executable:
        raise SystemExit("pwsh is required for PowerShell integration tests")

    command = (
        "Import-Module Pester -RequiredVersion 5.7.1 -Force; "
        "$result = Invoke-Pester -Path 'tests/powershell' -PassThru -Output Detailed; "
        "if ($result.FailedCount -ne 0 -or $result.PassedCount -eq 0) { exit 1 }"
    )
    run(executable, "-NoLogo", "-NoProfile", "-Command", command)


def verify_gitleaks() -> None:
    executable = shutil.which("gitleaks")
    if not executable:
        raise SystemExit("gitleaks 8.30.1 is required")
    version = subprocess.run(
        [executable, "version"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    if "8.30.1" not in version:
        go = shutil.which("go")
        metadata = ""
        if go:
            metadata = subprocess.run(
                [go, "version", "-m", executable],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        if not re.search(r"gitleaks/v8\s+v8\.30\.1\b", metadata):
            raise SystemExit(
                f"expected gitleaks 8.30.1, found {version.strip()}"
            )
    run(executable, "dir", "--no-banner", "--redact", ".")
    run(
        executable,
        "git",
        "--no-banner",
        "--redact",
        "--log-opts=--all",
        ".",
    )


def main() -> int:
    verify_required_files()
    run(sys.executable, "scripts/privacy_scan.py", "--history")
    verify_pytest()
    verify_pester()
    verify_gitleaks()
    print("All verification checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
