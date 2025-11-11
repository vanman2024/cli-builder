"""Basic type-safe Typer command template.

This template demonstrates modern Typer usage with:
- Full type hints on all parameters
- Path type for file operations
- Optional parameters with defaults
- Typed return hints
"""

import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()


@app.command()
def process(
    input_file: Path = typer.Argument(
        ...,
        help="Input file to process",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (optional)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
    count: int = typer.Option(
        10,
        "--count",
        "-c",
        help="Number of items to process",
        min=1,
        max=1000,
    ),
) -> None:
    """Process input file with type-safe parameters.

    Example:
        $ python cli.py input.txt --output result.txt --verbose --count 50
    """
    if verbose:
        typer.echo(f"Processing {input_file}")
        typer.echo(f"Count: {count}")

    # Your processing logic here
    content = input_file.read_text()

    if output_file:
        output_file.write_text(content)
        typer.secho(f"✓ Saved to {output_file}", fg=typer.colors.GREEN)
    else:
        typer.echo(content)


if __name__ == "__main__":
    app()
