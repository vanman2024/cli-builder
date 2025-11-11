#!/usr/bin/env bash
# Validate argparse parser structure and completeness

set -euo pipefail

usage() {
    cat <<EOF
Validate argparse parser structure

Usage: $(basename "$0") PARSER_FILE

Checks:
    - Valid Python syntax
    - Imports argparse
    - Creates ArgumentParser
    - Has main() function
    - Calls parse_args()
    - Has proper shebang
    - Has help text
    - Has version info

Examples:
    $(basename "$0") mycli.py
    $(basename "$0") ../templates/basic-parser.py
EOF
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

PARSER_FILE="$1"

if [ ! -f "$PARSER_FILE" ]; then
    echo "Error: File not found: $PARSER_FILE"
    exit 1
fi

echo "Validating argparse parser: $PARSER_FILE"
echo ""

ERRORS=0
WARNINGS=0

# Check shebang
if head -n1 "$PARSER_FILE" | grep -q '^#!/usr/bin/env python'; then
    echo "✓ Has proper Python shebang"
else
    echo "✗ Missing or invalid shebang"
    ((ERRORS++))
fi

# Check syntax
if python3 -m py_compile "$PARSER_FILE" 2>/dev/null; then
    echo "✓ Valid Python syntax"
else
    echo "✗ Invalid Python syntax"
    ((ERRORS++))
fi

# Check imports
if grep -q "import argparse" "$PARSER_FILE"; then
    echo "✓ Imports argparse"
else
    echo "✗ Does not import argparse"
    ((ERRORS++))
fi

# Check ArgumentParser creation
if grep -q "ArgumentParser(" "$PARSER_FILE"; then
    echo "✓ Creates ArgumentParser"
else
    echo "✗ Does not create ArgumentParser"
    ((ERRORS++))
fi

# Check main function
if grep -q "^def main(" "$PARSER_FILE"; then
    echo "✓ Has main() function"
else
    echo "⚠ No main() function found"
    ((WARNINGS++))
fi

# Check parse_args call
if grep -q "\.parse_args()" "$PARSER_FILE"; then
    echo "✓ Calls parse_args()"
else
    echo "✗ Does not call parse_args()"
    ((ERRORS++))
fi

# Check version
if grep -q "action='version'" "$PARSER_FILE"; then
    echo "✓ Has version info"
else
    echo "⚠ No version info found"
    ((WARNINGS++))
fi

# Check help text
if grep -q "help=" "$PARSER_FILE"; then
    echo "✓ Has help text for arguments"
else
    echo "⚠ No help text found"
    ((WARNINGS++))
fi

# Check description
if grep -q "description=" "$PARSER_FILE"; then
    echo "✓ Has parser description"
else
    echo "⚠ No parser description"
    ((WARNINGS++))
fi

# Check if executable
if [ -x "$PARSER_FILE" ]; then
    echo "✓ File is executable"
else
    echo "⚠ File is not executable (run: chmod +x $PARSER_FILE)"
    ((WARNINGS++))
fi

# Check subparsers if present
if grep -q "add_subparsers(" "$PARSER_FILE"; then
    echo "✓ Has subparsers"

    # Check if dest is set
    if grep -q "add_subparsers(.*dest=" "$PARSER_FILE"; then
        echo "  ✓ Subparsers have dest set"
    else
        echo "  ⚠ Subparsers missing dest parameter"
        ((WARNINGS++))
    fi
fi

# Check for choices
if grep -q "choices=" "$PARSER_FILE"; then
    echo "✓ Uses choices for validation"
fi

# Check for type coercion
if grep -q "type=" "$PARSER_FILE"; then
    echo "✓ Uses type coercion"
fi

# Check for argument groups
if grep -q "add_argument_group(" "$PARSER_FILE"; then
    echo "✓ Uses argument groups"
fi

# Check for mutually exclusive groups
if grep -q "add_mutually_exclusive_group(" "$PARSER_FILE"; then
    echo "✓ Uses mutually exclusive groups"
fi

# Summary
echo ""
echo "Validation Summary:"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "✓ Parser validation passed"
    exit 0
else
    echo ""
    echo "✗ Parser validation failed"
    exit 1
fi
