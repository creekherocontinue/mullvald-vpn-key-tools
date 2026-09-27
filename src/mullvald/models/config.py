"""Config schema for the Mullvald key generator."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from mullvald.models.key import KeyTier


class MullvaldConfig(BaseModel):
    seed_path: Path = Field(default=Path("config/seed.bin"))
    prefixes: dict[KeyTier, str] = Field(
        default_factory=lambda: {
            KeyTier.BASIC: "MVB",
            KeyTier.PLUS: "MVP",
            KeyTier.PRO: "MVR",
            KeyTier.TEAM: "MVT",
        }
    )
    default_days: int = 30
    max_batch: int = 10_000

    def prefix_for(self, tier: KeyTier) -> str:
        return self.prefixes.get(tier, "MVX")