"""Typer instance factory pattern template.

This template demonstrates:
- Factory function for creating Typer apps
- Better testability
- Configuration injection
- Dependency management
"""

import typer
from typing import Optional, Protocol
from pathlib import Path
from dataclasses import dataclass


# Configuration
@dataclass
class Config:
    """Application configuration."""

    verbose: bool = False
    debug: bool = False
    config_file: Optional[Path] = None


# Service protocol (dependency injection)
class StorageService(Protocol):
    """Storage service interface."""

    def save(self, data: str) -> None:
        """Save data."""
        ...

    def load(self) -> str:
        """Load data."""
        ...


class FileStorage:
    """File-based storage implementation."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def save(self, data: str) -> None:
        """Save data to file."""
        self.base_path.write_text(data)

    def load(self) -> str:
        """Load data from file."""
        return self.base_path.read_text()


def create_app(
    config: Optional[Config] = None, storage: Optional[StorageService] = None
) -> typer.Typer:
    """Factory function for creating Typer application.

    This pattern allows for:
    - Easy testing with mocked dependencies
    - Configuration injection
    - Multiple app instances with different configs

    Args:
        config: Application configuration
        storage: Storage service implementation

    Returns:
        Configured Typer application
    """
    config = config or Config()
    storage = storage or FileStorage(Path("data.txt"))

    app = typer.Typer(
        name="myapp",
        help="Example CLI with factory pattern",
        add_completion=True,
        no_args_is_help=True,
        rich_markup_mode="rich",
    )

    @app.command()
    def save(
        data: str = typer.Argument(..., help="Data to save"),
        force: bool = typer.Option(False, "--force", help="Overwrite existing"),
    ) -> None:
        """Save data using injected storage."""
        if config.verbose:
            typer.echo(f"Saving: {data}")

        try:
            storage.save(data)
            typer.secho("✓ Data saved successfully", fg=typer.colors.GREEN)
        except Exception as e:
            if config.debug:
                raise
            typer.secho(f"✗ Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    @app.command()
    def load() -> None:
        """Load data using injected storage."""
        try:
            data = storage.load()
            typer.echo(data)
        except FileNotFoundError:
            typer.secho("✗ No data found", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)
        except Exception as e:
            if config.debug:
                raise
            typer.secho(f"✗ Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    @app.command()
    def status() -> None:
        """Show application status."""
        typer.echo("Application Status:")
        typer.echo(f"  Verbose: {config.verbose}")
        typer.echo(f"  Debug: {config.debug}")
        typer.echo(f"  Config: {config.config_file or 'default'}")

    return app


def main() -> None:
    """Main entry point with configuration setup."""
    # Parse global options
    import sys

    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    debug = "--debug" in sys.argv

    # Create configuration
    config = Config(verbose=verbose, debug=debug)

    # Create and run app
    app = create_app(config=config)
    app()


if __name__ == "__main__":
    main()
