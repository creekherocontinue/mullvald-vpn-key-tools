"""Payload derivation: field layout, CRC guard, version rejection."""

from __future__ import annotations

import pytest

from mullvald.core.derivation import PAYLOAD_VERSION, derive_payload, parse_payload
from mullvald.models.key import KeyTier


def test_derive_parse_roundtrip() -> None:
    payload = derive_payload(
        tier=KeyTier.PRO,
        issued_at=1_730_000_000,
        expires_at=1_732_592_000,
        serial=7,
        prefix="MVR",
    )
    fields = parse_payload(payload)
    assert fields["version"] == PAYLOAD_VERSION
    assert fields["tier"] == "pro"
    assert fields["serial"] == "7"
    assert fields["prefix"] == "MVR"


def test_bad_crc_rejected() -> None:
    payload = derive_payload(
        tier=KeyTier.BASIC,
        issued_at=1,
        expires_at=2,
        serial=3,
        prefix="MVB",
    )
    corrupted = payload[:-1] + (b"0" if payload[-1:] != b"0" else b"1")
    with pytest.raises(ValueError, match="crc"):
        parse_payload(corrupted)


def test_unknown_version_rejected() -> None:
    with pytest.raises(ValueError, match="version"):
        parse_payload(b"MVK9|basic|1|2|3|MVB|00000000")
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>