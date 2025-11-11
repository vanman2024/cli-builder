#!/usr/bin/env python3
"""
Argument choices and custom validation patterns.

Usage:
    python choices-validation.py --log-level debug
    python choices-validation.py --port 8080 --host 192.168.1.1
    python choices-validation.py --region us-east-1 --instance-type t2.micro
"""

import argparse
import re
import sys
from pathlib import Path


def validate_port(value):
    """Custom validator for port numbers."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

    if ivalue < 1 or ivalue > 65535:
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid port (must be 1-65535)"
        )
    return ivalue


def validate_ip(value):
    """Custom validator for IP addresses."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(f"{value} is not a valid IP address")

    # Check each octet is 0-255
    octets = [int(x) for x in value.split('.')]
    if any(o < 0 or o > 255 for o in octets):
        raise argparse.ArgumentTypeError(
            f"{value} contains invalid octets (must be 0-255)"
        )
    return value


def validate_email(value):
    """Custom validator for email addresses."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(f"{value} is not a valid email address")
    return value


def validate_path_exists(value):
    """Custom validator to check if path exists."""
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"Path does not exist: {value}")
    return path


def validate_range(min_val, max_val):
    """Factory function for range validators."""
    def validator(value):
        try:
            ivalue = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

        if ivalue < min_val or ivalue > max_val:
            raise argparse.ArgumentTypeError(
                f"{value} must be between {min_val} and {max_val}"
            )
        return ivalue
    return validator


def main():
    parser = argparse.ArgumentParser(
        description='Demonstrate choices and validation patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== String Choices =====
    parser.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info',
        help='Logging level (default: %(default)s)'
    )

    parser.add_argument(
        '--region',
        choices=[
            'us-east-1', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-central-1',
            'ap-southeast-1', 'ap-northeast-1'
        ],
        default='us-east-1',
        help='AWS region (default: %(default)s)'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'toml', 'xml'],
        default='json',
        help='Output format (default: %(default)s)'
    )

    # ===== Custom Validators =====
    parser.add_argument(
        '--port',
        type=validate_port,
        default=8080,
        help='Server port (1-65535, default: %(default)s)'
    )

    parser.add_argument(
        '--host',
        type=validate_ip,
        default='127.0.0.1',
        help='Server host IP (default: %(default)s)'
    )

    parser.add_argument(
        '--email',
        type=validate_email,
        help='Email address for notifications'
    )

    parser.add_argument(
        '--config',
        type=validate_path_exists,
        help='Path to configuration file (must exist)'
    )

    # ===== Range Validators =====
    parser.add_argument(
        '--workers',
        type=validate_range(1, 32),
        default=4,
        help='Number of worker processes (1-32, default: %(default)s)'
    )

    parser.add_argument(
        '--timeout',
        type=validate_range(1, 3600),
        default=30,
        help='Request timeout in seconds (1-3600, default: %(default)s)'
    )

    # ===== Integer Choices =====
    parser.add_argument(
        '--instance-type',
        choices=['t2.micro', 't2.small', 't2.medium', 't3.large'],
        default='t2.micro',
        help='EC2 instance type (default: %(default)s)'
    )

    # ===== Type Coercion =====
    parser.add_argument(
        '--memory',
        type=float,
        default=1.0,
        help='Memory limit in GB (default: %(default)s)'
    )

    parser.add_argument(
        '--retry-count',
        type=int,
        default=3,
        help='Number of retries (default: %(default)s)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Display parsed values
    print("Configuration:")
    print(f"  Log Level: {args.log_level}")
    print(f"  Region: {args.region}")
    print(f"  Format: {args.format}")
    print(f"  Port: {args.port}")
    print(f"  Host: {args.host}")
    print(f"  Email: {args.email}")
    print(f"  Config: {args.config}")
    print(f"  Workers: {args.workers}")
    print(f"  Timeout: {args.timeout}s")
    print(f"  Instance Type: {args.instance_type}")
    print(f"  Memory: {args.memory}GB")
    print(f"  Retry Count: {args.retry_count}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
