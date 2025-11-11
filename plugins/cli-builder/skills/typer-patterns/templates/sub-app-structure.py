"""Sub-application structure template.

This template demonstrates:
- Multiple sub-apps for command organization
- Shared context between commands
- Hierarchical command structure
- Clean separation of concerns
"""

import typer
from typing import Optional
from pathlib import Path

# Main application
app = typer.Typer(
    name="mycli",
    help="Example CLI with sub-applications",
    add_completion=True,
)

# Database sub-app
db_app = typer.Typer(help="Database management commands")
app.add_typer(db_app, name="db")

# Server sub-app
server_app = typer.Typer(help="Server management commands")
app.add_typer(server_app, name="server")

# User sub-app
user_app = typer.Typer(help="User management commands")
app.add_typer(user_app, name="user")


# Main app callback for global options
@app.callback()
def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Config file path"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Global options for all commands."""
    # Store in context for sub-commands
    ctx.obj = {"config": config, "verbose": verbose}

    if verbose:
        typer.echo(f"Config: {config or 'default'}")


# Database commands
@db_app.command("migrate")
def db_migrate(
    ctx: typer.Context,
    direction: str = typer.Argument("up", help="Migration direction: up/down"),
    steps: int = typer.Option(1, help="Number of migration steps"),
) -> None:
    """Run database migrations."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        typer.echo(f"Running {steps} migration(s) {direction}")

    typer.secho("✓ Migrations complete", fg=typer.colors.GREEN)


@db_app.command("seed")
def db_seed(
    ctx: typer.Context, file: Optional[Path] = typer.Option(None, "--file", "-f")
) -> None:
    """Seed database with test data."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        typer.echo(f"Seeding from: {file or 'default seed'}")

    typer.secho("✓ Database seeded", fg=typer.colors.GREEN)


@db_app.command("backup")
def db_backup(ctx: typer.Context, output: Path = typer.Argument(...)) -> None:
    """Backup database to file."""
    typer.echo(f"Backing up database to {output}")
    typer.secho("✓ Backup complete", fg=typer.colors.GREEN)


# Server commands
@server_app.command("start")
def server_start(
    ctx: typer.Context,
    port: int = typer.Option(8000, help="Server port"),
    host: str = typer.Option("127.0.0.1", help="Server host"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
) -> None:
    """Start the application server."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        typer.echo(f"Starting server on {host}:{port}")

    if reload:
        typer.echo("Auto-reload enabled")

    typer.secho("✓ Server started", fg=typer.colors.GREEN)


@server_app.command("stop")
def server_stop(ctx: typer.Context) -> None:
    """Stop the application server."""
    typer.echo("Stopping server...")
    typer.secho("✓ Server stopped", fg=typer.colors.GREEN)


@server_app.command("status")
def server_status(ctx: typer.Context) -> None:
    """Check server status."""
    typer.echo("Server status: Running")


# User commands
@user_app.command("create")
def user_create(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="Username"),
    email: str = typer.Argument(..., help="Email address"),
    admin: bool = typer.Option(False, "--admin", help="Create as admin"),
) -> None:
    """Create a new user."""
    verbose = ctx.obj.get("verbose", False)

    if verbose:
        typer.echo(f"Creating user: {username} ({email})")

    if admin:
        typer.echo("Creating with admin privileges")

    typer.secho(f"✓ User {username} created", fg=typer.colors.GREEN)


@user_app.command("delete")
def user_delete(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="Username"),
    force: bool = typer.Option(False, "--force", help="Force deletion"),
) -> None:
    """Delete a user."""
    if not force:
        confirm = typer.confirm(f"Delete user {username}?")
        if not confirm:
            typer.echo("Cancelled")
            raise typer.Abort()

    typer.secho(f"✓ User {username} deleted", fg=typer.colors.RED)


@user_app.command("list")
def user_list(ctx: typer.Context) -> None:
    """List all users."""
    typer.echo("Listing users...")
    # List logic here


if __name__ == "__main__":
    app()
