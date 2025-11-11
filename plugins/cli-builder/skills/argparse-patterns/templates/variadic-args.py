#!/usr/bin/env python3
"""
Variadic argument patterns (nargs: ?, *, +, number).

Usage:
    python variadic-args.py file1.txt file2.txt file3.txt
    python variadic-args.py --output result.json file1.txt file2.txt
    python variadic-args.py --include *.py --exclude test_*.py
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Variadic argument patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== nargs='?' (optional, 0 or 1) =====
    parser.add_argument(
        '--output',
        nargs='?',
        const='default.json',  # Used if flag present but no value
        default=None,  # Used if flag not present
        help='Output file (default: stdout, or default.json if flag present)'
    )

    parser.add_argument(
        '--config',
        nargs='?',
        const='config.yaml',
        help='Configuration file (default: config.yaml if flag present)'
    )

    # ===== nargs='*' (zero or more) =====
    parser.add_argument(
        '--include',
        nargs='*',
        default=[],
        help='Include patterns (zero or more)'
    )

    parser.add_argument(
        '--exclude',
        nargs='*',
        default=[],
        help='Exclude patterns (zero or more)'
    )

    parser.add_argument(
        '--tags',
        nargs='*',
        metavar='TAG',
        help='Tags to apply'
    )

    # ===== nargs='+' (one or more, required) =====
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='Input files (at least one required)'
    )

    parser.add_argument(
        '--servers',
        nargs='+',
        metavar='SERVER',
        help='Server addresses (at least one required if specified)'
    )

    # ===== nargs=N (exact number) =====
    parser.add_argument(
        '--coordinates',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Coordinates as latitude longitude'
    )

    parser.add_argument(
        '--range',
        nargs=2,
        type=int,
        metavar=('START', 'END'),
        help='Range as start end'
    )

    parser.add_argument(
        '--rgb',
        nargs=3,
        type=int,
        metavar=('R', 'G', 'B'),
        help='RGB color values (0-255)'
    )

    # ===== Remainder arguments =====
    parser.add_argument(
        '--command',
        nargs=argparse.REMAINDER,
        help='Command and arguments to pass through'
    )

    # Parse arguments
    args = parser.parse_args()

    # Display results
    print("Variadic Arguments Results:")

    print("\nnargs='?' (optional):")
    print(f"  Output: {args.output}")
    print(f"  Config: {args.config}")

    print("\nnargs='*' (zero or more):")
    print(f"  Include Patterns: {args.include if args.include else '(none)'}")
    print(f"  Exclude Patterns: {args.exclude if args.exclude else '(none)'}")
    print(f"  Tags: {args.tags if args.tags else '(none)'}")

    print("\nnargs='+' (one or more):")
    print(f"  Files ({len(args.files)}):")
    for f in args.files:
        print(f"    - {f}")
    if args.servers:
        print(f"  Servers ({len(args.servers)}):")
        for s in args.servers:
            print(f"    - {s}")

    print("\nnargs=N (exact number):")
    if args.coordinates:
        lat, lon = args.coordinates
        print(f"  Coordinates: {lat}, {lon}")
    if args.range:
        start, end = args.range
        print(f"  Range: {start} to {end}")
    if args.rgb:
        r, g, b = args.rgb
        print(f"  RGB Color: rgb({r}, {g}, {b})")

    print("\nRemaining arguments:")
    if args.command:
        print(f"  Command: {' '.join(args.command)}")

    # Example usage
    print("\nExample Processing:")
    print(f"Processing {len(args.files)} file(s)...")

    if args.include:
        print(f"Including patterns: {', '.join(args.include)}")
    if args.exclude:
        print(f"Excluding patterns: {', '.join(args.exclude)}")

    if args.output:
        print(f"Output will be written to: {args.output}")
    else:
        print("Output will be written to: stdout")

    return 0


if __name__ == '__main__':
    sys.exit(main())
