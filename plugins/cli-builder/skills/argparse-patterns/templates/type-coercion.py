#!/usr/bin/env python3
"""
Type coercion and custom type converters.

Usage:
    python type-coercion.py --port 8080 --timeout 30.5 --date 2024-01-15
    python type-coercion.py --url https://api.example.com --size 1.5GB
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
import re


def parse_date(value):
    """Parse date in YYYY-MM-DD format."""
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {value} (expected YYYY-MM-DD)"
        )


def parse_datetime(value):
    """Parse datetime in ISO format."""
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid datetime format: {value} (expected ISO format)"
        )


def parse_url(value):
    """Parse and validate URL."""
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(f"Invalid URL: {value}")
    return value


def parse_size(value):
    """Parse size with units (e.g., 1.5GB, 500MB)."""
    pattern = r'^(\d+\.?\d*)(B|KB|MB|GB|TB)$'
    match = re.match(pattern, value, re.IGNORECASE)
    if not match:
        raise argparse.ArgumentTypeError(
            f"Invalid size format: {value} (expected number with unit)"
        )

    size, unit = match.groups()
    size = float(size)

    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    return int(size * units[unit.upper()])


def parse_duration(value):
    """Parse duration (e.g., 1h, 30m, 90s)."""
    pattern = r'^(\d+)(s|m|h|d)$'
    match = re.match(pattern, value, re.IGNORECASE)
    if not match:
        raise argparse.ArgumentTypeError(
            f"Invalid duration format: {value} (expected number with s/m/h/d)"
        )

    amount, unit = match.groups()
    amount = int(amount)

    units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    return amount * units[unit.lower()]


def parse_percentage(value):
    """Parse percentage (0-100)."""
    try:
        pct = float(value.rstrip('%'))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid percentage: {value}")

    if pct < 0 or pct > 100:
        raise argparse.ArgumentTypeError(
            f"Percentage must be between 0 and 100: {value}"
        )
    return pct


def parse_comma_separated(value):
    """Parse comma-separated list."""
    return [item.strip() for item in value.split(',') if item.strip()]


def parse_key_value_pairs(value):
    """Parse semicolon-separated key=value pairs."""
    pairs = {}
    for pair in value.split(';'):
        if '=' in pair:
            key, val = pair.split('=', 1)
            pairs[key.strip()] = val.strip()
    return pairs


def main():
    parser = argparse.ArgumentParser(
        description='Type coercion demonstrations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== Built-in Types =====
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port number (integer)'
    )

    parser.add_argument(
        '--timeout',
        type=float,
        default=30.0,
        help='Timeout in seconds (float)'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Configuration file path'
    )

    parser.add_argument(
        '--output',
        type=argparse.FileType('w'),
        help='Output file (opened for writing)'
    )

    parser.add_argument(
        '--input',
        type=argparse.FileType('r'),
        help='Input file (opened for reading)'
    )

    # ===== Custom Types =====
    parser.add_argument(
        '--date',
        type=parse_date,
        help='Date in YYYY-MM-DD format'
    )

    parser.add_argument(
        '--datetime',
        type=parse_datetime,
        help='Datetime in ISO format'
    )

    parser.add_argument(
        '--url',
        type=parse_url,
        help='URL to connect to'
    )

    parser.add_argument(
        '--size',
        type=parse_size,
        help='Size with unit (e.g., 1.5GB, 500MB)'
    )

    parser.add_argument(
        '--duration',
        type=parse_duration,
        help='Duration (e.g., 1h, 30m, 90s)'
    )

    parser.add_argument(
        '--percentage',
        type=parse_percentage,
        help='Percentage (0-100)'
    )

    parser.add_argument(
        '--tags',
        type=parse_comma_separated,
        help='Comma-separated tags'
    )

    parser.add_argument(
        '--env',
        type=parse_key_value_pairs,
        help='Environment variables as key=value;key2=value2'
    )

    # ===== List Types =====
    parser.add_argument(
        '--ids',
        type=int,
        nargs='+',
        help='List of integer IDs'
    )

    parser.add_argument(
        '--ratios',
        type=float,
        nargs='*',
        help='List of float ratios'
    )

    # Parse arguments
    args = parser.parse_args()

    # Display parsed values
    print("Type Coercion Results:")

    print("\nBuilt-in Types:")
    print(f"  Port (int): {args.port} - type: {type(args.port).__name__}")
    print(f"  Timeout (float): {args.timeout} - type: {type(args.timeout).__name__}")
    if args.config:
        print(f"  Config (Path): {args.config} - type: {type(args.config).__name__}")

    print("\nCustom Types:")
    if args.date:
        print(f"  Date: {args.date} - type: {type(args.date).__name__}")
    if args.datetime:
        print(f"  Datetime: {args.datetime}")
    if args.url:
        print(f"  URL: {args.url}")
    if args.size:
        print(f"  Size: {args.size} bytes ({args.size / (1024**3):.2f} GB)")
    if args.duration:
        print(f"  Duration: {args.duration} seconds ({args.duration / 3600:.2f} hours)")
    if args.percentage is not None:
        print(f"  Percentage: {args.percentage}%")
    if args.tags:
        print(f"  Tags: {args.tags}")
    if args.env:
        print(f"  Environment:")
        for key, value in args.env.items():
            print(f"    {key} = {value}")

    print("\nList Types:")
    if args.ids:
        print(f"  IDs: {args.ids}")
    if args.ratios:
        print(f"  Ratios: {args.ratios}")

    # Clean up file handles
    if args.output:
        args.output.close()
    if args.input:
        args.input.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
