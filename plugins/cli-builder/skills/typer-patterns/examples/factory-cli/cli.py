"""Factory pattern CLI example.

This example demonstrates:
- Factory function for app creation
- Dependency injection
- Testable CLI structure
- Configuration injection
"""

import typer
from typing import Protocol, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    """Application configuration."""

    verbose: bool = False
    data_dir: Path = Path("./data")
    max_items: int = 100


class Storage(Protocol):
    """Storage interface for dependency injection."""

    def save(self, key: str, value: str) -> None:
        """Save data."""
        ...

    def load(self, key: str) -> str:
        """Load data."""
        ...


class MemoryStorage:
    """In-memory storage implementation."""

    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    def save(self, key: str, value: str) -> None:
        """Save to memory."""
        self.data[key] = value

    def load(self, key: str) -> str:
        """Load from memory."""
        return self.data.get(key, "")


class FileStorage:
    """File-based storage implementation."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)

    def save(self, key: str, value: str) -> None:
        """Save to file."""
        file_path = self.base_dir / f"{key}.txt"
        file_path.write_text(value)

    def load(self, key: str) -> str:
        """Load from file."""
        file_path = self.base_dir / f"{key}.txt"
        return file_path.read_text() if file_path.exists() else ""


def create_app(config: Optional[Config] = None, storage: Optional[Storage] = None) -> typer.Typer:
    """Factory function to create Typer app with dependencies.

    This pattern enables:
    - Dependency injection for testing
    - Configuration flexibility
    - Multiple app instances
    - Easier unit testing

    Args:
        config: Application configuration
        storage: Storage implementation

    Returns:
        Configured Typer application
    """
    config = config or Config()
    storage = storage or FileStorage(config.data_dir)

    app = typer.Typer(
        help="Data management CLI with factory pattern",
        no_args_is_help=True,
    )

    @app.command()
    def save(
        key: str = typer.Argument(..., help="Data key"),
        value: str = typer.Argument(..., help="Data value"),
    ) -> None:
        """Save data using injected storage."""
        if config.verbose:
            typer.echo(f"Saving {key}={value}")

        try:
            storage.save(key, value)
            typer.secho(f"✓ Saved {key}", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"✗ Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    @app.command()
    def load(key: str = typer.Argument(..., help="Data key")) -> None:
        """Load data using injected storage."""
        if config.verbose:
            typer.echo(f"Loading {key}")

        try:
            value = storage.load(key)
            if value:
                typer.echo(value)
            else:
                typer.secho(f"✗ Key not found: {key}", fg=typer.colors.YELLOW)
        except Exception as e:
            typer.secho(f"✗ Error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    @app.command()
    def config_show() -> None:
        """Show current configuration."""
        typer.echo("Configuration:")
        typer.echo(f"  Verbose: {config.verbose}")
        typer.echo(f"  Data dir: {config.data_dir}")
        typer.echo(f"  Max items: {config.max_items}")

    return app


def main() -> None:
    """Main entry point with configuration."""
    import sys

    # Parse global flags
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    data_dir = Path("./data")

    # Check for custom data directory
    if "--data-dir" in sys.argv:
        idx = sys.argv.index("--data-dir")
        if idx + 1 < len(sys.argv):
            data_dir = Path(sys.argv[idx + 1])
            sys.argv.pop(idx)  # Remove flag
            sys.argv.pop(idx)  # Remove value

    # Create configuration
    config = Config(verbose=verbose, data_dir=data_dir)

    # Create and run app
    app = create_app(config=config)
    app()


if __name__ == "__main__":
    main()
