"""Validate handler — checks a single key against the loaded seed."""

from __future__ import annotations

from dataclasses import dataclass

from mullvald.core.context import KeygenContext
from mullvald.core.derivation import parse_payload
from mullvald.core.signing import decode_key, sign_payload
from mullvald.models.key import KeyTier


@dataclass(slots=True)
class ValidationResult:
    valid: bool
    reason: str
    tier: KeyTier | None = None
    expires_at: int | None = None


class ValidateHandler:
    def __init__(self, ctx: KeygenContext) -> None:
        self._ctx = ctx

    def run(self, key: str) -> ValidationResult:
        try:
            payload, sig_prefix = decode_key(key.strip())
        except Exception as exc:  # noqa: BLE001 — surface any decode failure
            return ValidationResult(False, f"decode error: {exc}")

        try:
            fields = parse_payload(payload)
        except ValueError as exc:
            return ValidationResult(False, str(exc))

        expected = sign_payload(payload, self._ctx.engine._load_seed())[:16]
        if expected != sig_prefix:
            return ValidationResult(False, "signature mismatch")

        return ValidationResult(
            valid=True,
            reason=f"valid {fields['tier']} key",
            tier=KeyTier(fields["tier"]),
            expires_at=int(fields["expires_at"]),
        )