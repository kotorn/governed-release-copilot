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


def run(*command: str) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


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
    run(sys.executable, "scripts/privacy_scan.py", "--history")
    verify_pytest()
    verify_gitleaks()
    print("All verification checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
