#!/usr/bin/env python3
"""
Basic argparse parser with common argument types.

Usage:
    python basic-parser.py --help
    python basic-parser.py deploy app1 --env production --force
    python basic-parser.py deploy app2 --env staging --timeout 60
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Deploy application to specified environment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s deploy my-app --env production
  %(prog)s deploy my-app --env staging --force
  %(prog)s deploy my-app --env dev --timeout 120
        '''
    )

    # Version info
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # Required positional argument
    parser.add_argument(
        'action',
        help='Action to perform'
    )

    parser.add_argument(
        'app_name',
        help='Name of the application to deploy'
    )

    # Optional arguments with different types
    parser.add_argument(
        '--env', '-e',
        default='development',
        help='Deployment environment (default: %(default)s)'
    )

    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=30,
        help='Timeout in seconds (default: %(default)s)'
    )

    # Boolean flag
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force deployment without confirmation'
    )

    # Verbose flag (count occurrences)
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity (-v, -vv, -vvv)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Use parsed arguments
    print(f"Action: {args.action}")
    print(f"App Name: {args.app_name}")
    print(f"Environment: {args.env}")
    print(f"Timeout: {args.timeout}s")
    print(f"Force: {args.force}")
    print(f"Verbosity Level: {args.verbose}")

    # Example validation
    if args.timeout < 1:
        parser.error("Timeout must be at least 1 second")

    return 0


if __name__ == '__main__':
    sys.exit(main())
