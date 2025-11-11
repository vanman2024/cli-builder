# Basic argparse Usage

Simple CLI with positional and optional arguments using Python's standard library.

## Template Reference

`templates/basic-parser.py`

## Overview

Demonstrates fundamental argparse patterns:
- Positional arguments (required)
- Optional arguments with flags
- Boolean flags
- Type coercion
- Default values
- Help text generation

## Quick Start

```bash
# View help
python basic-parser.py --help

# Basic usage
python basic-parser.py deploy my-app

# With optional arguments
python basic-parser.py deploy my-app --env staging --timeout 60

# Boolean flags
python basic-parser.py deploy my-app --force

# Verbose mode (count occurrences)
python basic-parser.py deploy my-app -vvv
```

## Key Patterns

### 1. Create Parser

```python
import argparse

parser = argparse.ArgumentParser(
    description='Deploy application to specified environment',
    formatter_class=argparse.RawDescriptionHelpFormatter
)
```

**Why `RawDescriptionHelpFormatter`?**
- Preserves formatting in epilog (usage examples)
- Better control over help text layout

### 2. Add Version

```python
parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s 1.0.0'
)
```

**Usage:** `python mycli.py --version`

### 3. Positional Arguments

```python
parser.add_argument(
    'app_name',
    help='Name of the application to deploy'
)
```

**Required by default** - no flag needed, just the value.

### 4. Optional Arguments

```python
parser.add_argument(
    '--env', '-e',
    default='development',
    help='Deployment environment (default: %(default)s)'
)
```

**Note:** `%(default)s` automatically shows default value in help.

### 5. Type Coercion

```python
parser.add_argument(
    '--timeout', '-t',
    type=int,
    default=30,
    help='Timeout in seconds'
)
```

**Automatic validation** - argparse will error if non-integer provided.

### 6. Boolean Flags

```python
parser.add_argument(
    '--force', '-f',
    action='store_true',
    help='Force deployment without confirmation'
)
```

**Result:**
- Present: `args.force = True`
- Absent: `args.force = False`

### 7. Count Action

```python
parser.add_argument(
    '--verbose', '-v',
    action='count',
    default=0,
    help='Increase verbosity (-v, -vv, -vvv)'
)
```

**Usage:**
- `-v`: verbosity = 1
- `-vv`: verbosity = 2
- `-vvv`: verbosity = 3

## Complete Example

```python
#!/usr/bin/env python3
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Simple deployment tool'
    )

    parser.add_argument('--version', action='version', version='1.0.0')

    parser.add_argument('app_name', help='Application name')
    parser.add_argument('--env', default='dev', help='Environment')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout')
    parser.add_argument('--force', action='store_true', help='Force')

    args = parser.parse_args()

    print(f"Deploying {args.app_name} to {args.env}")
    print(f"Timeout: {args.timeout}s")
    print(f"Force: {args.force}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## Help Output

```
usage: basic-parser.py [-h] [--version] [--env ENV] [--timeout TIMEOUT]
                       [--force] [--verbose]
                       action app_name

Deploy application to specified environment

positional arguments:
  action                Action to perform
  app_name              Name of the application to deploy

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --env ENV, -e ENV     Deployment environment (default: development)
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout in seconds (default: 30)
  --force, -f           Force deployment without confirmation
  --verbose, -v         Increase verbosity (-v, -vv, -vvv)
```

## Common Mistakes

### ❌ Wrong: Accessing before parsing

```python
args = parser.parse_args()
print(args.env)  # ✓ Correct
```

```python
print(args.env)  # ✗ Wrong - args doesn't exist yet
args = parser.parse_args()
```

### ❌ Wrong: Not checking boolean flags

```python
if args.force:  # ✓ Correct
    print("Force mode")
```

```python
if args.force == True:  # ✗ Unnecessary comparison
    print("Force mode")
```

### ❌ Wrong: Manual type conversion

```python
parser.add_argument('--port', type=int)  # ✓ Let argparse handle it
```

```python
parser.add_argument('--port')
port = int(args.port)  # ✗ Manual conversion (error-prone)
```

## Next Steps

- **Subcommands:** See `subcommands.md`
- **Validation:** See `validation-patterns.md`
- **Advanced:** See `advanced-parsing.md`
