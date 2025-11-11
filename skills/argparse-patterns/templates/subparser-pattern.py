#!/usr/bin/env python3
"""
Single-level subcommands pattern (like docker, kubectl).

Usage:
    python subparser-pattern.py init --template react
    python subparser-pattern.py deploy production --force
    python subparser-pattern.py status --format json
"""

import argparse
import sys


def cmd_init(args):
    """Initialize a new project."""
    print(f"Initializing project with {args.template} template...")
    print(f"Path: {args.path}")


def cmd_deploy(args):
    """Deploy application."""
    print(f"Deploying to {args.environment} in {args.mode} mode")
    if args.force:
        print("Warning: Force mode enabled")


def cmd_status(args):
    """Show deployment status."""
    print(f"Status format: {args.format}")
    print("Fetching status...")


def main():
    # Main parser
    parser = argparse.ArgumentParser(
        description='Multi-command CLI tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version='1.0.0'
    )

    # Create subparsers
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True  # Python 3.7+
    )

    # Init command
    init_parser = subparsers.add_parser(
        'init',
        help='Initialize a new project',
        description='Initialize a new project with specified template'
    )
    init_parser.add_argument(
        '--template', '-t',
        default='basic',
        help='Project template (default: %(default)s)'
    )
    init_parser.add_argument(
        '--path', '-p',
        default='.',
        help='Project path (default: %(default)s)'
    )
    init_parser.set_defaults(func=cmd_init)

    # Deploy command
    deploy_parser = subparsers.add_parser(
        'deploy',
        help='Deploy application to environment',
        description='Deploy application to specified environment'
    )
    deploy_parser.add_argument(
        'environment',
        choices=['development', 'staging', 'production'],
        help='Target environment'
    )
    deploy_parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force deployment without confirmation'
    )
    deploy_parser.add_argument(
        '--mode', '-m',
        choices=['fast', 'safe', 'rollback'],
        default='safe',
        help='Deployment mode (default: %(default)s)'
    )
    deploy_parser.set_defaults(func=cmd_deploy)

    # Status command
    status_parser = subparsers.add_parser(
        'status',
        help='Show deployment status',
        description='Display current deployment status'
    )
    status_parser.add_argument(
        '--format',
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format (default: %(default)s)'
    )
    status_parser.add_argument(
        '--service',
        action='append',
        help='Filter by service (can be used multiple times)'
    )
    status_parser.set_defaults(func=cmd_status)

    # Parse arguments
    args = parser.parse_args()

    # Call the appropriate command function
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main() or 0)
