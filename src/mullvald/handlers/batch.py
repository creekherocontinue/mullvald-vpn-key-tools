"""Batch handler — validate a file of keys, write a summary."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from mullvald.core.context import KeygenContext
from mullvald.handlers.validate import ValidateHandler


@dataclass(slots=True)
class BatchSummary:
    valid: int
    invalid: int
    total: int


class BatchHandler:
    def __init__(self, ctx: KeygenContext) -> None:
        self._ctx = ctx

    def run(self, input_file: Path, out_path: Path) -> BatchSummary:
        validator = ValidateHandler(self._ctx)
        lines = [ln.strip() for ln in input_file.read_text(encoding="utf-8").splitlines() if ln.strip()]

        valid_lines: list[str] = []
        invalid_lines: list[str] = []
        for line in lines:
            result = validator.run(line)
            (valid_lines if result.valid else invalid_lines).append(line)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            "\n".join(f"OK   {k}" for k in valid_lines)
            + "\n"
            + "\n".join(f"FAIL {k}" for k in invalid_lines)
            + "\n",
            encoding="utf-8",
        )
        return BatchSummary(valid=len(valid_lines), invalid=len(invalid_lines), total=len(lines))