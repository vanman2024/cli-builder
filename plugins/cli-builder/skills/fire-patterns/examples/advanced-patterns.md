# Advanced Fire CLI Patterns

This guide covers advanced patterns and techniques for building sophisticated Fire CLIs.

## Pattern 1: Configuration Management with Persistence

Implement persistent configuration storage:

```python
import fire
from rich.console import Console
from pathlib import Path
import json

console = Console()

class ConfigManager:
    """Handle configuration file I/O"""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self._ensure_exists()

    def _ensure_exists(self):
        """Create config file if missing"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self.save({})

    def load(self) -> dict:
        """Load configuration"""
        try:
            return json.loads(self.config_path.read_text())
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return {}

    def save(self, config: dict):
        """Save configuration"""
        self.config_path.write_text(json.dumps(config, indent=2))

class MyCLI:
    def __init__(self):
        self.config_manager = ConfigManager(
            Path.home() / ".mycli" / "config.json"
        )

    def configure(self, key, value):
        """Set configuration value"""
        config = self.config_manager.load()
        config[key] = value
        self.config_manager.save(config)
        console.print(f"[green]✓[/green] Set {key} = {value}")
```

## Pattern 2: Environment-Based Configuration

Handle multiple environments:

```python
from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"

class MyCLI:
    def __init__(self):
        self.current_env = Environment.DEV

    def set_env(self, env: Environment):
        """Switch environment

        Args:
            env: Target environment (dev, staging, production)
        """
        self.current_env = env
        console.print(f"[cyan]Environment: {env.value}[/cyan]")

    def deploy(self):
        """Deploy to current environment"""
        console.print(f"Deploying to {self.current_env.value}")

# Usage:
# python cli.py set-env staging
# python cli.py deploy
```

## Pattern 3: Property Access for Read-Only Values

Use properties for values that should be readable but not settable:

```python
class MyCLI:
    def __init__(self):
        self._version = "1.0.0"
        self._config_path = Path.home() / ".mycli"

    @property
    def version(self):
        """Get CLI version"""
        return self._version

    @property
    def config_path(self):
        """Get configuration path"""
        return str(self._config_path)

# Usage:
# python cli.py version      # Returns "1.0.0"
# python cli.py config-path  # Returns path
```

## Pattern 4: Validation and Error Handling

Implement robust validation:

```python
from pathlib import Path

class MyCLI:
    def deploy(self, path: str, confirm=False):
        """Deploy from path

        Args:
            path: Path to deployment files
            confirm: Skip confirmation prompt
        """
        deploy_path = Path(path)

        # Validate path exists
        if not deploy_path.exists():
            console.print(f"[red]Error: Path not found: {path}[/red]")
            return {"status": "error", "message": "Path not found"}

        # Validate path is directory
        if not deploy_path.is_dir():
            console.print(f"[red]Error: Not a directory: {path}[/red]")
            return {"status": "error", "message": "Not a directory"}

        # Require confirmation for sensitive operations
        if not confirm:
            console.print("[yellow]⚠ Use --confirm to proceed[/yellow]")
            return {"status": "cancelled"}

        # Perform deployment
        console.print(f"[green]Deploying from {path}...[/green]")
        return {"status": "success"}
```

## Pattern 5: Chaining Commands

Create chainable command patterns:

```python
class Builder:
    """Build pipeline with chaining"""

    def __init__(self):
        self.steps = []

    def clean(self):
        """Add clean step"""
        self.steps.append("clean")
        return self  # Return self for chaining

    def build(self):
        """Add build step"""
        self.steps.append("build")
        return self

    def test(self):
        """Add test step"""
        self.steps.append("test")
        return self

    def execute(self):
        """Execute pipeline"""
        for step in self.steps:
            console.print(f"[cyan]Running: {step}[/cyan]")
        return {"steps": self.steps}

class MyCLI:
    def __init__(self):
        self.builder = Builder()

# Usage:
# python cli.py builder clean
# python cli.py builder build
# python cli.py builder clean build test execute
```

## Pattern 6: Context Managers for Resources

Use context managers for resource handling:

```python
from contextlib import contextmanager

class MyCLI:
    @contextmanager
    def _deployment_context(self, env):
        """Context manager for deployments"""
        console.print(f"[cyan]Starting deployment to {env}...[/cyan]")
        try:
            yield
            console.print("[green]✓[/green] Deployment successful")
        except Exception as e:
            console.print(f"[red]✗ Deployment failed: {e}[/red]")
            raise
        finally:
            console.print("[dim]Cleanup complete[/dim]")

    def deploy(self, env='staging'):
        """Deploy with context management"""
        with self._deployment_context(env):
            # Deployment logic here
            console.print("  [dim]Building...[/dim]")
            console.print("  [dim]Uploading...[/dim]")
```

