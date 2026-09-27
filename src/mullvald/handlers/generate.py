"""Generate handler — CLI/GUI-facing key production."""

from __future__ import annotations

import logging
from pathlib import Path

from mullvald.core.context import KeygenContext
from mullvald.core.signing import encode_key
from mullvald.models.key import KeyTier

log = logging.getLogger(__name__)


class GenerateHandler:
    def __init__(self, ctx: KeygenContext) -> None:
        self._ctx = ctx

    def run(self, *, tier: str, days: int, count: int, out_path: Path | None) -> list[str]:
        if count < 1 or count > 10_000:
            raise ValueError("count must be between 1 and 10000")
        if days < 1:
            raise ValueError("days must be positive")

        tier_enum = KeyTier(tier)
        keys: list[str] = []
        for serial in range(1, count + 1):
            minted = self._ctx.engine.mint(tier_enum, days=days, serial=serial)
            keys.append(encode_key(minted.payload, minted.signature))

        if out_path is not None:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text("\n".join(keys) + "\n", encoding="utf-8")
            log.info("wrote %d keys to %s", len(keys), out_path)

        return keys