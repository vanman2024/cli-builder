# Rich Console Integration Example

This example shows how to integrate Fire CLI with Rich library for beautiful terminal output.

## Generate Rich CLI

```bash
./scripts/generate-fire-cli.sh \
  --name "Monitor" \
  --description "System monitoring CLI" \
  --template rich \
  --output monitor.py
```

## Rich Features

### Tables

Display data in formatted tables:

```python
from rich.table import Table

def list_items(self):
    """List items with table formatting"""
    items = [
        {"id": 1, "name": "Service A", "status": "active", "uptime": "99.9%"},
        {"id": 2, "name": "Service B", "status": "down", "uptime": "0%"},
        {"id": 3, "name": "Service C", "status": "pending", "uptime": "N/A"},
    ]

    table = Table(title="System Services", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=6)
    table.add_column("Name", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Uptime", justify="right", style="blue")

    for item in items:
        # Dynamic styling based on status
        status_style = {
            "active": "green",
            "down": "red",
            "pending": "yellow"
        }.get(item['status'], "white")

        table.add_row(
            str(item['id']),
            item['name'],
            f"[{status_style}]{item['status']}[/{status_style}]",
            item['uptime']
        )

    console.print(table)
    return items
```

Usage:
```bash
python monitor.py list-items
```

Output:
```
                    System Services
┏━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃ ID   ┃ Name      ┃ Status  ┃ Uptime ┃
┡━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ 1    │ Service A │ active  │  99.9% │
│ 2    │ Service B │ down    │     0% │
│ 3    │ Service C │ pending │    N/A │
└──────┴───────────┴─────────┴────────┘
```

### Progress Bars

Show progress for long-running operations:

```python
from rich.progress import track
import time

def process(self, count=100):
    """Process items with progress bar

    Args:
        count: Number of items to process
    """
    console.print("[cyan]Starting processing...[/cyan]")

    results = []
    for i in track(range(count), description="Processing..."):
        time.sleep(0.01)  # Simulate work
        results.append(i)

    console.print("[green]✓[/green] Processing complete!")
    return {"processed": len(results)}
```

Usage:
```bash
python monitor.py process --count=50
```

Output:
```
Starting processing...
Processing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
✓ Processing complete!
```

### Panels

Display information in bordered panels:

```python
from rich.panel import Panel

def status(self):
    """Display system status"""
    panel = Panel(
        "[bold green]System Running[/bold green]\n"
        "Version: 1.0.0\n"
        "Uptime: 24 hours\n"
        "Load: [yellow]0.45[/yellow]\n"
        "Memory: [blue]45%[/blue]",
        title="System Status",
        border_style="green"
    )
    console.print(panel)

    return {
        "status": "running",
        "version": "1.0.0",
        "uptime": "24h"
    }
```

Usage:
```bash
python monitor.py status
```

Output:
```
╭─────── System Status ────────╮
│ System Running               │
│ Version: 1.0.0               │
│ Uptime: 24 hours             │
│ Load: 0.45                   │
│ Memory: 45%                  │
╰──────────────────────────────╯
```

### Trees

Display hierarchical data:

```python
from rich.tree import Tree

def show_structure(self):
    """Display project structure"""
    tree = Tree("📁 Project Root")

    src = tree.add("📁 src")
    src.add("📄 main.py")
    src.add("📄 config.py")

    tests = tree.add("📁 tests")
    tests.add("📄 test_main.py")
    tests.add("📄 test_config.py")

    tree.add("📄 README.md")
    tree.add("📄 requirements.txt")

    console.print(tree)
```

Usage:
```bash
python monitor.py show-structure
```

Output:
```
📁 Project Root
├── 📁 src
│   ├── 📄 main.py
│   └── 📄 config.py
├── 📁 tests
│   ├── 📄 test_main.py
│   └── 📄 test_config.py
├── 📄 README.md
└── 📄 requirements.txt
```

### Styled Output

Use rich markup for styled text:

```python
def deploy(self, environment):
    """Deploy to environment

    Args:
        environment: Target environment
    """
    console.print(f"[bold cyan]Deploying to {environment}...[/bold cyan]")
    console.print("[dim]Step 1: Building...[/dim]")
    console.print("[dim]Step 2: Testing...[/dim]")
    console.print("[dim]Step 3: Uploading...[/dim]")
    console.print("[green]✓[/green] Deployment complete!")

    # Error example
    if environment == "production":
        console.print("[red]⚠ Production deployment requires approval[/red]")
```

### Color Palette

Common rich colors and styles:

```python
# Colors
console.print("[red]Error message[/red]")
console.print("[green]Success message[/green]")
console.print("[yellow]Warning message[/yellow]")
console.print("[blue]Info message[/blue]")
console.print("[cyan]Action message[/cyan]")
console.print("[magenta]Highlight[/magenta]")

# Styles
console.print("[bold]Bold text[/bold]")
console.print("[dim]Dimmed text[/dim]")
console.print("[italic]Italic text[/italic]")
console.print("[underline]Underlined text[/underline]")

# Combinations
console.print("[bold red]Bold red text[/bold red]")
console.print("[dim yellow]Dimmed yellow text[/dim yellow]")

# Emojis
console.print("✓ Success")
console.print("✗ Failure")
console.print("⚠ Warning")
console.print("ℹ Info")
console.print("→ Next step")
console.print("🚀 Deploy")
console.print("📦 Package")
```

## Complete Rich CLI Example

```python
import fire
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import time

console = Console()

class Monitor:
    """System monitoring CLI with rich output"""

    def __init__(self):
        self.version = "1.0.0"

    def status(self):
        """Display comprehensive status"""
        # Header panel
        console.print(Panel(
            "[bold green]System Online[/bold green]",
            title="Monitor Status",
            border_style="green"
        ))

        # Services table
        table = Table(title="Services")
        table.add_column("Service", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Load", justify="right")

        table.add_row("API", "[green]●[/green] Running", "45%")
        table.add_row("DB", "[green]●[/green] Running", "23%")
        table.add_row("Cache", "[yellow]●[/yellow] Degraded", "78%")

        console.print(table)

    def deploy(self, env='staging'):
        """Deploy with visual feedback"""
        console.print(Panel(
            f"[bold]Deploying to {env}[/bold]",
            border_style="cyan"
        ))

        steps = ["Build", "Test", "Upload", "Verify"]
        for step in track(steps, description="Deploying..."):
            time.sleep(0.5)

        console.print("[green]✓[/green] Deployment successful!")

if __name__ == '__main__':
    fire.Fire(Monitor)
```

## Installation

```bash
pip install fire rich
```

## Best Practices

1. **Use Console Instance**: Create one `Console()` instance and reuse it
2. **Consistent Colors**: Use consistent colors for similar message types
3. **Progress for Long Tasks**: Always show progress for operations >1 second
4. **Tables for Lists**: Use tables instead of plain text for structured data
5. **Panels for Sections**: Use panels to separate different output sections
6. **Emojis Sparingly**: Use emojis to enhance, not clutter
7. **Test in Different Terminals**: Rich output varies by terminal capabilities
