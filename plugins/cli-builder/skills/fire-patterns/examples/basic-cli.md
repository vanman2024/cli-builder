# Basic Fire CLI Example

This example demonstrates creating a simple Fire CLI with basic commands.

## Generate Basic CLI

```bash
./scripts/generate-fire-cli.sh \
  --name "TaskManager" \
  --description "Simple task management CLI" \
  --template basic \
  --output task_manager.py
```

## Generated CLI Structure

```python
import fire
from rich.console import Console

console = Console()

class TaskManager:
    """Simple task management CLI"""

    def __init__(self):
        self.version = "1.0.0"
        self.verbose = False

    def init(self, name='my-project'):
        """Initialize a new project

        Args:
            name: Project name (default: my-project)
        """
        console.print(f"[green]✓[/green] Initializing project: {name}")
        return {"status": "success", "project": name}

    def build(self, verbose=False):
        """Build the project

        Args:
            verbose: Enable verbose output (default: False)
        """
        self.verbose = verbose
        if self.verbose:
            console.print("[dim]Verbose mode enabled[/dim]")

        console.print("[cyan]Building project...[/cyan]")
        console.print("[green]✓[/green] Build complete!")

if __name__ == '__main__':
    fire.Fire(TaskManager)
```

## Usage Examples

### Display Help

```bash
python task_manager.py --help
```

Output:
```
NAME
    task_manager.py

SYNOPSIS
    task_manager.py COMMAND

COMMANDS
    COMMAND is one of the following:

     init
       Initialize a new project

     build
       Build the project

     version_info
       Display version information
```

### Initialize Project

```bash
python task_manager.py init
# Uses default name 'my-project'

python task_manager.py init --name=my-app
# Custom project name
```

### Build with Verbose Mode

```bash
python task_manager.py build --verbose
```

### Get Version Information

```bash
python task_manager.py version-info
```

## Key Features

1. **Automatic Help Generation**: Fire generates help text from docstrings
2. **Type Conversion**: Fire automatically converts string arguments to correct types
3. **Default Values**: Parameter defaults become CLI defaults
4. **Boolean Flags**: `verbose=False` becomes `--verbose` flag
5. **Rich Output**: Integration with rich console for colored output

## Common Patterns

### Boolean Flags

```python
def deploy(self, force=False, dry_run=False):
    """Deploy application

    Args:
        force: Force deployment
        dry_run: Perform dry run only
    """
    pass

# Usage:
# python cli.py deploy --force
# python cli.py deploy --dry-run
# python cli.py deploy --noforce  # Explicit False
```

### Required vs Optional Arguments

```python
def create(self, name, template='default'):
    """Create resource

    Args:
        name: Resource name (required)
        template: Template to use (optional)
    """
    pass

# Usage:
# python cli.py create my-resource
# python cli.py create my-resource --template=advanced
```

### Returning Values

```python
def status(self):
    """Get status"""
    return {
        "running": True,
        "version": "1.0.0",
        "uptime": "24h"
    }

# Fire will display the returned dict
```

## Next Steps

1. Add more commands as methods
2. Use rich console for better output
3. Add configuration management
4. Implement nested classes for command groups
5. Add type hints for better IDE support
