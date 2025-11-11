# Validation Patterns with argparse

Custom validators, type checking, and error handling.

## Template Reference

`templates/choices-validation.py`

## Overview

Robust argument validation:
- Built-in choices validation
- Custom type validators
- Range validation
- Pattern matching (regex)
- File/path validation

## Quick Start

```bash
# Valid inputs
python choices-validation.py --log-level debug --port 8080
python choices-validation.py --region us-east-1 --email user@example.com

# Invalid inputs (will error)
python choices-validation.py --log-level invalid  # Not in choices
python choices-validation.py --port 99999         # Out of range
python choices-validation.py --email invalid      # Invalid format
```

## Validation Methods

### 1. Choices (Built-in)

```python
parser.add_argument(
    '--log-level',
    choices=['debug', 'info', 'warning', 'error', 'critical'],
    default='info',
    help='Logging level'
)
```

**Automatic validation** - argparse rejects invalid values.

### 2. Custom Type Validator

```python
def validate_port(value):
    """Validate port number is 1-65535."""
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

    if ivalue < 1 or ivalue > 65535:
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid port (must be 1-65535)"
        )
    return ivalue


parser.add_argument(
    '--port',
    type=validate_port,
    default=8080,
    help='Server port (1-65535)'
)
```

### 3. Regex Pattern Validation

```python
import re

def validate_email(value):
    """Validate email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid email address"
        )
    return value


parser.add_argument('--email', type=validate_email)
```

### 4. IP Address Validation

```python
def validate_ip(value):
    """Validate IPv4 address."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(
            f"{value} is not a valid IP address"
        )

    # Check each octet is 0-255
    octets = [int(x) for x in value.split('.')]
    if any(o < 0 or o > 255 for o in octets):
        raise argparse.ArgumentTypeError(
            f"{value} contains invalid octets"
        )
    return value


parser.add_argument('--host', type=validate_ip)
```

### 5. Path Validation

```python
from pathlib import Path

def validate_path_exists(value):
    """Validate path exists."""
    path = Path(value)
    if not path.exists():
        raise argparse.ArgumentTypeError(
            f"Path does not exist: {value}"
        )
    return path


parser.add_argument('--config', type=validate_path_exists)
```

### 6. Range Validation Factory

```python
def validate_range(min_val, max_val):
    """Factory function for range validators."""
    def validator(value):
        try:
            ivalue = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"{value} is not a valid integer"
            )

        if ivalue < min_val or ivalue > max_val:
            raise argparse.ArgumentTypeError(
                f"{value} must be between {min_val} and {max_val}"
            )
        return ivalue
    return validator


# Usage
parser.add_argument(
    '--workers',
    type=validate_range(1, 32),
    default=4,
    help='Number of workers (1-32)'
)
```

## Complete Validation Example

```python
#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


def validate_port(value):
    ivalue = int(value)
    if not (1 <= ivalue <= 65535):
        raise argparse.ArgumentTypeError(
            f"Port must be 1-65535, got {value}"
        )
    return ivalue


def validate_email(value):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise argparse.ArgumentTypeError(
            f"Invalid email: {value}"
        )
    return value


def main():
    parser = argparse.ArgumentParser(
        description='Validation examples'
    )

    # Choices
    parser.add_argument(
        '--env',
        choices=['dev', 'staging', 'prod'],
        required=True,
        help='Environment (required)'
    )

    # Custom validators
    parser.add_argument('--port', type=validate_port, default=8080)
    parser.add_argument('--email', type=validate_email)

    # Path validation
    parser.add_argument(
        '--config',
        type=lambda x: Path(x) if Path(x).exists() else
              parser.error(f"File not found: {x}"),
        help='Config file (must exist)'
    )

    args = parser.parse_args()

    print(f"Environment: {args.env}")
    print(f"Port: {args.port}")
    if args.email:
        print(f"Email: {args.email}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## Post-Parse Validation

Sometimes you need to validate relationships between arguments:

```python
args = parser.parse_args()

