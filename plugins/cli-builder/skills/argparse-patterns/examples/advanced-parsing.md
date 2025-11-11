# Advanced argparse Patterns

Complex argument parsing scenarios and advanced techniques.

## Templates Reference

- `templates/custom-actions.py`
- `templates/mutually-exclusive.py`
- `templates/argument-groups.py`
- `templates/variadic-args.py`

## Overview

Advanced patterns:
- Custom action classes
- Mutually exclusive groups
- Argument groups (organization)
- Variadic arguments (nargs)
- Environment variable fallback
- Config file integration
- Subparser inheritance

## 1. Custom Actions

Create custom argument processing logic.

### Simple Custom Action

```python
class UpperCaseAction(argparse.Action):
    """Convert value to uppercase."""

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())


parser.add_argument('--name', action=UpperCaseAction)
```

### Key-Value Action

```python
class KeyValueAction(argparse.Action):
    """Parse key=value pairs."""

    def __call__(self, parser, namespace, values, option_string=None):
        if '=' not in values:
            parser.error(f"Must be key=value format: {values}")

        key, value = values.split('=', 1)
        items = getattr(namespace, self.dest, {}) or {}
        items[key] = value
        setattr(namespace, self.dest, items)


parser.add_argument(
    '--env', '-e',
    action=KeyValueAction,
    help='Environment variable (key=value)'
)

# Usage: --env API_KEY=abc123 --env DB_URL=postgres://...
```

### Load File Action

```python
class LoadFileAction(argparse.Action):
    """Load and parse file content."""

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            with open(values, 'r') as f:
                content = f.read()
            setattr(namespace, self.dest, content)
        except Exception as e:
            parser.error(f"Cannot load file {values}: {e}")


parser.add_argument('--config', action=LoadFileAction)
```

## 2. Mutually Exclusive Groups

Ensure only one option from a group is used.

### Basic Exclusivity

```python
group = parser.add_mutually_exclusive_group()
group.add_argument('--json', help='Output as JSON')
group.add_argument('--yaml', help='Output as YAML')
group.add_argument('--xml', help='Output as XML')

# Valid: --json output.json
# Valid: --yaml output.yaml
# Invalid: --json output.json --yaml output.yaml
```

### Required Exclusive Group

```python
mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument('--create', metavar='NAME')
mode_group.add_argument('--update', metavar='NAME')
mode_group.add_argument('--delete', metavar='NAME')
mode_group.add_argument('--list', action='store_true')

# Must specify exactly one: create, update, delete, or list
```

### Multiple Exclusive Groups

```python
# Output format group
output = parser.add_mutually_exclusive_group()
output.add_argument('--json', action='store_true')
output.add_argument('--yaml', action='store_true')

# Verbosity group
verbosity = parser.add_mutually_exclusive_group()
verbosity.add_argument('--verbose', action='store_true')
verbosity.add_argument('--quiet', action='store_true')

# Can use one from each group:
# Valid: --json --verbose
# Invalid: --json --yaml
```

## 3. Argument Groups

Organize arguments for better help display.

```python
parser = argparse.ArgumentParser()

# Server configuration
server_group = parser.add_argument_group(
    'server configuration',
    'Options for configuring the web server'
)
server_group.add_argument('--host', default='127.0.0.1')
server_group.add_argument('--port', type=int, default=8080)
server_group.add_argument('--workers', type=int, default=4)

# Database configuration
db_group = parser.add_argument_group(
    'database configuration',
    'Options for database connection'
)
db_group.add_argument('--db-host', default='localhost')
db_group.add_argument('--db-port', type=int, default=5432)
db_group.add_argument('--db-name', required=True)

# Logging configuration
log_group = parser.add_argument_group(
    'logging configuration',
    'Options for logging and monitoring'
)
log_group.add_argument('--log-level',
                       choices=['debug', 'info', 'warning', 'error'],
                       default='info')
log_group.add_argument('--log-file', help='Log to file')
```

**Help output groups arguments logically.**

## 4. Variadic Arguments (nargs)

Handle variable number of arguments.

### Optional Single Argument (?)

```python
parser.add_argument(
    '--output',
    nargs='?',
    const='default.json',  # Used if flag present, no value
    default=None,          # Used if flag not present
    help='Output file'
)

# --output           → 'default.json'
# --output file.json → 'file.json'
# (no flag)          → None
```

### Zero or More (*)

```python
parser.add_argument(
    '--include',
    nargs='*',
    default=[],
    help='Include patterns'
)

# --include          → []
# --include *.py     → ['*.py']
# --include *.py *.md → ['*.py', '*.md']
```

### One or More (+)

```python
parser.add_argument(
    'files',
    nargs='+',
    help='Input files (at least one required)'
)

# file1.txt          → ['file1.txt']
# file1.txt file2.txt → ['file1.txt', 'file2.txt']
# (no files)         → Error: required
```

### Exact Number

