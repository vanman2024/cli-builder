#!/usr/bin/env python3
# Modern Python CLI using typer (FastAPI style)

import typer
from typing import Optional
from enum import Enum

app = typer.Typer()

class Environment(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"

@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    config: Optional[str] = typer.Option(None, "--config", "-c", envvar="CONFIG_PATH", help="Path to config file")
):
    """
    A simple CLI application built with Typer
    """
    if verbose:
        typer.echo("Verbose mode enabled")

    if config:
        typer.echo(f"Using config: {config}")

@app.command()
def start(
    port: int = typer.Option(8080, "--port", "-p", help="Port to listen on"),
    host: str = typer.Option("localhost", help="Host to bind to"),
):
    """Start the service"""
    typer.echo(f"Starting service on {host}:{port}")

@app.command()
def stop():
    """Stop the service"""
    typer.echo("Stopping service...")

@app.command()
def status():
    """Check service status"""
    typer.echo("Service is running")

@app.command()
def deploy(
    env: Environment = typer.Option(..., "--env", "-e", help="Target environment"),
    force: bool = typer.Option(False, "--force", help="Force deployment")
):
    """Deploy to environment"""
    typer.echo(f"Deploying to {env.value}...")
    if force:
        typer.echo("Force flag enabled")

if __name__ == "__main__":
    app()
