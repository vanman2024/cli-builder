#!/usr/bin/env python3
"""
Custom action classes for advanced argument processing.

Usage:
    python custom-actions.py --env-file .env
    python custom-actions.py --key API_KEY --key DB_URL
    python custom-actions.py --range 1-10 --range 20-30
"""

import argparse
import sys
from pathlib import Path


class LoadEnvFileAction(argparse.Action):
    """Custom action to load environment variables from file."""

    def __call__(self, parser, namespace, values, option_string=None):
        env_file = Path(values)
        if not env_file.exists():
            parser.error(f"Environment file does not exist: {values}")

        env_vars = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()

        setattr(namespace, self.dest, env_vars)


class KeyValueAction(argparse.Action):
    """Custom action to parse key=value pairs."""

    def __call__(self, parser, namespace, values, option_string=None):
        if '=' not in values:
            parser.error(f"Argument must be in key=value format: {values}")

        key, value = values.split('=', 1)
        items = getattr(namespace, self.dest, None) or {}
        items[key] = value
        setattr(namespace, self.dest, items)


class RangeAction(argparse.Action):
    """Custom action to parse ranges like 1-10."""

    def __call__(self, parser, namespace, values, option_string=None):
        if '-' not in values:
            parser.error(f"Range must be in format start-end: {values}")

        try:
            start, end = values.split('-')
            start = int(start)
            end = int(end)
        except ValueError:
            parser.error(f"Invalid range format: {values}")

        if start > end:
            parser.error(f"Start must be less than or equal to end: {values}")

        ranges = getattr(namespace, self.dest, None) or []
        ranges.append((start, end))
        setattr(namespace, self.dest, ranges)


class AppendUniqueAction(argparse.Action):
    """Custom action to append unique values only."""

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None) or []
        if values not in items:
            items.append(values)
        setattr(namespace, self.dest, items)


class ValidateAndStoreAction(argparse.Action):
    """Custom action that validates before storing."""

    def __call__(self, parser, namespace, values, option_string=None):
        # Custom validation logic
        if values.startswith('test-'):
            print(f"Warning: Using test value: {values}")

        # Transform value
        transformed = values.upper()

        setattr(namespace, self.dest, transformed)


class IncrementAction(argparse.Action):
    """Custom action to increment a value."""

    def __init__(self, option_strings, dest, default=0, **kwargs):
        super().__init__(option_strings, dest, nargs=0, default=default, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        current = getattr(namespace, self.dest, self.default)
        setattr(namespace, self.dest, current + 1)


def main():
    parser = argparse.ArgumentParser(
        description='Custom action demonstrations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Load environment file
    parser.add_argument(
        '--env-file',
        action=LoadEnvFileAction,
        help='Load environment variables from file'
    )

    # Key-value pairs
    parser.add_argument(
        '--config', '-c',
        action=KeyValueAction,
        help='Configuration in key=value format (can be used multiple times)'
    )

    # Range parsing
    parser.add_argument(
        '--range', '-r',
        action=RangeAction,
        help='Range in start-end format (e.g., 1-10)'
    )

    # Unique append
    parser.add_argument(
        '--tag',
        action=AppendUniqueAction,
        help='Add unique tag (duplicates ignored)'
    )

    # Validate and transform
    parser.add_argument(
        '--key',
        action=ValidateAndStoreAction,
        help='Key to transform to uppercase'
    )

    # Custom increment
    parser.add_argument(
        '--increment',
        action=IncrementAction,
        help='Increment counter'
    )

    # Parse arguments
    args = parser.parse_args()

    # Display results
    print("Custom Actions Results:")

    if args.env_file:
        print(f"\nEnvironment Variables:")
        for key, value in args.env_file.items():
            print(f"  {key}={value}")

    if args.config:
        print(f"\nConfiguration:")
        for key, value in args.config.items():
            print(f"  {key}={value}")

    if args.range:
        print(f"\nRanges:")
        for start, end in args.range:
            print(f"  {start}-{end} (includes {end - start + 1} values)")

    if args.tag:
        print(f"\nUnique Tags: {', '.join(args.tag)}")

    if args.key:
        print(f"\nTransformed Key: {args.key}")

    if args.increment:
        print(f"\nIncrement Count: {args.increment}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
