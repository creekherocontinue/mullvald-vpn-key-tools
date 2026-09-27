# Security Policy

## Scope

`mullvald-vpn-key-tools` is an offline key generation and validation
utility. It does not ship a Mullvald VPN client, does not modify the
client binary, and does not phone home. The attack surface we care
about is:

- Key material leaking to disk in plaintext when it shouldn't.
- The `services/` layer making network calls without explicit consent.
- Dependency supply-chain issues in the pinned toolchain.

## Reporting a vulnerability

Open a private security advisory on the GitHub repo, or email
`security@mullvald-key-tools.invalid` (placeholder — replace with the
real maintainer inbox before publishing). Include:

- Repo commit hash.
- Python version and OS build.
- Minimal reproduction.
- Whether the issue is exploitable offline or requires a hostile
  config file.

We aim to acknowledge within 72 hours and ship a patch within 14 days
for high-severity issues.

## What is out of scope

- Anything requiring physical access to the machine.
- Mullvald VPN client bugs — report those upstream.
- "My generated key got banned" — that's a client-side enforcement
  question, not a tooling vulnerability.

## Hardening notes for users

- Run the generator on a machine you control.
- Keep `config/local.toml` out of version control (it's gitignored).
- The `--no-network` flag disables every outbound call in `services/`.