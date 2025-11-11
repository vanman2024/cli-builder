#!/bin/bash
# Validate typer-patterns skill structure

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

echo "Validating typer-patterns skill..."
echo "========================================"

# Check SKILL.md exists
echo "Checking SKILL.md..."
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo -e "${RED}✗ SKILL.md not found${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ SKILL.md exists${NC}"

    # Check frontmatter starts at line 1
    FIRST_LINE=$(head -n 1 "$SKILL_DIR/SKILL.md")
    if [ "$FIRST_LINE" != "---" ]; then
        echo -e "${RED}✗ SKILL.md frontmatter must start at line 1 (found: $FIRST_LINE)${NC}"
        ((ERRORS++))
    else
        echo -e "${GREEN}✓ Frontmatter starts at line 1${NC}"
    fi

    # Check required frontmatter fields
    if grep -q "^name: " "$SKILL_DIR/SKILL.md"; then
        echo -e "${GREEN}✓ name field present${NC}"
    else
        echo -e "${RED}✗ name field missing${NC}"
        ((ERRORS++))
    fi

    if grep -q "^description: " "$SKILL_DIR/SKILL.md"; then
        echo -e "${GREEN}✓ description field present${NC}"
    else
        echo -e "${RED}✗ description field missing${NC}"
        ((ERRORS++))
    fi

    # Check for "Use when" in description
    if grep "^description: " "$SKILL_DIR/SKILL.md" | grep -q "Use when"; then
        echo -e "${GREEN}✓ Description contains 'Use when' triggers${NC}"
    else
        echo -e "${YELLOW}⚠ Description should include 'Use when' trigger contexts${NC}"
    fi
fi

# Check templates directory
echo "Checking templates..."
TEMPLATE_COUNT=$(find "$SKILL_DIR/templates" -name "*.py" 2>/dev/null | wc -l)
if [ "$TEMPLATE_COUNT" -ge 4 ]; then
    echo -e "${GREEN}✓ Found $TEMPLATE_COUNT templates (minimum 4)${NC}"
else
    echo -e "${RED}✗ Found $TEMPLATE_COUNT templates (need at least 4)${NC}"
    ((ERRORS++))
fi

# Check scripts directory
echo "Checking scripts..."
SCRIPT_COUNT=$(find "$SKILL_DIR/scripts" -name "*.sh" 2>/dev/null | wc -l)
if [ "$SCRIPT_COUNT" -ge 3 ]; then
    echo -e "${GREEN}✓ Found $SCRIPT_COUNT scripts (minimum 3)${NC}"
else
    echo -e "${RED}✗ Found $SCRIPT_COUNT scripts (need at least 3)${NC}"
    ((ERRORS++))
fi

# Check scripts are executable
NONEXEC=$(find "$SKILL_DIR/scripts" -name "*.sh" ! -executable 2>/dev/null | wc -l)
if [ "$NONEXEC" -gt 0 ]; then
    echo -e "${YELLOW}⚠ $NONEXEC scripts are not executable${NC}"
else
    echo -e "${GREEN}✓ All scripts are executable${NC}"
fi

# Check examples directory
echo "Checking examples..."
EXAMPLE_COUNT=$(find "$SKILL_DIR/examples" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
if [ "$EXAMPLE_COUNT" -ge 3 ]; then
    echo -e "${GREEN}✓ Found $EXAMPLE_COUNT example directories (minimum 3)${NC}"
else
    echo -e "${RED}✗ Found $EXAMPLE_COUNT examples (need at least 3)${NC}"
    ((ERRORS++))
fi

# Check for README files in examples
for example_dir in "$SKILL_DIR/examples"/*; do
    if [ -d "$example_dir" ]; then
        example_name=$(basename "$example_dir")
        if [ -f "$example_dir/README.md" ]; then
            echo -e "${GREEN}✓ Example $example_name has README.md${NC}"
        else
            echo -e "${YELLOW}⚠ Example $example_name missing README.md${NC}"
        fi
    fi
done

# Check for hardcoded secrets (basic check)
echo "Checking for hardcoded secrets..."
if grep -r "sk-[a-zA-Z0-9]" "$SKILL_DIR" 2>/dev/null | grep -v "validate-skill.sh" | grep -q .; then
    echo -e "${RED}✗ Possible API keys detected${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✓ No obvious API keys detected${NC}"
fi

# Check SKILL.md length
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_DIR/SKILL.md")
    if [ "$LINE_COUNT" -gt 150 ]; then
        echo -e "${YELLOW}⚠ SKILL.md is $LINE_COUNT lines (consider keeping under 150)${NC}"
    else
        echo -e "${GREEN}✓ SKILL.md length is reasonable ($LINE_COUNT lines)${NC}"
    fi
fi

echo "========================================"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ Validation passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s)${NC}"
    exit 1
fi
