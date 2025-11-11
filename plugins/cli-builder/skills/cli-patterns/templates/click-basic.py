#!/usr/bin/env python3
# Python equivalent using click (similar API to urfave/cli)

import click

@click.group()
@click.version_option('0.1.0')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', '-c', envvar='CONFIG_PATH', help='Path to config file')
@click.pass_context
def cli(ctx, verbose, config):
    """A simple CLI application"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = config

    if verbose:
        click.echo('Verbose mode enabled')

    if config:
        click.echo(f'Using config: {config}')

@cli.command()
@click.option('--port', '-p', default=8080, help='Port to listen on')
@click.pass_context
def start(ctx, port):
    """Start the service"""
    if ctx.obj['verbose']:
        click.echo(f'Starting service on port {port}')
    else:
        click.echo(f'Starting on port {port}')

@cli.command()
@click.pass_context
def stop(ctx):
    """Stop the service"""
    click.echo('Stopping service...')

@cli.command()
def status():
    """Check service status"""
    click.echo('Service is running')

@cli.command()
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Set configuration value"""
    click.echo(f'Setting {key} = {value}')

if __name__ == '__main__':
    cli(obj={})
