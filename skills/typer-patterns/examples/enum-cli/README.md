# Enum CLI Example

Type-safe CLI using Enums for constrained choices.

## Features

- Multiple Enum types (LogLevel, OutputFormat)
- Autocomplete support
- Type-safe matching with match/case
- Validated input values

## Usage

```bash
# Export as JSON (default)
python cli.py export

# Export as YAML
python cli.py export yaml

# Export with custom log level
python cli.py export json --log-level debug

# Save to file
python cli.py export yaml --output config.yaml

# Validate log level
python cli.py validate info
```

## Testing

```bash
# Export JSON to console
python cli.py export json
# Output: {"app": "example", "version": "1.0.0", ...}

# Export YAML to file
python cli.py export yaml --output test.yaml --log-level warning
# Creates test.yaml with YAML format

# Validate enum value
python cli.py validate error
# Output: Log Level: error
#         Severity: High - error messages

# Invalid enum (will fail with helpful message)
python cli.py export invalid
# Error: Invalid value for 'FORMAT': 'invalid' is not one of 'json', 'yaml', 'text'.
```

## Key Patterns

1. **Enum as Argument**: `format: OutputFormat = typer.Argument(...)`
2. **Enum as Option**: `log_level: LogLevel = typer.Option(...)`
3. **String Enum**: Inherit from `str, Enum` for string values
4. **Match/Case**: Use pattern matching with enum values
5. **Autocomplete**: Automatic shell completion for enum values

## Benefits

- Type safety at runtime and compile time
- IDE autocomplete for enum values
- Automatic validation of inputs
- Self-documenting constrained choices
- Easy to extend with new values
