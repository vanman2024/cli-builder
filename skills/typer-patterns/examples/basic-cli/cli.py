"""Basic CLI example using type hints.

This example demonstrates:
- Simple type-safe command
- Path validation
- Optional parameters
- Verbose output
"""

import typer
from pathlib import Path
from typing import Optional

app = typer.Typer(help="Basic file processing CLI")


@app.command()
def process(
    input_file: Path = typer.Argument(
        ..., help="Input file to process", exists=True
    ),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
    uppercase: bool = typer.Option(False, "--uppercase", "-u"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Process text file with optional transformations."""
    if verbose:
        typer.echo(f"Processing: {input_file}")

    content = input_file.read_text()

    if uppercase:
        content = content.upper()

    if output:
        output.write_text(content)
        typer.secho(f"✓ Written to: {output}", fg=typer.colors.GREEN)
    else:
        typer.echo(content)


if __name__ == "__main__":
    app()
