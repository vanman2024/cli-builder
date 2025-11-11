"""Sub-application CLI example.

This example demonstrates:
- Multi-level command structure
- Sub-apps for logical grouping
- Shared context across commands
- Clean command organization
"""

import typer
from typing import Optional
from pathlib import Path

# Main app
app = typer.Typer(
    help="Project management CLI with sub-commands", add_completion=True
)

# Sub-applications
db_app = typer.Typer(help="Database commands")
server_app = typer.Typer(help="Server commands")
user_app = typer.Typer(help="User management commands")

# Add sub-apps to main app
app.add_typer(db_app, name="db")
app.add_typer(server_app, name="server")
app.add_typer(user_app, name="user")


# Global callback for shared options
@app.callback()
def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(None, "--config", "-c"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Global options for all commands."""
    ctx.obj = {"config": config, "verbose": verbose}
    if verbose:
        typer.echo(f"Config: {config or 'default'}")


# Database commands
@db_app.command("init")
def db_init(ctx: typer.Context) -> None:
    """Initialize database."""
    if ctx.obj["verbose"]:
        typer.echo("Initializing database...")
    typer.secho("✓ Database initialized", fg=typer.colors.GREEN)


@db_app.command("migrate")
def db_migrate(ctx: typer.Context, steps: int = typer.Option(1)) -> None:
    """Run database migrations."""
    if ctx.obj["verbose"]:
        typer.echo(f"Running {steps} migration(s)...")
    typer.secho("✓ Migrations complete", fg=typer.colors.GREEN)


@db_app.command("seed")
def db_seed(ctx: typer.Context) -> None:
    """Seed database with test data."""
    if ctx.obj["verbose"]:
        typer.echo("Seeding database...")
    typer.secho("✓ Database seeded", fg=typer.colors.GREEN)


# Server commands
@server_app.command("start")
def server_start(
    ctx: typer.Context,
    port: int = typer.Option(8000, "--port", "-p"),
    host: str = typer.Option("127.0.0.1", "--host"),
) -> None:
    """Start application server."""
    if ctx.obj["verbose"]:
        typer.echo(f"Starting server on {host}:{port}...")
    typer.secho(f"✓ Server running at http://{host}:{port}", fg=typer.colors.GREEN)


@server_app.command("stop")
def server_stop(ctx: typer.Context) -> None:
    """Stop application server."""
    if ctx.obj["verbose"]:
        typer.echo("Stopping server...")
    typer.secho("✓ Server stopped", fg=typer.colors.RED)


@server_app.command("restart")
def server_restart(ctx: typer.Context) -> None:
    """Restart application server."""
    if ctx.obj["verbose"]:
        typer.echo("Restarting server...")
    typer.secho("✓ Server restarted", fg=typer.colors.GREEN)


# User commands
@user_app.command("create")
def user_create(
    ctx: typer.Context,
    username: str = typer.Argument(...),
    email: str = typer.Option(..., "--email", "-e"),
    admin: bool = typer.Option(False, "--admin"),
) -> None:
    """Create a new user."""
    if ctx.obj["verbose"]:
        typer.echo(f"Creating user: {username}")
    role = "admin" if admin else "user"
    typer.secho(f"✓ User {username} created as {role}", fg=typer.colors.GREEN)


@user_app.command("delete")
def user_delete(ctx: typer.Context, username: str = typer.Argument(...)) -> None:
    """Delete a user."""
    confirm = typer.confirm(f"Delete user {username}?")
    if not confirm:
        typer.echo("Cancelled")
        raise typer.Abort()
    typer.secho(f"✓ User {username} deleted", fg=typer.colors.RED)


@user_app.command("list")
def user_list(ctx: typer.Context) -> None:
    """List all users."""
    users = ["alice", "bob", "charlie"]
    typer.echo("Users:")
    for user in users:
        typer.echo(f"  - {user}")


if __name__ == "__main__":
    app()
