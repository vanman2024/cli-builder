#!/bin/bash
# Validate type hints in Typer CLI files

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file provided
if [ $# -eq 0 ]; then
    echo -e "${RED}✗ Usage: $0 <python-file>${NC}"
    exit 1
fi

FILE="$1"

# Check if file exists
if [ ! -f "$FILE" ]; then
    echo -e "${RED}✗ File not found: $FILE${NC}"
    exit 1
fi

echo "Validating type hints in: $FILE"
echo "----------------------------------------"

ERRORS=0

# Check for type hints on function parameters
echo "Checking function parameter type hints..."
UNTYPED_PARAMS=$(grep -n "def " "$FILE" | while read -r line; do
    LINE_NUM=$(echo "$line" | cut -d: -f1)
    LINE_CONTENT=$(echo "$line" | cut -d: -f2-)

    # Extract parameter list
    PARAMS=$(echo "$LINE_CONTENT" | sed -n 's/.*def [^(]*(\(.*\)).*/\1/p')

    # Check if any parameter lacks type hint (excluding self, ctx)
    if echo "$PARAMS" | grep -qE '[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*=' | \
       grep -vE '[a-zA-Z_][a-zA-Z0-9_]*[[:space:]]*:[[:space:]]*[a-zA-Z]'; then
        echo "  Line $LINE_NUM: Missing type hint"
        ((ERRORS++))
    fi
done)

if [ -z "$UNTYPED_PARAMS" ]; then
    echo -e "${GREEN}✓ All parameters have type hints${NC}"
else
    echo -e "${RED}$UNTYPED_PARAMS${NC}"
fi

# Check for return type hints
echo "Checking function return type hints..."
MISSING_RETURN=$(grep -n "def " "$FILE" | grep -v "-> " | while read -r line; do
    LINE_NUM=$(echo "$line" | cut -d: -f1)
    echo "  Line $LINE_NUM: Missing return type hint"
    ((ERRORS++))
done)

if [ -z "$MISSING_RETURN" ]; then
    echo -e "${GREEN}✓ All functions have return type hints${NC}"
else
    echo -e "${RED}$MISSING_RETURN${NC}"
fi

# Check for Typer imports
echo "Checking Typer imports..."
if ! grep -q "^import typer" "$FILE" && ! grep -q "^from typer import" "$FILE"; then
    echo -e "${RED}✗ Missing typer import${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ Typer imported${NC}"
fi

# Check for typing imports when using Optional, Union, etc.
echo "Checking typing imports..."
if grep -qE "Optional|Union|List|Dict|Tuple" "$FILE"; then
    if ! grep -q "from typing import" "$FILE"; then
        echo -e "${YELLOW}⚠ Using typing types but missing typing import${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✓ Typing imports present${NC}"
    fi
else
    echo -e "${YELLOW}⚠ No typing annotations detected${NC}"
fi

# Check for Path usage
echo "Checking Path usage for file parameters..."
if grep -qE "file|path|dir" "$FILE" | grep -i "str.*=.*typer"; then
    echo -e "${YELLOW}⚠ Consider using Path type instead of str for file/path parameters${NC}"
else
    echo -e "${GREEN}✓ No obvious Path type issues${NC}"
fi

# Check for Enum usage
echo "Checking for Enum patterns..."
if grep -qE "class.*\(str, Enum\)" "$FILE"; then
    echo -e "${GREEN}✓ Enum classes found${NC}"
else
    echo -e "${YELLOW}⚠ No Enum classes detected (consider for constrained choices)${NC}"
fi

# Check for docstrings
echo "Checking command docstrings..."
MISSING_DOCS=$(grep -A1 "def " "$FILE" | grep -v '"""' | wc -l)
if [ "$MISSING_DOCS" -gt 0 ]; then
    echo -e "${YELLOW}⚠ Some functions may be missing docstrings${NC}"
else
    echo -e "${GREEN}✓ Docstrings appear present${NC}"
fi

echo "----------------------------------------"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Validation passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s)${NC}"
    exit 1
fi