```python
parser.add_argument(
    '--range',
    nargs=2,
    type=int,
    metavar=('START', 'END'),
    help='Range as start end'
)

# --range 1 10 → [1, 10]
# --range 1    → Error: expected 2
```

### Remainder

```python
parser.add_argument(
    '--command',
    nargs=argparse.REMAINDER,
    help='Pass-through command and args'
)

# mycli --command python script.py --arg1 --arg2
# → command = ['python', 'script.py', '--arg1', '--arg2']
```

## 5. Environment Variable Fallback

```python
import os

parser = argparse.ArgumentParser()

parser.add_argument(
    '--api-key',
    default=os.environ.get('API_KEY'),
    help='API key (default: $API_KEY)'
)

parser.add_argument(
    '--db-url',
    default=os.environ.get('DATABASE_URL'),
    help='Database URL (default: $DATABASE_URL)'
)

# Precedence: CLI arg > Environment variable > Default
```

## 6. Config File Integration

```python
import configparser

def load_config(config_file):
    """Load configuration from INI file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


parser = argparse.ArgumentParser()

parser.add_argument('--config', help='Config file')
parser.add_argument('--host', help='Server host')
parser.add_argument('--port', type=int, help='Server port')

args = parser.parse_args()

# Load config file if specified
if args.config:
    config = load_config(args.config)

    # Use config values as defaults if not specified on CLI
    if not args.host:
        args.host = config.get('server', 'host', fallback='127.0.0.1')

    if not args.port:
        args.port = config.getint('server', 'port', fallback=8080)
```

## 7. Parent Parsers (Inheritance)

Share common arguments across subcommands.

```python
# Parent parser with common arguments
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--verbose', action='store_true')
parent_parser.add_argument('--config', help='Config file')

# Main parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

# Subcommands inherit from parent
deploy_parser = subparsers.add_parser(
    'deploy',
    parents=[parent_parser],
    help='Deploy application'
)
deploy_parser.add_argument('environment')

build_parser = subparsers.add_parser(
    'build',
    parents=[parent_parser],
    help='Build application'
)
build_parser.add_argument('--target')

# Both subcommands have --verbose and --config
```

## 8. Argument Defaults from Dict

```python
defaults = {
    'host': '127.0.0.1',
    'port': 8080,
    'workers': 4,
    'timeout': 30.0
}

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port', type=int)
parser.add_argument('--workers', type=int)
parser.add_argument('--timeout', type=float)

# Set all defaults at once
parser.set_defaults(**defaults)
```

## 9. Namespace Manipulation

```python
# Pre-populate namespace
defaults = argparse.Namespace(
    host='127.0.0.1',
    port=8080,
    debug=False
)

args = parser.parse_args(namespace=defaults)

# Or modify after parsing
args = parser.parse_args()
args.computed_value = args.value1 + args.value2
```

## 10. Conditional Arguments

```python
args = parser.parse_args()

# Add conditional validation
if args.ssl and not (args.cert and args.key):
    parser.error("--ssl requires both --cert and --key")

# Add computed values
if args.workers == 'auto':
    import os
    args.workers = os.cpu_count()
```

## Complete Advanced Example

```python
#!/usr/bin/env python3
import argparse
import os
import sys


class KeyValueAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        key, value = values.split('=', 1)
        items = getattr(namespace, self.dest, {}) or {}
        items[key] = value
        setattr(namespace, self.dest, items)


def main():
    # Parent parser for common args
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument('--verbose', action='store_true')
    parent.add_argument('--config', help='Config file')

    # Main parser
    parser = argparse.ArgumentParser(
        description='Advanced argparse patterns'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Deploy command
    deploy = subparsers.add_parser(
        'deploy',
        parents=[parent],
        help='Deploy application'
    )

    # Mutually exclusive group
    format_group = deploy.add_mutually_exclusive_group()
    format_group.add_argument('--json', action='store_true')
    format_group.add_argument('--yaml', action='store_true')

    # Custom action
    deploy.add_argument(
        '--env', '-e',
        action=KeyValueAction,
        help='Environment variable'
    )

    # Variadic arguments
    deploy.add_argument(
        'targets',
        nargs='+',
        help='Deployment targets'
    )

    # Environment fallback
    deploy.add_argument(
        '--api-key',
        default=os.environ.get('API_KEY'),
        help='API key'
    )

    args = parser.parse_args()

    # Post-parse validation
    if args.command == 'deploy':
        if not args.api_key:
            parser.error("API key required (use --api-key or $API_KEY)")

    return 0


if __name__ == '__main__':
    sys.exit(main())
```

## Best Practices

1. **Use parent parsers** for shared arguments
2. **Use argument groups** for organization
3. **Use mutually exclusive groups** when appropriate
4. **Validate after parsing** for complex logic
5. **Provide environment fallbacks** for sensitive data
6. **Use custom actions** for complex transformations
7. **Document nargs behavior** in help text

## Next Steps

- Review template files for complete implementations
- Test patterns with `scripts/test-parser.sh`
- Compare with Click/Typer alternatives
