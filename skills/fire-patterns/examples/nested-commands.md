# Nested Commands Example

This example demonstrates using nested classes to organize related commands into groups.

## Generate Nested CLI

```bash
./scripts/generate-fire-cli.sh \
  --name "DeployTool" \
  --description "Deployment management tool" \
  --template nested \
  --output deploy_tool.py
```

## Command Structure

```
deploy_tool.py
├── config               # Configuration group
│   ├── get             # Get config value
│   ├── set             # Set config value
│   ├── list            # List all config
│   └── reset           # Reset config
├── resources            # Resources group
│   ├── create          # Create resource
│   ├── delete          # Delete resource
│   └── list            # List resources
└── info                 # Display info
```

## Usage Examples

### Configuration Management

```bash
# Set configuration value
python deploy_tool.py config set api_key abc123

# Get configuration value
python deploy_tool.py config get api_key
# Output: api_key: abc123

# List all configuration
python deploy_tool.py config list
# Output:
# Configuration:
#   api_key: abc123
#   endpoint: https://api.example.com

# Reset configuration
python deploy_tool.py config reset --confirm
```

### Resource Management

```bash
# Create resource with default template
python deploy_tool.py resources create my-resource

# Create resource with custom template
python deploy_tool.py resources create my-resource --template=advanced

# List all resources
python deploy_tool.py resources list
# Output:
# Resources:
#   • item1
#   • item2
#   • item3

# Delete resource (requires confirmation)
python deploy_tool.py resources delete my-resource
# Output: ⚠ Use --confirm to delete resource

python deploy_tool.py resources delete my-resource --confirm
# Output: ✓ resource deleted
```

### Display Information

```bash
python deploy_tool.py info
# Output:
# DeployTool v1.0.0
# Config file: /home/user/.deploytool/config.json
```

## Implementation Pattern

### Main CLI Class

```python
class DeployTool:
    """Main CLI application"""

    def __init__(self):
        self.version = "1.0.0"
        self.config_file = Path.home() / ".deploytool" / "config.json"
        # Initialize nested command groups
        self.config = self.Config(self)
        self.resources = self.Resources()

    def info(self):
        """Display CLI information"""
        console.print(f"[bold]DeployTool[/bold] v{self.version}")
        return {"version": self.version}
```

### Nested Command Group

```python
class Config:
    """Configuration management commands"""

    def __init__(self, parent):
        self.parent = parent  # Access to main CLI instance

    def get(self, key):
        """Get configuration value

        Args:
            key: Configuration key to retrieve
        """
        config = self._load_config()
        value = config.get(key)
        console.print(f"[blue]{key}[/blue]: {value}")
        return value

    def set(self, key, value):
        """Set configuration value

        Args:
            key: Configuration key to set
            value: Configuration value
        """
        config = self._load_config()
        config[key] = value
        self._save_config(config)
        console.print(f"[green]✓[/green] Set {key} = {value}")

    def _load_config(self):
        """Private helper method (not exposed as command)"""
        if not self.parent.config_file.exists():
            return {}
        return json.loads(self.parent.config_file.read_text())

    def _save_config(self, config):
        """Private helper method (not exposed as command)"""
        self.parent.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.parent.config_file.write_text(json.dumps(config, indent=2))
```

## Key Concepts

### Parent Access

Nested classes can access the parent CLI instance:

```python
class Config:
    def __init__(self, parent):
        self.parent = parent  # Store parent reference

    def some_command(self):
        # Access parent properties
        version = self.parent.version
        config_file = self.parent.config_file
```

### Private Methods

Methods starting with `_` are not exposed as CLI commands:

```python
def list(self):
    """Public command - accessible via CLI"""
    pass

def _load_config(self):
    """Private helper - not accessible via CLI"""
    pass
```

### Multiple Nesting Levels

You can nest command groups multiple levels deep:

```python
class CLI:
    class Database:
        """Database commands"""

        class Migration:
            """Migration subcommands"""

            def up(self):
                """Run migrations up"""
                pass

            def down(self):
                """Run migrations down"""
                pass

# Usage:
# python cli.py database migration up
# python cli.py database migration down
```

## Help Navigation

### Top-Level Help

```bash
python deploy_tool.py --help
```

Shows all command groups and top-level commands.

### Group-Level Help

```bash
python deploy_tool.py config --help
```

Shows all commands in the `config` group.

### Command-Level Help

```bash
python deploy_tool.py config set --help
```

Shows help for specific command including arguments.

## Best Practices

1. **Logical Grouping**: Group related commands together
2. **Clear Names**: Use descriptive names for groups and commands
3. **Parent Access**: Use parent reference to share state
4. **Private Helpers**: Use `_` prefix for helper methods
5. **Comprehensive Docs**: Document each command group and command
6. **Shallow Nesting**: Keep nesting to 2-3 levels maximum

## Advanced Pattern: Shared Context

```python
class CLI:
    def __init__(self):
        self.context = {"verbose": False, "config": {}}

    class Commands:
        def __init__(self, parent):
            self.parent = parent

        def run(self, verbose=False):
            """Run command"""
            self.parent.context["verbose"] = verbose
            if verbose:
                console.print("[dim]Verbose mode enabled[/dim]")
```

This allows sharing state across command groups through the parent context.
