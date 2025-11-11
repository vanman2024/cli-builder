#!/usr/bin/env python3
"""
Boolean flag patterns with store_true, store_false, and count actions.

Usage:
    python boolean-flags.py --verbose
    python boolean-flags.py -vvv --debug --force
    python boolean-flags.py --no-cache --quiet
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Boolean flag patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== store_true (False by default) =====
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )

    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force operation without confirmation'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without making changes'
    )

    # ===== store_false (True by default) =====
    parser.add_argument(
        '--no-cache',
        action='store_false',
        dest='cache',
        help='Disable caching (enabled by default)'
    )

    parser.add_argument(
        '--no-color',
        action='store_false',
        dest='color',
        help='Disable colored output (enabled by default)'
    )

    # ===== count action (count occurrences) =====
    parser.add_argument(
        '-v',
        action='count',
        default=0,
        dest='verbosity',
        help='Increase verbosity (-v, -vv, -vvv)'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='count',
        default=0,
        help='Decrease verbosity (-q, -qq, -qqq)'
    )

    # ===== store_const action =====
    parser.add_argument(
        '--fast',
        action='store_const',
        const='fast',
        dest='mode',
        help='Use fast mode'
    )

    parser.add_argument(
        '--safe',
        action='store_const',
        const='safe',
        dest='mode',
        help='Use safe mode (default)'
    )

    parser.set_defaults(mode='safe')

    # ===== Combined short flags =====
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Process all items'
    )

    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process recursively'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    # Parse arguments
    args = parser.parse_args()

    # Calculate effective verbosity
    effective_verbosity = args.verbosity - args.quiet

    # Display configuration
    print("Boolean Flags Configuration:")
    print(f"  Verbose: {args.verbose}")
    print(f"  Debug: {args.debug}")
    print(f"  Force: {args.force}")
    print(f"  Dry Run: {args.dry_run}")
    print(f"  Cache: {args.cache}")
    print(f"  Color: {args.color}")
    print(f"  Verbosity Level: {effective_verbosity}")
    print(f"  Mode: {args.mode}")
    print(f"  All: {args.all}")
    print(f"  Recursive: {args.recursive}")
    print(f"  Interactive: {args.interactive}")

    # Example usage based on flags
    if args.debug:
        print("\nDebug mode enabled - showing detailed information")

    if args.dry_run:
        print("\nDry run mode - no changes will be made")

    if effective_verbosity > 0:
        print(f"\nVerbosity level: {effective_verbosity}")
        if effective_verbosity >= 3:
            print("Maximum verbosity - showing everything")
    elif effective_verbosity < 0:
        print(f"\nQuiet level: {abs(effective_verbosity)}")

    if args.force:
        print("\nForce mode - skipping confirmations")

    if not args.cache:
        print("\nCache disabled")

    if not args.color:
        print("\nColor output disabled")

    return 0


if __name__ == '__main__':
    sys.exit(main())
