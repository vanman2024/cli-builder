# Basic CLI Example

Simple type-safe CLI demonstrating fundamental Typer patterns.

## Features

- Type hints on all parameters
- Path validation
- Optional output file
- Boolean flags
- Verbose mode

## Usage

```bash
# Process and display
python cli.py input.txt

# Process and save
python cli.py input.txt --output result.txt

# Convert to uppercase
python cli.py input.txt --uppercase

# Verbose output
python cli.py input.txt --verbose
```

## Testing

```bash
# Create test file
echo "hello world" > test.txt

# Run CLI
python cli.py test.txt --uppercase
# Output: HELLO WORLD

# Save to file
python cli.py test.txt --output out.txt --uppercase --verbose
# Outputs: Processing: test.txt
#          ✓ Written to: out.txt
```

## Key Patterns

1. **Path type**: Automatic validation of file existence
2. **Optional parameters**: Using `Optional[Path]` for optional output
3. **Boolean flags**: Simple `bool` type for flags
4. **Colored output**: Using `typer.secho()` for success messages
