"""Advanced validation and callbacks template.

This template demonstrates:
- Custom validators with callbacks
- Complex validation logic
- Interdependent parameter validation
- Rich error messages
"""

import typer
from typing import Optional
from pathlib import Path
import re


app = typer.Typer()


# Custom validators
def validate_email(value: str) -> str:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        raise typer.BadParameter("Invalid email format")
    return value


def validate_port(value: int) -> int:
    """Validate port number range."""
    if not 1024 <= value <= 65535:
        raise typer.BadParameter("Port must be between 1024-65535")
    return value


def validate_path_exists(value: Path) -> Path:
    """Validate that path exists."""
    if not value.exists():
        raise typer.BadParameter(f"Path does not exist: {value}")
    return value


def validate_percentage(value: float) -> float:
    """Validate percentage range."""
    if not 0.0 <= value <= 100.0:
        raise typer.BadParameter("Percentage must be between 0-100")
    return value


def validate_url(value: str) -> str:
    """Validate URL format."""
    pattern = r"^https?://[^\s/$.?#].[^\s]*$"
    if not re.match(pattern, value):
        raise typer.BadParameter("Invalid URL format (must start with http:// or https://)")
    return value


# Context manager for complex validation
class ValidationContext:
    """Context for cross-parameter validation."""

    def __init__(self) -> None:
        self.params: dict = {}

    def add(self, key: str, value: any) -> None:
        """Add parameter to context."""
        self.params[key] = value

    def validate_dependencies(self) -> None:
        """Validate parameter dependencies."""
        # Example: if ssl is enabled, cert and key must be provided
        if self.params.get("ssl") and not (
            self.params.get("cert") and self.params.get("key")
        ):
            raise typer.BadParameter("SSL requires both --cert and --key")


# Global validation context
validation_context = ValidationContext()


@app.command()
def server(
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        "-h",
        help="Server host",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Server port",
        callback=lambda _, value: validate_port(value),
    ),
    ssl: bool = typer.Option(
        False,
        "--ssl",
        help="Enable SSL/TLS",
    ),
    cert: Optional[Path] = typer.Option(
        None,
        "--cert",
        help="SSL certificate file",
        callback=lambda _, value: validate_path_exists(value) if value else None,
    ),
    key: Optional[Path] = typer.Option(
        None,
        "--key",
        help="SSL private key file",
        callback=lambda _, value: validate_path_exists(value) if value else None,
    ),
) -> None:
    """Start server with validated parameters.

    Example:
        $ python cli.py server --port 8443 --ssl --cert cert.pem --key key.pem
    """
    # Store params for cross-validation
    validation_context.add("ssl", ssl)
    validation_context.add("cert", cert)
    validation_context.add("key", key)

    # Validate dependencies
    try:
        validation_context.validate_dependencies()
    except typer.BadParameter as e:
        typer.secho(f"✗ Validation error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1)

    # Start server
    protocol = "https" if ssl else "http"
    typer.echo(f"Starting server at {protocol}://{host}:{port}")


@app.command()
def user_create(
    username: str = typer.Argument(..., help="Username (alphanumeric only)"),
    email: str = typer.Option(
        ...,
        "--email",
        "-e",
        help="User email",
        callback=lambda _, value: validate_email(value),
    ),
    age: Optional[int] = typer.Option(
        None,
        "--age",
        help="User age",
        min=13,
        max=120,
    ),
) -> None:
    """Create user with validated inputs.

    Example:
        $ python cli.py user-create john --email john@example.com --age 25
    """
    # Additional username validation
    if not username.isalnum():
        typer.secho(
            "✗ Username must be alphanumeric", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(1)

    typer.secho(f"✓ User created: {username}", fg=typer.colors.GREEN)


@app.command()
def deploy(
    url: str = typer.Option(
        ...,
        "--url",
        help="Deployment URL",
        callback=lambda _, value: validate_url(value),
    ),
    threshold: float = typer.Option(
        95.0,
        "--threshold",
        help="Success threshold percentage",
        callback=lambda _, value: validate_percentage(value),
    ),
    rollback_on_error: bool = typer.Option(
        True, "--rollback/--no-rollback", help="Rollback on error"
    ),
) -> None:
    """Deploy with validated URL and threshold.

    Example:
        $ python cli.py deploy --url https://example.com --threshold 99.5
    """
    typer.echo(f"Deploying to: {url}")
    typer.echo(f"Success threshold: {threshold}%")
    typer.echo(f"Rollback on error: {rollback_on_error}")


@app.command()
def batch_process(
    input_dir: Path = typer.Argument(
        ...,
        help="Input directory",
        callback=lambda _, value: validate_path_exists(value),
    ),
    pattern: str = typer.Option(
        "*.txt", "--pattern", "-p", help="File pattern"
    ),
    workers: int = typer.Option(
        4,
        "--workers",
        "-w",
        help="Number of worker threads",
        min=1,
        max=32,
    ),
) -> None:
    """Batch process files with validation.

    Example:
        $ python cli.py batch-process ./data --pattern "*.json" --workers 8
    """
    if not input_dir.is_dir():
        typer.secho(
            f"✗ Not a directory: {input_dir}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(1)

    typer.echo(f"Processing files in: {input_dir}")
    typer.echo(f"Pattern: {pattern}")
    typer.echo(f"Workers: {workers}")


if __name__ == "__main__":
    app()
