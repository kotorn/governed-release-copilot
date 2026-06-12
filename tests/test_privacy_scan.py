from __future__ import annotations

from scripts.privacy_scan import scan_text


def test_synthetic_text_is_allowed() -> None:
    assert scan_text(
        "sample",
        "RN-SYNTH-0001 uses artifact://synthetic/workflow/before.json",
    ) == []


def test_email_shape_is_rejected() -> None:
    unsafe = "owner" + "@" + "example" + ".com"

    assert scan_text("sample", unsafe) == ["sample: email or UPN"]


def test_tenant_domain_is_rejected() -> None:
    unsafe = "https://tenant." + "share" + "point.com/sites/demo"

    assert scan_text("sample", unsafe) == ["sample: tenant domain"]


def test_absolute_user_path_is_rejected() -> None:
    unsafe = "C:\\" + "Users" + "\\person\\secret.txt"

    assert scan_text("sample", unsafe) == ["sample: absolute user path"]

