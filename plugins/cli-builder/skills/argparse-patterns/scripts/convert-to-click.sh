#!/usr/bin/env bash
# Convert argparse code to Click decorators

set -euo pipefail

usage() {
    cat <<EOF
Convert argparse parser to Click decorators

Usage: $(basename "$0") ARGPARSE_FILE [OUTPUT_FILE]

Performs basic conversion from argparse to Click:
    - ArgumentParser → @click.group() or @click.command()
    - add_argument() → @click.option() or @click.argument()
    - add_subparsers() → @group.command()
    - choices=[] → type=click.Choice([])
    - action='store_true' → is_flag=True

Note: This is a basic converter. Manual refinement may be needed.

Examples:
    $(basename "$0") mycli.py mycli_click.py
    $(basename "$0") basic-parser.py
EOF
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

ARGPARSE_FILE="$1"
OUTPUT_FILE="${2:-}"

if [ ! -f "$ARGPARSE_FILE" ]; then
    echo "Error: File not found: $ARGPARSE_FILE"
    exit 1
fi

echo "Converting argparse to Click: $ARGPARSE_FILE"

convert_to_click() {
    cat <<'EOF'
#!/usr/bin/env python3
"""
Converted from argparse to Click

This is a basic conversion. You may need to adjust:
- Argument order and grouping
- Type conversions
- Custom validators
- Error handling
"""

import click


@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    """CLI tool converted from argparse"""
    ctx.ensure_object(dict)


# Convert your subcommands here
# Example pattern:
#
# @cli.command()
# @click.argument('target')
# @click.option('--env', type=click.Choice(['dev', 'staging', 'prod']), default='dev')
# @click.option('--force', is_flag=True, help='Force operation')
# def deploy(target, env, force):
#     """Deploy to environment"""
#     click.echo(f"Deploying {target} to {env}")
#     if force:
#         click.echo("Force mode enabled")


if __name__ == '__main__':
    cli()
EOF

    echo ""
    echo "# Detected argparse patterns:"
    echo ""

    # Detect subcommands
    if grep -q "add_subparsers(" "$ARGPARSE_FILE"; then
        echo "# Subcommands found:"
        grep -oP "add_parser\('\K[^']+(?=')" "$ARGPARSE_FILE" | while read -r cmd; do
            echo "#   - $cmd"
        done
        echo ""
    fi

    # Detect arguments
    if grep -q "add_argument(" "$ARGPARSE_FILE"; then
        echo "# Arguments found:"
        grep "add_argument(" "$ARGPARSE_FILE" | grep -oP "'[^']+'" | head -n1 | while read -r arg; do
            echo "#   $arg"
        done
        echo ""
    fi

    # Detect choices
    if grep -q "choices=" "$ARGPARSE_FILE"; then
        echo "# Choices found (convert to click.Choice):"
        grep -oP "choices=\[\K[^\]]+(?=\])" "$ARGPARSE_FILE" | while read -r choices; do
            echo "#   [$choices]"
        done
        echo ""
    fi

    # Provide conversion hints
    cat <<'EOF'

# Conversion Guide:
#
# argparse                          → Click
# ----------------------------------|--------------------------------
# parser.add_argument('arg')        → @click.argument('arg')
# parser.add_argument('--opt')      → @click.option('--opt')
# action='store_true'               → is_flag=True
# choices=['a', 'b']                → type=click.Choice(['a', 'b'])
# type=int                          → type=int
# required=True                     → required=True
# default='value'                   → default='value'
# help='...'                        → help='...'
#
# For nested subcommands:
# Use @group.command() decorator
#
# For more info: https://click.palletsprojects.com/
EOF
}

# Output
if [ -n "$OUTPUT_FILE" ]; then
    convert_to_click > "$OUTPUT_FILE"
    chmod +x "$OUTPUT_FILE"
    echo "Converted to Click: $OUTPUT_FILE"
    echo ""
    echo "Next steps:"
    echo "  1. Review the generated file"
    echo "  2. Add your command implementations"
    echo "  3. Install Click: pip install click"
    echo "  4. Test: python $OUTPUT_FILE --help"
else
    convert_to_click
fi
