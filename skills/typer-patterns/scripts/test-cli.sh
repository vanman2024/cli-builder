#!/bin/bash
# Test Typer CLI functionality

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if file provided
if [ $# -eq 0 ]; then
    echo -e "${RED}✗ Usage: $0 <python-file>${NC}"
    exit 1
fi

CLI_FILE="$1"

# Check if file exists
if [ ! -f "$CLI_FILE" ]; then
    echo -e "${RED}✗ File not found: $CLI_FILE${NC}"
    exit 1
fi

echo "Testing Typer CLI: $CLI_FILE"
echo "========================================"

TESTS_PASSED=0
TESTS_FAILED=0

# Test: Help command
echo "Test: Help output"
if python "$CLI_FILE" --help > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Help command works${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Help command failed${NC}"
    ((TESTS_FAILED++))
fi

# Test: Version flag (if supported)
echo "Test: Version flag"
if python "$CLI_FILE" --version > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Version flag works${NC}"
    ((TESTS_PASSED++))
elif grep -q "version" "$CLI_FILE"; then
    echo -e "${YELLOW}⚠ Version defined but flag not working${NC}"
else
    echo -e "${YELLOW}⚠ No version flag (optional)${NC}"
fi

# Test: Check for syntax errors
echo "Test: Python syntax"
if python -m py_compile "$CLI_FILE" 2>/dev/null; then
    echo -e "${GREEN}✓ No syntax errors${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Syntax errors detected${NC}"
    ((TESTS_FAILED++))
fi

# Test: Type checking with mypy (if available)
echo "Test: Type checking"
if command -v mypy &> /dev/null; then
    if mypy "$CLI_FILE" --ignore-missing-imports 2>/dev/null; then
        echo -e "${GREEN}✓ Type checking passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠ Type checking warnings/errors${NC}"
        echo "  Run: mypy $CLI_FILE --ignore-missing-imports"
    fi
else
    echo -e "${YELLOW}⚠ mypy not installed (skipping type check)${NC}"
fi

# Test: Linting with ruff (if available)
echo "Test: Code linting"
if command -v ruff &> /dev/null; then
    if ruff check "$CLI_FILE" --select E,W,F 2>/dev/null; then
        echo -e "${GREEN}✓ Linting passed${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠ Linting warnings/errors${NC}"
        echo "  Run: ruff check $CLI_FILE"
    fi
else
    echo -e "${YELLOW}⚠ ruff not installed (skipping linting)${NC}"
fi

# Test: Import check
echo "Test: Import dependencies"
if python -c "import sys; sys.path.insert(0, '.'); exec(open('$CLI_FILE').read().split('if __name__')[0])" 2>/dev/null; then
    echo -e "${GREEN}✓ All imports successful${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ Import errors detected${NC}"
    echo "  Check that all dependencies are installed"
    ((TESTS_FAILED++))
fi

# Test: Check for common patterns
echo "Test: Typer patterns"
PATTERN_ISSUES=0

if ! grep -q "@app.command()" "$CLI_FILE"; then
    echo -e "${YELLOW}  ⚠ No @app.command() decorators found${NC}"
    ((PATTERN_ISSUES++))
fi

if ! grep -q "typer.Typer()" "$CLI_FILE"; then
    echo -e "${YELLOW}  ⚠ No Typer() instance found${NC}"
    ((PATTERN_ISSUES++))
fi

if ! grep -q "if __name__ == \"__main__\":" "$CLI_FILE"; then
    echo -e "${YELLOW}  ⚠ Missing if __name__ == '__main__' guard${NC}"
    ((PATTERN_ISSUES++))
fi

if [ $PATTERN_ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ Common patterns found${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}⚠ Some patterns missing${NC}"
fi

echo "========================================"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
