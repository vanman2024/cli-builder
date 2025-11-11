#!/bin/bash
# Helper script to convert argparse CLI to Typer (guidance)

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

cat << 'EOF'
Converting argparse to Typer
=============================

This script provides guidance on converting argparse CLIs to Typer.

Common Conversions:
-------------------

1. Argument Parser Setup
   argparse: parser = ArgumentParser()
   Typer:    app = typer.Typer()

2. Positional Arguments
   argparse: parser.add_argument('name')
   Typer:    name: str = typer.Argument(...)

3. Optional Arguments
   argparse: parser.add_argument('--flag', '-f')
   Typer:    flag: bool = typer.Option(False, '--flag', '-f')

4. Required Options
   argparse: parser.add_argument('--name', required=True)
   Typer:    name: str = typer.Option(...)

5. Default Values
   argparse: parser.add_argument('--count', default=10)
   Typer:    count: int = typer.Option(10)

6. Type Conversion
   argparse: parser.add_argument('--port', type=int)
   Typer:    port: int = typer.Option(8000)

7. Choices/Enums
   argparse: parser.add_argument('--format', choices=['json', 'yaml'])
   Typer:    format: Format = typer.Option(Format.json)  # Format is Enum

8. File Arguments
   argparse: parser.add_argument('--input', type=argparse.FileType('r'))
   Typer:    input: Path = typer.Option(...)

9. Help Text
   argparse: parser.add_argument('--name', help='User name')
   Typer:    name: str = typer.Option(..., help='User name')

10. Subcommands
    argparse: subparsers = parser.add_subparsers()
    Typer:    sub_app = typer.Typer(); app.add_typer(sub_app, name='sub')

Example Conversion:
-------------------

BEFORE (argparse):
    parser = ArgumentParser()
    parser.add_argument('input', help='Input file')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

AFTER (Typer):
    app = typer.Typer()

    @app.command()
    def main(
        input: Path = typer.Argument(..., help='Input file'),
        output: Optional[Path] = typer.Option(None, '--output', '-o'),
        verbose: bool = typer.Option(False, '--verbose', '-v')
    ) -> None:
        """Process input file."""
        pass

    if __name__ == '__main__':
        app()

Benefits of Typer:
------------------
✓ Automatic type validation
✓ Better IDE support with type hints
✓ Less boilerplate code
✓ Built-in help generation
✓ Easier testing
✓ Rich formatting support

Next Steps:
-----------
1. Identify all argparse patterns in your CLI
2. Use templates from this skill as reference
3. Convert incrementally, one command at a time
4. Run validation: ./scripts/validate-types.sh
5. Test thoroughly: ./scripts/test-cli.sh

EOF

echo -e "${BLUE}For specific conversion help, provide your argparse CLI code.${NC}"
