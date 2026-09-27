"""Runtime context: config, paths, and feature flags."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mullvald.models.config import MullvaldConfig


@dataclass(slots=True)
class KeygenContext:
    """Everything a handler needs to do its job.

    Attributes:
        config: Parsed Mullvald config (tier table, prefixes, seed path).
        allow_network: If False, services must not open sockets.
        engine: Injected by bootstrap after construction; typed loosely
            here to avoid a circular import with core.engine.
    """

    config: MullvaldConfig
    allow_network: bool = False
    engine: Any = None
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Path | None, allow_network: bool) -> "KeygenContext":
        if config_path is None:
            config_path = Path("config/default.toml")
        if config_path.exists():
            with config_path.open("rb") as fh:
                raw = tomllib.load(fh)
        else:
            raw = {}
        return cls(config=MullvaldConfig.model_validate(raw), allow_network=allow_network)