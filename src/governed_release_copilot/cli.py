"""CLI for deterministic ReleaseChangeV1 evaluation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .policy import Decision, evaluate_release
from .validator import load_schema

EXIT_READY = 0
EXIT_CLOSED = 2
EXIT_DUPLICATE = 3
EXIT_USAGE = 4


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grc-validate",
        description="Evaluate one synthetic ReleaseChangeV1 payload.",
    )
    parser.add_argument("payload", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=repository_root() / "schema" / "ReleaseChangeV1.schema.json",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        help="Optional JSON array of previously accepted changeHash values.",
    )
    return parser


def _read_object(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("payload root must be a JSON object")
    return value


def _read_registry(path: Path | None) -> set[str]:
    if path is None:
        return set()
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("registry must be a JSON array of strings")
    return set(value)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        payload = _read_object(args.payload)
        schema = load_schema(args.schema)
        registry = _read_registry(args.registry)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error), "decision": "UsageError"}))
        return EXIT_USAGE

    evaluation = evaluate_release(payload, schema, registry)
    print(
        json.dumps(
            {
                "decision": evaluation.decision.value,
                "reasons": list(evaluation.reasons),
                "releaseId": payload.get("releaseId"),
                "changeHash": payload.get("changeHash"),
            },
            sort_keys=True,
        )
    )

    if evaluation.decision is Decision.READY_FOR_APPROVAL:
        return EXIT_READY
    if evaluation.decision is Decision.DUPLICATE:
        return EXIT_DUPLICATE
    return EXIT_CLOSED


if __name__ == "__main__":
    sys.exit(main())

