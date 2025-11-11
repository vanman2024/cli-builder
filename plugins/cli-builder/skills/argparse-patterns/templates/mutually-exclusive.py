#!/usr/bin/env python3
"""
Mutually exclusive argument groups.

Usage:
    python mutually-exclusive.py --json output.json
    python mutually-exclusive.py --yaml output.yaml
    python mutually-exclusive.py --verbose
    python mutually-exclusive.py --quiet
    python mutually-exclusive.py --create resource
    python mutually-exclusive.py --delete resource
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Mutually exclusive argument groups',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== Output Format (mutually exclusive) =====
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        '--json',
        metavar='FILE',
        help='Output in JSON format'
    )
    output_group.add_argument(
        '--yaml',
        metavar='FILE',
        help='Output in YAML format'
    )
    output_group.add_argument(
        '--xml',
        metavar='FILE',
        help='Output in XML format'
    )

    # ===== Verbosity (mutually exclusive) =====
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Increase verbosity'
    )
    verbosity_group.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output'
    )

    # ===== Operation Mode (mutually exclusive, required) =====
    operation_group = parser.add_mutually_exclusive_group(required=True)
    operation_group.add_argument(
        '--create',
        metavar='RESOURCE',
        help='Create a resource'
    )
    operation_group.add_argument(
        '--update',
        metavar='RESOURCE',
        help='Update a resource'
    )
    operation_group.add_argument(
        '--delete',
        metavar='RESOURCE',
        help='Delete a resource'
    )
    operation_group.add_argument(
        '--list',
        action='store_true',
        help='List all resources'
    )

    # ===== Authentication Method (mutually exclusive) =====
    auth_group = parser.add_mutually_exclusive_group()
    auth_group.add_argument(
        '--token',
        metavar='TOKEN',
        help='Authenticate with token'
    )
    auth_group.add_argument(
        '--api-key',
        metavar='KEY',
        help='Authenticate with API key'
    )
    auth_group.add_argument(
        '--credentials',
        metavar='FILE',
        help='Authenticate with credentials file'
    )

    # ===== Deployment Strategy (mutually exclusive with default) =====
    strategy_group = parser.add_mutually_exclusive_group()
    strategy_group.add_argument(
        '--rolling',
        action='store_true',
        help='Use rolling deployment'
    )
    strategy_group.add_argument(
        '--blue-green',
        action='store_true',
        help='Use blue-green deployment'
    )
    strategy_group.add_argument(
        '--canary',
        action='store_true',
        help='Use canary deployment'
    )

    # Set default strategy if none specified
    parser.set_defaults(rolling=False, blue_green=False, canary=False)

    # Parse arguments
    args = parser.parse_args()

    # Display configuration
    print("Mutually Exclusive Groups Configuration:")

    # Output format
    if args.json:
        print(f"  Output Format: JSON to {args.json}")
    elif args.yaml:
        print(f"  Output Format: YAML to {args.yaml}")
    elif args.xml:
        print(f"  Output Format: XML to {args.xml}")
    else:
        print("  Output Format: None (default stdout)")

    # Verbosity
    if args.verbose:
        print("  Verbosity: Verbose")
    elif args.quiet:
        print("  Verbosity: Quiet")
    else:
        print("  Verbosity: Normal")

    # Operation
    if args.create:
        print(f"  Operation: Create {args.create}")
    elif args.update:
        print(f"  Operation: Update {args.update}")
    elif args.delete:
        print(f"  Operation: Delete {args.delete}")
    elif args.list:
        print("  Operation: List resources")

    # Authentication
    if args.token:
        print(f"  Auth Method: Token")
    elif args.api_key:
        print(f"  Auth Method: API Key")
    elif args.credentials:
        print(f"  Auth Method: Credentials file ({args.credentials})")
    else:
        print("  Auth Method: None")

    # Deployment strategy
    if args.rolling:
        print("  Deployment: Rolling")
    elif args.blue_green:
        print("  Deployment: Blue-Green")
    elif args.canary:
        print("  Deployment: Canary")
    else:
        print("  Deployment: Default")

    return 0


if __name__ == '__main__':
    sys.exit(main())
