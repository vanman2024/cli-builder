# Typer Patterns - Quick Start

Modern type-safe CLI patterns for building maintainable command-line applications with Typer.

## Structure

```
typer-patterns/
├── SKILL.md                  # Main skill documentation
├── templates/                # 5 production-ready templates
│   ├── basic-typed-command.py       # Simple type-safe CLI
│   ├── enum-options.py              # Enum-based choices
│   ├── sub-app-structure.py         # Multi-command hierarchy
│   ├── typer-instance.py            # Factory pattern
│   └── advanced-validation.py       # Custom validators
├── scripts/                  # 5 helper scripts
│   ├── validate-types.sh            # Type hint validation
│   ├── generate-cli.sh              # CLI generator
│   ├── test-cli.sh                  # CLI testing
│   ├── convert-argparse.sh          # Migration guide
│   └── validate-skill.sh            # Skill validation
└── examples/                 # 4 complete examples
    ├── basic-cli/                   # Simple CLI example
    ├── enum-cli/                    # Enum usage example
    ├── subapp-cli/                  # Sub-commands example
    └── factory-cli/                 # Testable factory pattern

```

## Quick Usage

### Generate a new CLI

```bash
cd skills/typer-patterns
./scripts/generate-cli.sh basic my_cli.py --app-name myapp
```

### Validate type hints

```bash
./scripts/validate-types.sh my_cli.py
```

### Test CLI functionality

```bash
./scripts/test-cli.sh my_cli.py
```

## Templates at a Glance

| Template | Use Case | Key Features |
|----------|----------|--------------|
| **basic-typed-command.py** | Simple CLIs | Type hints, Path validation, Options |
| **enum-options.py** | Constrained choices | Enums, autocomplete, match/case |
| **sub-app-structure.py** | Complex CLIs | Sub-apps, shared context, hierarchy |
| **typer-instance.py** | Testable CLIs | Factory pattern, DI, mocking |
| **advanced-validation.py** | Custom validation | Callbacks, validators, protocols |

## Example: Quick CLI in 5 Minutes

1. **Copy template**
   ```bash
   cp templates/basic-typed-command.py my_cli.py
   ```

2. **Customize**
   ```python
   # Edit my_cli.py - change function names, add logic
   ```

3. **Validate**
   ```bash
   ./scripts/validate-types.sh my_cli.py
   ```

4. **Test**
   ```bash
   python my_cli.py --help
   ```

## Type Safety Checklist

- [ ] All parameters have type hints
- [ ] Return types specified on all functions
- [ ] Use `Path` for file/directory parameters
- [ ] Use `Enum` for constrained choices
- [ ] Use `Optional[T]` for optional parameters
- [ ] Add docstrings for help text

## Common Patterns

### Type Hints
```python
def process(
    input: Path = typer.Argument(...),
    output: Optional[Path] = typer.Option(None),
    count: int = typer.Option(10),
    verbose: bool = typer.Option(False)
) -> None:
```

### Enums
```python
class Format(str, Enum):
    json = "json"
    yaml = "yaml"

def export(format: Format = typer.Option(Format.json)) -> None:
```

### Sub-Apps
```python
app = typer.Typer()
db_app = typer.Typer()
app.add_typer(db_app, name="db")

@db_app.command("migrate")
def db_migrate() -> None:
```

### Factory Pattern
```python
def create_app(config: Config) -> typer.Typer:
    app = typer.Typer()
    # Define commands with config access
    return app
```

## Next Steps

1. Review `SKILL.md` for comprehensive patterns
2. Study `examples/` for working code
3. Use `scripts/` to automate common tasks
4. Customize templates for your use case

## Validation Results

Skill validation: **PASSED** ✓
- SKILL.md: Valid frontmatter and structure
- Templates: 5 templates (minimum 4 required)
- Scripts: 5 scripts (minimum 3 required)
- Examples: 4 complete examples with READMEs
- Security: No hardcoded secrets detected