## Pattern 7: Plugin Architecture

Create extensible CLI with plugins:

```python
from abc import ABC, abstractmethod
from typing import List

class Plugin(ABC):
    """Base plugin class"""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute plugin"""
        pass

class DatabasePlugin(Plugin):
    """Database operations plugin"""

    def execute(self, operation):
        console.print(f"[cyan]Database: {operation}[/cyan]")

class CachePlugin(Plugin):
    """Cache operations plugin"""

    def execute(self, operation):
        console.print(f"[yellow]Cache: {operation}[/yellow]")

class MyCLI:
    def __init__(self):
        self.plugins: List[Plugin] = [
            DatabasePlugin(),
            CachePlugin()
        ]

    def run_plugins(self, operation):
        """Execute operation on all plugins

        Args:
            operation: Operation to run
        """
        for plugin in self.plugins:
            plugin.execute(operation)
```

## Pattern 8: Async Operations

Handle async operations in Fire CLI:

```python
import asyncio
from typing import List

class MyCLI:
    def fetch(self, urls: List[str]):
        """Fetch multiple URLs concurrently

        Args:
            urls: List of URLs to fetch
        """
        async def fetch_all():
            tasks = [self._fetch_one(url) for url in urls]
            return await asyncio.gather(*tasks)

        results = asyncio.run(fetch_all())
        return {"fetched": len(results)}

    async def _fetch_one(self, url):
        """Fetch single URL"""
        # Simulated async fetch
        await asyncio.sleep(0.1)
        return url

# Usage:
# python cli.py fetch https://example.com https://google.com
```

## Pattern 9: Dry Run Mode

Implement dry-run capability:

```python
class MyCLI:
    def __init__(self):
        self.dry_run = False

    def deploy(self, env, dry_run=False):
        """Deploy to environment

        Args:
            env: Target environment
            dry_run: Show what would happen without executing
        """
        self.dry_run = dry_run

        if self.dry_run:
            console.print("[yellow]DRY RUN MODE[/yellow]")

        self._execute("Build project", lambda: self._build())
        self._execute("Run tests", lambda: self._test())
        self._execute("Upload files", lambda: self._upload(env))

    def _execute(self, description, action):
        """Execute or simulate action"""
        if self.dry_run:
            console.print(f"[dim]Would: {description}[/dim]")
        else:
            console.print(f"[cyan]{description}...[/cyan]")
            action()

    def _build(self):
        pass  # Build logic

    def _test(self):
        pass  # Test logic

    def _upload(self, env):
        pass  # Upload logic
```

## Pattern 10: Logging Integration

Integrate structured logging:

```python
import logging
from pathlib import Path

class MyCLI:
    def __init__(self):
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging"""
        log_file = Path.home() / ".mycli" / "cli.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def deploy(self, env):
        """Deploy with logging"""
        self.logger.info(f"Starting deployment to {env}")
        try:
            console.print(f"[cyan]Deploying to {env}...[/cyan]")
            # Deployment logic
            self.logger.info("Deployment successful")
            console.print("[green]✓[/green] Deployed!")
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            console.print(f"[red]✗ Error: {e}[/red]")
            raise
```

## Pattern 11: Interactive Confirmation

Add interactive prompts:

```python
class MyCLI:
    def delete(self, resource, force=False):
        """Delete resource with confirmation

        Args:
            resource: Resource to delete
            force: Skip confirmation
        """
        if not force:
            console.print(f"[yellow]⚠ Delete {resource}?[/yellow]")
            console.print("[dim]Use --force to skip this prompt[/dim]")
            return

        console.print(f"[red]Deleting {resource}...[/red]")
        # Delete logic here
        console.print("[green]✓[/green] Deleted")
```

## Best Practices Summary

1. **Error Handling**: Always validate inputs and handle errors gracefully
2. **Confirmation**: Require confirmation for destructive operations
3. **Dry Run**: Implement dry-run mode for risky operations
4. **Logging**: Log important actions to file for audit trail
5. **Type Hints**: Use type hints for better IDE support
6. **Properties**: Use properties for read-only values
7. **Context Managers**: Use context managers for resource cleanup
8. **Enums**: Use Enums for constrained choices
9. **Async**: Use asyncio for concurrent operations
10. **Plugins**: Design for extensibility with plugin architecture
