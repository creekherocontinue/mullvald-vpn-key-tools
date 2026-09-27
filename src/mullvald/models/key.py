"""Key model and tier enum."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class KeyTier(str, Enum):
    BASIC = "basic"
    PLUS = "plus"
    PRO = "pro"
    TEAM = "team"


@dataclass(slots=True, frozen=True)
class MullvaldKey:
    tier: KeyTier
    issued_at: int
    expires_at: int
    serial: int
    payload: bytes
    signature: str

    def __str__(self) -> str:
        from mullvald.core.signing import encode_key

        return encode_key(self.payload, self.signature)