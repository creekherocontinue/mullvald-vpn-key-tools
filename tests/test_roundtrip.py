"""Round-trip: mint a key, encode it, decode it, verify it."""

from __future__ import annotations

from pathlib import Path

from mullvald.core.context import KeygenContext
from mullvald.core.engine import KeygenEngine
from mullvald.core.signing import decode_key, encode_key
from mullvald.handlers.validate import ValidateHandler
from mullvald.models.key import KeyTier


def _ctx() -> KeygenContext:
    ctx = KeygenContext.load(None, allow_network=False)
    ctx.engine = KeygenEngine(ctx)
    return ctx


def test_mint_encode_decode_verify() -> None:
    ctx = _ctx()
    minted = ctx.engine.mint(KeyTier.PLUS, days=30, serial=42)
    key_str = encode_key(minted.payload, minted.signature)

    payload, sig = decode_key(key_str)
    assert payload == minted.payload
    assert sig == minted.signature[:16]

    result = ValidateHandler(ctx).run(key_str)
    assert result.valid, result.reason
    assert result.tier is KeyTier.PLUS


def test_tampered_key_fails() -> None:
    ctx = _ctx()
    minted = ctx.engine.mint(KeyTier.BASIC, days=1, serial=1)
    key_str = encode_key(minted.payload, minted.signature)

    # Flip a character in the body to break the CRC.
    tampered = key_str[:5] + ("A" if key_str[5] != "A" else "B") + key_str[6:]
    result = ValidateHandler(ctx).run(tampered)
    assert not result.valid