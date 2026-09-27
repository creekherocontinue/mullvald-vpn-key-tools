"""Local keystore — append-only JSONL of minted keys.

Persists to `keys/keystore.jsonl`. Each record is one line:
`{"key": "...", "tier": "plus", "issued_at": 1730000000, "serial": 7}`
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

DEFAULT_STORE = Path("keys/keystore.jsonl")


class KeyStore:
    def __init__(self, path: Path = DEFAULT_STORE) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, key: str, tier: str, issued_at: int, serial: int) -> None:
        record = {"key": key, "tier": tier, "issued_at": issued_at, "serial": serial}
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
        log.debug("keystore += serial=%d tier=%s", serial, tier)

    def iter_records(self):
        if not self._path.exists():
            return
        with self._path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)