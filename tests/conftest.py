from __future__ import annotations

import json
from pathlib import Path

import pytest

from governed_release_copilot.validator import load_schema

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "samples"


@pytest.fixture(scope="session")
def schema() -> dict:
    return load_schema(ROOT / "schema" / "ReleaseChangeV1.schema.json")


def load_sample(name: str) -> dict:
    with (SAMPLES / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)

