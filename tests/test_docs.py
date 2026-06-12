from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "docs" / "video"
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _words(text: str) -> list[str]:
    return re.findall(r"\b[\w'-]+\b", text)


def _srt_text(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    content = [
        line
        for line in lines
        if line
        and not line.isdigit()
        and "-->" not in line
    ]
    return " ".join(content)


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _local_markdown_links(path: Path) -> list[Path]:
    destinations: list[Path] = []
    for target in LINK.findall(path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        clean = target.split("#", 1)[0]
        destinations.append((path.parent / clean).resolve())
    return destinations


def test_all_local_markdown_links_resolve() -> None:
    markdown_files = [ROOT / "README.md", ROOT / "DECISIONS.md"]
    markdown_files.extend((ROOT / "docs").rglob("*.md"))

    broken = [
        f"{path.relative_to(ROOT)} -> {target}"
        for path in markdown_files
        for target in _local_markdown_links(path)
        if not target.exists()
    ]

    assert broken == []


def test_video_has_eight_verbatim_scene_caption_pairs() -> None:
    scenes = sorted(VIDEO.glob("scene-*.txt"))
    captions = sorted(VIDEO.glob("scene-*.srt"))

    assert len(scenes) == 8
    assert len(captions) == 8
    for scene, caption in zip(scenes, captions, strict=True):
        assert scene.stem == caption.stem
        assert _normalized(scene.read_text(encoding="utf-8")) == _normalized(
            _srt_text(caption)
        )


def test_frozen_narration_is_between_550_and_600_words() -> None:
    total = sum(
        len(_words(path.read_text(encoding="utf-8")))
        for path in VIDEO.glob("scene-*.txt")
    )

    assert 550 <= total <= 600


def test_evidence_matrix_covers_every_scene() -> None:
    matrix = (ROOT / "docs" / "evidence-matrix.md").read_text(
        encoding="utf-8"
    )

    for scene in VIDEO.glob("scene-*.txt"):
        assert scene.name in matrix


def test_architecture_png_is_rendered_at_submission_size() -> None:
    png = ROOT / "docs" / "architecture.png"
    data = png.read_bytes()

    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", data[16:24])
    assert width >= 1200
    assert height >= 600


def test_pronunciation_notes_cover_required_terms() -> None:
    guide = (VIDEO / "README.md").read_text(encoding="utf-8")

    assert '`BPA`: "B P A"' in guide
    assert '`Work IQ`: "Work I Q"' in guide
    assert '`ReleaseChangeV1`: "Release Change Version One"' in guide
