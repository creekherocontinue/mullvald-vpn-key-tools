"""Keygen engine — orchestrates seed loading, derivation, and signing."""

from __future__ import annotations

import hmac
import logging
import time
from hashlib import sha256

from mullvald.core.context import KeygenContext
from mullvald.core.derivation import derive_payload
from mullvald.core.signing import sign_payload
from mullvald.models.key import MullvaldKey, KeyTier

log = logging.getLogger(__name__)


class KeygenEngine:
    """Produces signed Mullvald keys from a seed and a tier spec.

    The engine is stateless across calls except for the loaded seed
    material, which is cached on first use. All operations are pure
    CPU; no I/O after construction.
    """

    def __init__(self, ctx: KeygenContext) -> None:
        self._ctx = ctx
        self._seed: bytes | None = None

    def _load_seed(self) -> bytes:
        if self._seed is None:
            path = self._ctx.config.seed_path
            if path.exists():
                self._seed = path.read_bytes().strip()
            else:
                # Deterministic dev seed so the tool works out of the box.
                self._seed = sha256(b"mullvald-dev-seed-2026").digest()
                log.warning("seed file missing at %s, using dev seed", path)
        return self._seed

    def mint(self, tier: KeyTier, days: int, serial: int) -> MullvaldKey:
        """Mint a single key for the given tier and validity window."""
        issued = int(time.time())
        expires = issued + days * 86_400
        payload = derive_payload(
            tier=tier,
            issued_at=issued,
            expires_at=expires,
            serial=serial,
            prefix=self._ctx.config.prefix_for(tier),
        )
        signature = sign_payload(payload, self._load_seed())
        return MullvaldKey(
            tier=tier,
            issued_at=issued,
            expires_at=expires,
            serial=serial,
            payload=payload,
            signature=signature,
        )

    def verify(self, key: MullvaldKey) -> bool:
        """Constant-time signature check against the loaded seed."""
        expected = sign_payload(key.payload, self._load_seed())
        return hmac.compare_digest(expected, key.signature)

    def selfcheck(self) -> bool:
        """Mint and verify a throwaway key; True if the engine is wired."""
        probe = self.mint(KeyTier.BASIC, days=1, serial=0)
        return self.verify(probe)