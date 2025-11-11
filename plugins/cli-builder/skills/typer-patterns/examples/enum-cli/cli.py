"""Enum-based CLI example.

This example demonstrates:
- Enum usage for constrained choices
- Multiple enum types
- Autocomplete with enums
- Match/case with enum values
"""

import typer
from enum import Enum
from typing import Optional
import json


class LogLevel(str, Enum):
    """Logging levels."""

    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"


class OutputFormat(str, Enum):
    """Output formats."""

    json = "json"
    yaml = "yaml"
    text = "text"


app = typer.Typer(help="Configuration export CLI with Enums")


@app.command()
def export(
    format: OutputFormat = typer.Argument(
        OutputFormat.json, help="Export format"
    ),
    log_level: LogLevel = typer.Option(
        LogLevel.info, "--log-level", "-l", help="Logging level"
    ),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
) -> None:
    """Export configuration in specified format.

    The format parameter uses an Enum, providing:
    - Autocomplete in the shell
    - Validation of input values
    - Type safety in code
    """
    # Sample data
    data = {
        "app": "example",
        "version": "1.0.0",
        "log_level": log_level.value,
        "features": ["auth", "api", "cache"],
    }

    # Format output based on enum
    match format:
        case OutputFormat.json:
            output_text = json.dumps(data, indent=2)
        case OutputFormat.yaml:
            # Simplified YAML output
            output_text = "\n".join(f"{k}: {v}" for k, v in data.items())
        case OutputFormat.text:
            output_text = "\n".join(
                f"{k.upper()}: {v}" for k, v in data.items()
            )

    # Output
    if output:
        with open(output, "w") as f:
            f.write(output_text)
        typer.secho(f"✓ Exported to {output}", fg=typer.colors.GREEN)
    else:
        typer.echo(output_text)


@app.command()
def validate(
    level: LogLevel = typer.Argument(..., help="Log level to validate")
) -> None:
    """Validate and display log level information."""
    typer.echo(f"Log Level: {level.value}")

    # Access enum properties
    match level:
        case LogLevel.debug:
            typer.echo("Severity: Lowest - detailed debugging information")
        case LogLevel.info:
            typer.echo("Severity: Low - informational messages")
        case LogLevel.warning:
            typer.echo("Severity: Medium - warning messages")
        case LogLevel.error:
            typer.echo("Severity: High - error messages")


if __name__ == "__main__":
    app()
