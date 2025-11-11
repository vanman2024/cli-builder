# Nested Subcommands

Multi-level command hierarchies like `git config get` or `kubectl config view`.

## Template Reference

`templates/nested-subparser.py`

## Overview

Create deep command structures:
- `mycli config get key`
- `mycli config set key value`
- `mycli deploy start production`
- `mycli deploy stop production`

## Quick Start

```bash
# Two-level commands
python nested-subparser.py config get database_url
python nested-subparser.py config set api_key abc123
python nested-subparser.py config list

# Deploy subcommands
python nested-subparser.py deploy start production --replicas 3
python nested-subparser.py deploy stop staging
```

## Architecture

```
mycli
├── config
│   ├── get <key>
│   ├── set <key> <value>
│   ├── list
│   └── delete <key>
└── deploy
    ├── start <environment>
    ├── stop <environment>
    └── restart <environment>
```

## Implementation Pattern

### 1. Main Parser

```python
parser = argparse.ArgumentParser(description='Multi-level CLI')
subparsers = parser.add_subparsers(dest='command', required=True)
```

### 2. First-Level Subcommand

```python
# Create 'config' command group
config_parser = subparsers.add_parser(
    'config',
    help='Manage configuration'
)

# Create second-level subparsers under 'config'
config_subparsers = config_parser.add_subparsers(
    dest='config_command',
    required=True
)
```

### 3. Second-Level Subcommands

```python
# config get
config_get = config_subparsers.add_parser('get', help='Get value')
config_get.add_argument('key', help='Configuration key')
config_get.set_defaults(func=config_get_handler)

# config set
config_set = config_subparsers.add_parser('set', help='Set value')
config_set.add_argument('key', help='Configuration key')
config_set.add_argument('value', help='Configuration value')
config_set.add_argument('--force', action='store_true')
config_set.set_defaults(func=config_set_handler)
```

## Complete Example

```python
#!/usr/bin/env python3
import argparse
import sys


# Config handlers
def config_get(args):
    print(f"Getting: {args.key}")
    return 0


def config_set(args):
    print(f"Setting: {args.key} = {args.value}")
    return 0


# Deploy handlers
def deploy_start(args):
    print(f"Starting deployment to {args.environment}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='Nested CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # === Config group ===
    config_parser = subparsers.add_parser('config', help='Configuration')
    config_subs = config_parser.add_subparsers(
        dest='config_command',
        required=True
    )

    # config get
    get_parser = config_subs.add_parser('get')
    get_parser.add_argument('key')
    get_parser.set_defaults(func=config_get)

    # config set
    set_parser = config_subs.add_parser('set')
    set_parser.add_argument('key')
    set_parser.add_argument('value')
    set_parser.set_defaults(func=config_set)

    # === Deploy group ===
    deploy_parser = subparsers.add_parser('deploy', help='Deployment')
    deploy_subs = deploy_parser.add_subparsers(
        dest='deploy_command',
        required=True
    )

    # deploy start
    start_parser = deploy_subs.add_parser('start')
    start_parser.add_argument('environment')
    start_parser.set_defaults(func=deploy_start)

    # Parse and dispatch
    args = parser.parse_args()
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
```

## Accessing Nested Commands

```python
args = parser.parse_args()

# Top-level command
print(args.command)  # 'config' or 'deploy'

# Second-level command
if args.command == 'config':
    print(args.config_command)  # 'get', 'set', 'list', 'delete'
elif args.command == 'deploy':
    print(args.deploy_command)  # 'start', 'stop', 'restart'
```

## Help Output

### Top-Level Help

```
usage: mycli [-h] {config,deploy} ...

positional arguments:
  {config,deploy}
    config         Manage configuration
    deploy         Manage deployments
```

### Second-Level Help

```bash
$ python mycli.py config --help

usage: mycli config [-h] {get,set,list,delete} ...

positional arguments:
  {get,set,list,delete}
    get              Get configuration value
    set              Set configuration value
    list             List all configuration
    delete           Delete configuration value
```

### Third-Level Help

```bash
$ python mycli.py config set --help

usage: mycli config set [-h] [-f] key value

positional arguments:
  key          Configuration key
  value        Configuration value

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  Overwrite existing value
```

## Dispatch Pattern

### Option 1: Manual Switch

```python
args = parser.parse_args()

if args.command == 'config':
    if args.config_command == 'get':
        config_get(args)
    elif args.config_command == 'set':
        config_set(args)
elif args.command == 'deploy':
    if args.deploy_command == 'start':
        deploy_start(args)
```

### Option 2: Function Dispatch (Recommended)

```python
# Set handlers when creating parsers
config_get.set_defaults(func=config_get_handler)
config_set.set_defaults(func=config_set_handler)
deploy_start.set_defaults(func=deploy_start_handler)

# Simple dispatch
args = parser.parse_args()
return args.func(args)
```

## Best Practices

### 1. Consistent Naming

```python
# ✓ Good - consistent dest naming
config_parser.add_subparsers(dest='config_command')
deploy_parser.add_subparsers(dest='deploy_command')
```

### 2. Set Required

```python
# ✓ Good - require subcommand
config_subs = config_parser.add_subparsers(
    dest='config_command',
    required=True
)
```

### 3. Provide Help

```python
# ✓ Good - descriptive help at each level
config_parser = subparsers.add_parser(
    'config',
    help='Manage configuration',
    description='Configuration management commands'
)
```

### 4. Use set_defaults

```python
# ✓ Good - easy dispatch
get_parser.set_defaults(func=config_get)
```

## How Deep Should You Go?

### ✓ Good: 2-3 Levels

```
mycli config get key
mycli deploy start production
```

### ⚠️ Consider alternatives: 4+ Levels

```
mycli server database config get key  # Too deep
```

**Alternatives:**
- Flatten: `mycli db-config-get key`
- Split: Separate CLI tools
- Use flags: `mycli config get key --scope=server --type=database`

## Common Mistakes

### ❌ Wrong: Same dest name

```python
# Both use 'command' - second overwrites first
config_subs = config_parser.add_subparsers(dest='command')
deploy_subs = deploy_parser.add_subparsers(dest='command')
```

```python
# ✓ Correct - unique dest names
config_subs = config_parser.add_subparsers(dest='config_command')
deploy_subs = deploy_parser.add_subparsers(dest='deploy_command')
```

### ❌ Wrong: Accessing wrong level

```python
args = parser.parse_args(['config', 'get', 'key'])

print(args.command)         # ✓ 'config'
print(args.config_command)  # ✓ 'get'
print(args.deploy_command)  # ✗ Error - not set
```

### ❌ Wrong: Not checking hierarchy

```python
# ✗ Assumes deploy command
print(args.deploy_command)
```

```python
# ✓ Check first
if args.command == 'deploy':
    print(args.deploy_command)
```

## Real-World Examples

### Git-style

```
git config --global user.name "Name"
git remote add origin url
git branch --list
```

### Kubectl-style

```
kubectl config view
kubectl get pods --namespace default
kubectl logs pod-name --follow
```

### Docker-style

```
docker container ls
docker image build -t name .
docker network create name
```

## Next Steps

- **Validation:** See `validation-patterns.md`
- **Advanced:** See `advanced-parsing.md`
- **Compare frameworks:** See templates for Click/Typer equivalents
