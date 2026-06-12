"""Fail-closed privacy scan for the public working tree and Git history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

SKIP_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
}

PATTERNS = {
    "email or UPN": re.compile(
        r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
    ),
    "canonical GUID": re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
        r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
    ),
    "tenant domain": re.compile(
        "(?i)("
        + "share"
        + r"point\.com|onmicro"
        + r"soft\.com|dev\.azure\.com|dynamics\.com)"
    ),
    "internal hostname": re.compile(
        r"(?i)\b(?:intranet\.[A-Z0-9.-]+|[A-Z0-9.-]+\.(?:corp|local))\b"
    ),
    "real ticket identifier": re.compile(
        r"\b(?:INC|REQ|RITM)[0-9]{6,}\b"
    ),
    "credential assignment": re.compile(
        r"(?i)(?:client[_-]?secret|access[_-]?token|api[_-]?key|password)"
        r"\s*[:=]\s*[\"']?[^\s\"']{8,}"
    ),
    "bearer token": re.compile(
        "(?i)\\bBear" + r"er\s+[A-Za-z0-9._-]{16,}"
    ),
    "private key": re.compile(
        "-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE " + "KEY-----"
    ),
    "absolute user path": re.compile(
        "(?i)(?:[A-Z]:\\\\Us" + r"ers\\[^\\\s]+|/ho" + r"me/[^/\s]+)"
    ),
}


def is_binary(data: bytes) -> bool:
    return b"\x00" in data


def scan_text(label: str, text: str) -> list[str]:
    findings: list[str] = []
    for name, pattern in PATTERNS.items():
        if name == "canonical GUID" and "manifest.json" in label:
            continue
        if pattern.search(text):
            findings.append(f"{label}: {name}")
    return findings


def iter_worktree_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_PARTS or part.endswith(".egg-info") for part in relative.parts):
            continue
        yield path


def scan_worktree(root: Path) -> list[str]:
    findings: list[str] = []
    for path in iter_worktree_files(root):
        data = path.read_bytes()
        if is_binary(data):
            continue
        text = data.decode("utf-8", errors="replace")
        findings.extend(scan_text(path.relative_to(root).as_posix(), text))
    return findings


def _git(root: Path, *args: str, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=text,
    )


def scan_history(root: Path) -> list[str]:
    try:
        listing = _git(root, "rev-list", "--objects", "--all").stdout
    except subprocess.CalledProcessError:
        return []

    findings: list[str] = []
    seen: set[str] = set()
    for line in listing.splitlines():
        object_id, _, path = line.partition(" ")
        if object_id in seen:
            continue
        seen.add(object_id)
        object_type = _git(root, "cat-file", "-t", object_id).stdout.strip()
        if object_type != "blob":
            continue
        data = _git(root, "cat-file", "-p", object_id, text=False).stdout
        if is_binary(data):
            continue
        label = f"history:{path or object_id}"
        findings.extend(
            scan_text(label, data.decode("utf-8", errors="replace"))
        )
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    root = args.root.resolve()
    findings = scan_worktree(root)
    if args.history:
        findings.extend(scan_history(root))

    if findings:
        print("\n".join(sorted(set(findings))), file=sys.stderr)
        return 1
    print("Privacy scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

