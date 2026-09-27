"""Human-facing formatting helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def humanize_expiry(epoch: int) -> str:
    dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def chunk_key(key: str, size: int = 8) -> str:
    return " ".join(key[i : i + size] for i in range(0, len(key), size))