# Contributing to mullvald-vpn-key-tools

Thanks for wanting to help push the Mullvald VPN Key Generator forward.
This repo is a Windows desktop utility that generates, validates, and
manages Mullvald-format license keys for the Mullvald VPN client. It is
maintained by hobbyists, reverse engineers, and people who like their
tooling offline and auditable.

## Ground rules

- Keep the generator **offline-first**. No telemetry, no phone-home,
  no network calls in the core path. Anything that touches the network
  lives in `src/mullvald/services/` and must be opt-in.
- Match the existing layer boundaries. `bootstrap/` wires things up,
  `core/` does the math, `handlers/` exposes features, `services/`
  talks to the outside world, `models/` holds schemas, `utils/` holds
  pure helpers.
- Every new key format needs a fixture in `tests/fixtures/` and a
  round-trip test. If it doesn't round-trip, it doesn't ship.

## Dev setup

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m mullvald --selfcheck
```

## Style

- Python 3.12+, type hints everywhere, `ruff` + `mypy --strict`.
- No global mutable state. Pass a `KeygenContext` if you need config.
- Logging via `mullvald.utils.logging_setup`, never bare `print`.

## Pull requests

- One feature per PR. Small diffs get merged fast.
- Include the exact command you ran to verify.
- If you add a new key prefix, update `docs/key_formats.md` and bump
  `models/version.py`.

## Reporting key-format breakage

If a Mullvald client update invalidates a key format, open an issue
tagged `format-drift` with the client build number and the failing
fixture output. Do **not** paste full keys from a paid account.