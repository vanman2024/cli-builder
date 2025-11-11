# Subcommands with argparse

Multi-command CLI like `git`, `docker`, or `kubectl` using subparsers.

## Template Reference

`templates/subparser-pattern.py`

## Overview

Create CLIs with multiple commands:
- `mycli init` - Initialize project
- `mycli deploy production` - Deploy to environment
- `mycli status` - Show status

Each subcommand has its own arguments and options.

## Quick Start

```bash
# View main help
python subparser-pattern.py --help

# View subcommand help
python subparser-pattern.py init --help
python subparser-pattern.py deploy --help

# Execute subcommands
python subparser-pattern.py init --template react
python subparser-pattern.py deploy production --force
python subparser-pattern.py status --format json
```

## Key Patterns

### 1. Create Subparsers

```python
parser = argparse.ArgumentParser(description='Multi-command CLI')

subparsers = parser.add_subparsers(
    dest='command',        # Store command name in args.command
    help='Available commands',
    required=True          # At least one command required (Python 3.7+)
)
```

**Important:** Set `dest='command'` to access which command was used.

### 2. Add Subcommand

```python
init_parser = subparsers.add_parser(
    'init',
    help='Initialize a new project',
    description='Initialize a new project with specified template'
)

init_parser.add_argument('--template', default='basic')
init_parser.add_argument('--path', default='.')
```

Each subcommand is a separate parser with its own arguments.

### 3. Set Command Handler

```python
def cmd_init(args):
    """Initialize project."""
    print(f"Initializing with {args.template} template...")

init_parser.set_defaults(func=cmd_init)
```

**Dispatch pattern:**

```python
args = parser.parse_args()
return args.func(args)  # Call the appropriate handler
```

### 4. Subcommand with Choices

```python
deploy_parser = subparsers.add_parser('deploy')

deploy_parser.add_argument(
    'environment',
    choices=['development', 'staging', 'production'],
    help='Target environment'
)

deploy_parser.add_argument(
    '--mode',
    choices=['fast', 'safe', 'rollback'],
    default='safe'
)
```

## Complete Example

```python
#!/usr/bin/env python3
import argparse
import sys


def cmd_init(args):
    print(f"Initializing with {args.template} template")
    return 0


def cmd_deploy(args):
    print(f"Deploying to {args.environment}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='My CLI Tool')
    parser.add_argument('--version', action='version', version='1.0.0')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize project')
    init_parser.add_argument('--template', default='basic')
    init_parser.set_defaults(func=cmd_init)

    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy app')
    deploy_parser.add_argument(
        'environment',
        choices=['dev', 'staging', 'prod']
    )
    deploy_parser.set_defaults(func=cmd_deploy)

    # Parse and dispatch
    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
```

## Help Output

### Main Help

```
usage: mycli [-h] [--version] {init,deploy,status} ...

Multi-command CLI tool

positional arguments:
  {init,deploy,status}  Available commands
    init                Initialize a new project
    deploy              Deploy application to environment
    status              Show deployment status

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

### Subcommand Help

```bash
$ python mycli.py deploy --help

usage: mycli deploy [-h] [-f] [-m {fast,safe,rollback}]
                    {development,staging,production}

positional arguments:
  {development,staging,production}
                        Target environment

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Force deployment without confirmation
  -m {fast,safe,rollback}, --mode {fast,safe,rollback}
                        Deployment mode (default: safe)
```

## Accessing Parsed Values

```python
args = parser.parse_args()

# Which command was used?
print(args.command)  # 'init', 'deploy', or 'status'

# Command-specific arguments
if args.command == 'deploy':
    print(args.environment)  # 'production'
    print(args.force)        # True/False
    print(args.mode)         # 'safe'
```

## Common Patterns

### Pattern 1: Switch on Command

```python
args = parser.parse_args()

if args.command == 'init':
    init_project(args)
elif args.command == 'deploy':
    deploy_app(args)
elif args.command == 'status':
    show_status(args)
```

### Pattern 2: Function Dispatch (Better)

```python
# Set handlers
init_parser.set_defaults(func=cmd_init)
deploy_parser.set_defaults(func=cmd_deploy)

# Dispatch
args = parser.parse_args()
return args.func(args)
```

### Pattern 3: Check if Command Provided

```python
args = parser.parse_args()

if not args.command:
    parser.print_help()
    sys.exit(1)
```

**Note:** Use `required=True` in `add_subparsers()` to make this automatic.

## Common Mistakes

### ❌ Wrong: Forgetting dest

```python
subparsers = parser.add_subparsers(dest='command')  # ✓ Can check args.command
```

```python
subparsers = parser.add_subparsers()  # ✗ Can't access which command
```

### ❌ Wrong: Accessing wrong argument

```python
# deploy_parser defines 'environment'
# init_parser defines 'template'

args = parser.parse_args(['deploy', 'prod'])
print(args.environment)  # ✓ Correct
print(args.template)     # ✗ Error - not defined for deploy
```

### ❌ Wrong: No required=True (Python 3.7+)

```python
subparsers = parser.add_subparsers(dest='command', required=True)  # ✓
```

```python
subparsers = parser.add_subparsers(dest='command')  # ✗ Command optional
# User can run: python mycli.py (no command)
```

## Nested Subcommands

For multi-level commands like `git config get`, see:
- `nested-commands.md`
- `templates/nested-subparser.py`

## Next Steps

- **Nested Commands:** See `nested-commands.md`
- **Validation:** See `validation-patterns.md`
- **Complex CLIs:** See `advanced-parsing.md`
