"""Command-line entry point for the Mullvald key generator."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from mullvald.core.engine import KeygenEngine
from mullvald.core.context import KeygenContext
from mullvald.handlers.generate import GenerateHandler
from mullvald.handlers.validate import ValidateHandler
from mullvald.handlers.batch import BatchHandler
from mullvald.utils.logging_setup import configure_logging

console = Console()


@click.group()
@click.option("--config", type=click.Path(path_type=Path), default=None)
@click.option("--no-network", is_flag=True, default=False)
@click.option("-v", "--verbose", count=True)
@click.pass_context
def main(ctx: click.Context, config: Path | None, no_network: bool, verbose: int) -> None:
    """mullvald — offline key generator for Mullvald VPN."""
    configure_logging(verbose)
    ctx.obj = KeygenContext.load(config, allow_network=not no_network)
    ctx.obj.engine = KeygenEngine(ctx.obj)


@main.command("generate")
@click.option("--tier", type=click.Choice(["basic", "plus", "pro", "team"]), default="plus")
@click.option("--days", type=int, default=30)
@click.option("--count", type=int, default=1)
@click.option("--out", type=click.Path(path_type=Path), default=None)
@click.pass_obj
def generate_cmd(ctx: KeygenContext, tier: str, days: int, count: int, out: Path | None) -> None:
    """Generate one or more Mullvald keys."""
    handler = GenerateHandler(ctx)
    keys = handler.run(tier=tier, days=days, count=count, out_path=out)
    for k in keys:
        console.print(f"[green]{k}[/green]")


@main.command("validate")
@click.argument("key")
@click.pass_obj
def validate_cmd(ctx: KeygenContext, key: str) -> None:
    """Validate a single Mullvald key."""
    result = ValidateHandler(ctx).run(key)
    style = "green" if result.valid else "red"
    console.print(f"[{style}]{result.reason}[/{style}]")


@main.command("batch")
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--out", type=click.Path(path_type=Path), default=Path("keys/batch_out.txt"))
@click.pass_obj
def batch_cmd(ctx: KeygenContext, input_file: Path, out: Path) -> None:
    """Batch-validate keys from a file."""
    summary = BatchHandler(ctx).run(input_file, out)
    console.print(f"valid={summary.valid} invalid={summary.invalid} written={out}")


@main.command("selfcheck")
@click.pass_obj
def selfcheck_cmd(ctx: KeygenContext) -> None:
    """Verify the engine is wired and the seed is loaded."""
    ok = ctx.engine.selfcheck()
    console.print("[green]selfcheck ok[/green]" if ok else "[red]selfcheck failed[/red]")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()