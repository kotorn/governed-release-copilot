from __future__ import annotations

import json

from governed_release_copilot.cli import (
    EXIT_CLOSED,
    EXIT_DUPLICATE,
    EXIT_READY,
    main,
)

from conftest import SAMPLES, load_sample


def test_cli_ready_output_is_structured(capsys) -> None:
    result = main([str(SAMPLES / "valid.json")])
    output = json.loads(capsys.readouterr().out)

    assert result == EXIT_READY
    assert output["decision"] == "ReadyForApproval"


def test_cli_needs_input_fails_closed(capsys) -> None:
    result = main([str(SAMPLES / "missing-fields.json")])
    output = json.loads(capsys.readouterr().out)

    assert result == EXIT_CLOSED
    assert output["decision"] == "NeedsInput"


def test_cli_duplicate_uses_registry(tmp_path, capsys) -> None:
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps([load_sample("valid.json")["changeHash"]]),
        encoding="utf-8",
    )

    result = main(
        [
            "--registry",
            str(registry),
            str(SAMPLES / "duplicate.json"),
        ]
    )
    output = json.loads(capsys.readouterr().out)

    assert result == EXIT_DUPLICATE
    assert output["decision"] == "Duplicate"


def test_cli_rejection_fails_closed(capsys) -> None:
    result = main([str(SAMPLES / "rejected.json")])
    output = json.loads(capsys.readouterr().out)

    assert result == EXIT_CLOSED
    assert output["decision"] == "Rejected"

