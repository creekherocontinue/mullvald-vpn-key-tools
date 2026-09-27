"""Payload derivation: builds the canonical byte string that gets signed.

The payload layout is fixed and versioned so that validators on the
Mullvald side can parse it without a schema lookup:

    MVK1 | tier | issued | expires | serial | prefix | crc32

Fields are pipe-separated ASCII. The trailing CRC32 is over the
preceding bytes and guards against transcription errors when a user
copies a key by hand.
"""

from __future__ import annotations

import zlib

from mullvald.models.key import KeyTier

PAYLOAD_VERSION = "MVK1"


def derive_payload(
    *,
    tier: KeyTier,
    issued_at: int,
    expires_at: int,
    serial: int,
    prefix: str,
) -> bytes:
    head = f"{PAYLOAD_VERSION}|{tier.value}|{issued_at}|{expires_at}|{serial}|{prefix}"
    raw = head.encode("ascii")
    crc = zlib.crc32(raw) & 0xFFFFFFFF
    return raw + f"|{crc:08x}".encode("ascii")


def parse_payload(payload: bytes) -> dict[str, str]:
    """Inverse of :func:`derive_payload`. Raises ValueError on bad CRC."""
    text = payload.decode("ascii")
    body, _, crc = text.rpartition("|")
    if not body or not crc:
        raise ValueError("malformed payload: missing crc")
    if zlib.crc32(body.encode("ascii")) & 0xFFFFFFFF != int(crc, 16):
        raise ValueError("payload crc mismatch")
    version, tier, issued, expires, serial, prefix = body.split("|")
    if version != PAYLOAD_VERSION:
        raise ValueError(f"unsupported payload version {version}")
    return {
        "version": version,
        "tier": tier,
        "issued_at": issued,
        "expires_at": expires,
        "serial": serial,
        "prefix": prefix,
    }