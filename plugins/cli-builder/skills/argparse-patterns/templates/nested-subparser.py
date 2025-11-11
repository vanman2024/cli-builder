#!/usr/bin/env python3
"""
Nested subcommands pattern (like git config get/set, kubectl config view).

Usage:
    python nested-subparser.py config get database_url
    python nested-subparser.py config set api_key abc123
    python nested-subparser.py config list
    python nested-subparser.py deploy start production --replicas 3
    python nested-subparser.py deploy stop production
"""

import argparse
import sys


# Config command handlers
def config_get(args):
    """Get configuration value."""
    print(f"Getting config: {args.key}")
    # Simulate getting config
    print(f"{args.key} = example_value")


def config_set(args):
    """Set configuration value."""
    print(f"Setting config: {args.key} = {args.value}")
    if args.force:
        print("(Overwriting existing value)")


def config_list(args):
    """List all configuration values."""
    print(f"Listing all configuration (format: {args.format})")


def config_delete(args):
    """Delete configuration value."""
    if not args.force:
        response = input(f"Delete {args.key}? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled")
            return 1
    print(f"Deleted: {args.key}")


# Deploy command handlers
def deploy_start(args):
    """Start deployment."""
    print(f"Starting deployment to {args.environment}")
    print(f"Replicas: {args.replicas}")
    print(f"Wait: {args.wait}")


def deploy_stop(args):
    """Stop deployment."""
    print(f"Stopping deployment in {args.environment}")


def deploy_restart(args):
    """Restart deployment."""
    print(f"Restarting deployment in {args.environment}")
    if args.hard:
        print("(Hard restart)")


def main():
    # Main parser
    parser = argparse.ArgumentParser(
        description='Multi-level CLI tool with nested subcommands',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--version', action='version', version='1.0.0')

    # Top-level subparsers
    subparsers = parser.add_subparsers(
        dest='command',
        help='Top-level commands',
        required=True
    )

    # ===== Config command group =====
    config_parser = subparsers.add_parser(
        'config',
        help='Manage configuration',
        description='Configuration management commands'
    )

    # Config subcommands
    config_subparsers = config_parser.add_subparsers(
        dest='config_command',
        help='Config operations',
        required=True
    )

    # config get
    config_get_parser = config_subparsers.add_parser(
        'get',
        help='Get configuration value'
    )
    config_get_parser.add_argument('key', help='Configuration key')
    config_get_parser.set_defaults(func=config_get)

    # config set
    config_set_parser = config_subparsers.add_parser(
        'set',
        help='Set configuration value'
    )
    config_set_parser.add_argument('key', help='Configuration key')
    config_set_parser.add_argument('value', help='Configuration value')
    config_set_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Overwrite existing value'
    )
    config_set_parser.set_defaults(func=config_set)

    # config list
    config_list_parser = config_subparsers.add_parser(
        'list',
        help='List all configuration values'
    )
    config_list_parser.add_argument(
        '--format',
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format (default: %(default)s)'
    )
    config_list_parser.set_defaults(func=config_list)

    # config delete
    config_delete_parser = config_subparsers.add_parser(
        'delete',
        help='Delete configuration value'
    )
    config_delete_parser.add_argument('key', help='Configuration key')
    config_delete_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Delete without confirmation'
    )
    config_delete_parser.set_defaults(func=config_delete)

    # ===== Deploy command group =====
    deploy_parser = subparsers.add_parser(
        'deploy',
        help='Manage deployments',
        description='Deployment management commands'
    )

    # Deploy subcommands
    deploy_subparsers = deploy_parser.add_subparsers(
        dest='deploy_command',
        help='Deploy operations',
        required=True
    )

    # deploy start
    deploy_start_parser = deploy_subparsers.add_parser(
        'start',
        help='Start deployment'
    )
    deploy_start_parser.add_argument(
        'environment',
        choices=['development', 'staging', 'production'],
        help='Target environment'
    )
    deploy_start_parser.add_argument(
        '--replicas', '-r',
        type=int,
        default=1,
        help='Number of replicas (default: %(default)s)'
    )
    deploy_start_parser.add_argument(
        '--wait',
        action='store_true',
        help='Wait for deployment to complete'
    )
    deploy_start_parser.set_defaults(func=deploy_start)

    # deploy stop
    deploy_stop_parser = deploy_subparsers.add_parser(
        'stop',
        help='Stop deployment'
    )
    deploy_stop_parser.add_argument(
        'environment',
        choices=['development', 'staging', 'production'],
        help='Target environment'
    )
    deploy_stop_parser.set_defaults(func=deploy_stop)

    # deploy restart
    deploy_restart_parser = deploy_subparsers.add_parser(
        'restart',
        help='Restart deployment'
    )
    deploy_restart_parser.add_argument(
        'environment',
        choices=['development', 'staging', 'production'],
        help='Target environment'
    )
    deploy_restart_parser.add_argument(
        '--hard',
        action='store_true',
        help='Perform hard restart'
    )
    deploy_restart_parser.set_defaults(func=deploy_restart)

    # Parse arguments
    args = parser.parse_args()

    # Call the appropriate command function
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main() or 0)
