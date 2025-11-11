# Factory Pattern CLI Example

Testable CLI using factory pattern with dependency injection.

## Features

- Factory function for app creation
- Dependency injection via Protocol
- Multiple storage implementations
- Configuration injection
- Highly testable structure

## Usage

```bash
# Save data
python cli.py save name "John Doe"
python cli.py save email "john@example.com"

# Load data
python cli.py load name
# Output: John Doe

python cli.py load email
# Output: john@example.com

# Show configuration
python cli.py config-show

# Use verbose mode
python cli.py --verbose save status "active"

# Custom data directory
python cli.py --data-dir /tmp/mydata save test "value"
```

## Testing Example

```python
# test_cli.py
from cli import create_app, Config, MemoryStorage
from typer.testing import CliRunner

def test_save_and_load():
    """Test save and load commands."""
    # Create test configuration
    config = Config(verbose=True)
    storage = MemoryStorage()

    # Create app with test dependencies
    app = create_app(config=config, storage=storage)

    # Test runner
    runner = CliRunner()

    # Test save
    result = runner.invoke(app, ["save", "test_key", "test_value"])
    assert result.exit_code == 0
    assert "Saved test_key" in result.output

    # Test load
    result = runner.invoke(app, ["load", "test_key"])
    assert result.exit_code == 0
    assert "test_value" in result.output
```

Run tests:
```bash
pytest test_cli.py
```

## Architecture

### Factory Function
```python
def create_app(config: Config, storage: Storage) -> typer.Typer:
    """Create app with injected dependencies."""
```

### Storage Protocol
```python
class Storage(Protocol):
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str: ...
```

### Implementations
- `MemoryStorage`: In-memory storage (for testing)
- `FileStorage`: File-based storage (for production)

## Key Patterns

1. **Factory Function**: Returns configured Typer app
2. **Protocol Types**: Interface for dependency injection
3. **Dataclass Config**: Type-safe configuration
4. **Dependency Injection**: Pass storage and config to factory
5. **Testability**: Easy to mock dependencies in tests

## Benefits

- Unit testable without file I/O
- Swap implementations easily
- Configuration flexibility
- Clean dependency management
- Follows SOLID principles
- Easy to extend with new storage types

## Extension Example

Add new storage type:

```python
class DatabaseStorage:
    """Database storage implementation."""

    def __init__(self, connection_string: str) -> None:
        self.conn = connect(connection_string)

    def save(self, key: str, value: str) -> None:
        self.conn.execute("INSERT INTO data VALUES (?, ?)", (key, value))

    def load(self, key: str) -> str:
        return self.conn.execute("SELECT value FROM data WHERE key = ?", (key,)).fetchone()

# Use it
storage = DatabaseStorage("postgresql://localhost/mydb")
app = create_app(storage=storage)
```
