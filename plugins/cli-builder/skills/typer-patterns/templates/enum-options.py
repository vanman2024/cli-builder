"""Enum-based options template for Typer.

This template demonstrates:
- Enum usage for constrained choices
- Multiple enum types
- Enum with autocomplete
- Type-safe enum handling
"""

import typer
from enum import Enum
from typing import Optional


class LogLevel(str, Enum):
    """Log level choices."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"


class OutputFormat(str, Enum):
    """Output format choices."""

    json = "json"
    yaml = "yaml"
    text = "text"
    csv = "csv"


class Environment(str, Enum):
    """Deployment environment choices."""

    development = "development"
    staging = "staging"
    production = "production"


app = typer.Typer()


@app.command()
def deploy(
    environment: Environment = typer.Argument(
        ..., help="Target deployment environment"
    ),
    format: OutputFormat = typer.Option(
        OutputFormat.json, "--format", "-f", help="Output format for logs"
    ),
    log_level: LogLevel = typer.Option(
        LogLevel.info, "--log-level", "-l", help="Logging level"
    ),
    force: bool = typer.Option(False, "--force", help="Force deployment"),
) -> None:
    """Deploy application with enum-based options.

    Example:
        $ python cli.py production --format yaml --log-level debug
    """
    typer.echo(f"Deploying to: {environment.value}")
    typer.echo(f"Output format: {format.value}")
    typer.echo(f"Log level: {log_level.value}")

    if force:
        typer.secho("⚠ Force deployment enabled", fg=typer.colors.YELLOW)

    # Deployment logic here
    # The enum values are guaranteed to be valid


@app.command()
def export(
    format: OutputFormat = typer.Argument(
        OutputFormat.json, help="Export format"
    ),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
) -> None:
    """Export data in specified format.

    Example:
        $ python cli.py export yaml --output data.yaml
    """
    typer.echo(f"Exporting as {format.value}")

    # Export logic based on format
    match format:
        case OutputFormat.json:
            typer.echo("Generating JSON...")
        case OutputFormat.yaml:
            typer.echo("Generating YAML...")
        case OutputFormat.text:
            typer.echo("Generating plain text...")
        case OutputFormat.csv:
            typer.echo("Generating CSV...")


if __name__ == "__main__":
    app()
