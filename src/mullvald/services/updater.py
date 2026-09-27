"""Opt-in update checker. No-op unless ctx.allow_network is True."""

from __future__ import annotations

import logging
import urllib.request

log = logging.getLogger(__name__)

MANIFEST_URL = "https://updates.mullvald-key-tools.invalid/manifest.json"


def check_for_updates(allow_network: bool, current: str) -> str | None:
    if not allow_network:
        log.debug("network disabled, skipping update check")
        return None
    try:
        with urllib.request.urlopen(MANIFEST_URL, timeout=5) as resp:  # noqa: S310
            import json

            data = json.loads(resp.read().decode("utf-8"))
        latest = data.get("latest")
        if latest and latest != current:
            return latest
    except Exception as exc:  # noqa: BLE001
        log.warning("update check failed: %s", exc)
    return None