"""HMAC-SHA256 signing for Mullvald key payloads."""

from __future__ import annotations

import hmac
from hashlib import sha256


def sign_payload(payload: bytes, seed: bytes) -> str:
    """Return the hex HMAC-SHA256 of *payload* under *seed*."""
    return hmac.new(seed, payload, sha256).hexdigest()


def encode_key(payload: bytes, signature: str) -> str:
    """Assemble the human-facing key string.

    Format: MVK1-<base32(payload)>-<sig[0:16]>
    The signature is truncated to 16 hex chars — enough for the
    validator's constant-time check, short enough to keep keys legible.
    """
    import base64

    body = base64.b32encode(payload).decode("ascii").rstrip("=")
    return f"{body}-{signature[:16]}"


def decode_key(key: str) -> tuple[bytes, str]:
    """Split a key string back into (payload, signature_prefix)."""
    import base64

    body, _, sig = key.rpartition("-")
    pad = "=" * (-len(body) % 8)
    payload = base64.b32decode(body + pad)
    return payload, sig