# Validate argument combinations
if args.ssl and not (args.cert and args.key):
    parser.error("--ssl requires both --cert and --key")

if args.output and args.output.exists() and not args.force:
    parser.error(f"Output file exists: {args.output}. Use --force to overwrite")

# Validate argument ranges
if args.start_date > args.end_date:
    parser.error("Start date must be before end date")
```

## Error Messages

### Built-in Error Format

```bash
$ python mycli.py --env invalid
usage: mycli.py [-h] --env {dev,staging,prod}
mycli.py: error: argument --env: invalid choice: 'invalid'
(choose from 'dev', 'staging', 'prod')
```

### Custom Error Format

```python
def validate_port(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Port must be an integer (got '{value}')"
        )

    if ivalue < 1 or ivalue > 65535:
        raise argparse.ArgumentTypeError(
            f"Port {ivalue} is out of range (valid: 1-65535)"
        )
    return ivalue
```

```bash
$ python mycli.py --port 99999
usage: mycli.py [-h] [--port PORT]
mycli.py: error: argument --port: Port 99999 is out of range (valid: 1-65535)
```

## Common Validation Patterns

### URL Validation

```python
import re

def validate_url(value):
    pattern = r'^https?://[\w\.-]+\.\w+(:\d+)?(/.*)?$'
    if not re.match(pattern, value):
        raise argparse.ArgumentTypeError(f"Invalid URL: {value}")
    return value
```

### Date Validation

```python
from datetime import datetime

def validate_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date: {value} (expected YYYY-MM-DD)"
        )
```

### File Extension Validation

```python
def validate_json_file(value):
    path = Path(value)
    if path.suffix != '.json':
        raise argparse.ArgumentTypeError(
            f"File must have .json extension: {value}"
        )
    return path
```

### Percentage Validation

```python
def validate_percentage(value):
    try:
        pct = float(value.rstrip('%'))
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid percentage: {value}")

    if not (0 <= pct <= 100):
        raise argparse.ArgumentTypeError(
            f"Percentage must be 0-100: {value}"
        )
    return pct
```

## Best Practices

### ✓ Do: Fail Early

```python
# Validate during parsing
parser.add_argument('--port', type=validate_port)

# Not after parsing
args = parser.parse_args()
if not valid_port(args.port):  # ✗ Too late
    sys.exit(1)
```

### ✓ Do: Provide Clear Messages

```python
# ✓ Clear, actionable error
raise argparse.ArgumentTypeError(
    f"Port {value} is out of range (valid: 1-65535)"
)

# ✗ Vague error
raise argparse.ArgumentTypeError("Invalid port")
```

### ✓ Do: Use Choices When Possible

```python
# ✓ Let argparse handle it
parser.add_argument('--env', choices=['dev', 'staging', 'prod'])

# ✗ Manual validation
parser.add_argument('--env')
if args.env not in ['dev', 'staging', 'prod']:
    parser.error("Invalid environment")
```

### ✓ Do: Validate Type Before Range

```python
def validate_port(value):
    # First ensure it's an integer
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not an integer: {value}")

    # Then check range
    if not (1 <= ivalue <= 65535):
        raise argparse.ArgumentTypeError(f"Out of range: {ivalue}")

    return ivalue
```

## Testing Validation

```python
import pytest
from io import StringIO
import sys


def test_valid_port():
    """Test valid port number."""
    parser = create_parser()
    args = parser.parse_args(['--port', '8080'])
    assert args.port == 8080


def test_invalid_port():
    """Test invalid port number."""
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--port', '99999'])


def test_invalid_choice():
    """Test invalid choice."""
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--env', 'invalid'])
```

## Next Steps

- **Advanced Patterns:** See `advanced-parsing.md`
- **Type Coercion:** See `templates/type-coercion.py`
- **Custom Actions:** See `templates/custom-actions.py`
