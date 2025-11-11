#!/bin/bash

# validate-prompts.sh
# Validate prompt templates and check for common issues

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0
WARNINGS=0

echo "🔍 Validating inquirer-patterns skill..."
echo

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ((ERRORS++))
}

warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
    ((WARNINGS++))
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check SKILL.md exists
echo "📄 Checking SKILL.md..."
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    error "SKILL.md not found"
else
    success "SKILL.md exists"

    # Check frontmatter starts at line 1
    FIRST_LINE=$(head -n 1 "$SKILL_DIR/SKILL.md")
    if [ "$FIRST_LINE" != "---" ]; then
        error "SKILL.md frontmatter must start at line 1"
    else
        success "Frontmatter starts at line 1"
    fi

    # Check for required frontmatter fields
    if ! grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
        error "Missing 'name' field in frontmatter"
    else
        success "Frontmatter has 'name' field"
    fi

    if ! grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
        error "Missing 'description' field in frontmatter"
    else
        success "Frontmatter has 'description' field"
    fi

    # Check for "Use when" context
    if ! grep -qi "use when" "$SKILL_DIR/SKILL.md"; then
        warning "Missing 'Use when' trigger context in description"
    else
        success "'Use when' context found"
    fi
fi

echo

# Check Node.js templates
echo "📁 Checking Node.js templates..."
NODEJS_DIR="$SKILL_DIR/templates/nodejs"

if [ ! -d "$NODEJS_DIR" ]; then
    error "Node.js templates directory not found"
else
    success "Node.js templates directory exists"

    REQUIRED_NODEJS_TEMPLATES=(
        "text-prompt.js"
        "list-prompt.js"
        "checkbox-prompt.js"
        "password-prompt.js"
        "autocomplete-prompt.js"
        "conditional-prompt.js"
        "comprehensive-example.js"
    )

    for template in "${REQUIRED_NODEJS_TEMPLATES[@]}"; do
        if [ ! -f "$NODEJS_DIR/$template" ]; then
            error "Missing Node.js template: $template"
        else
            # Check for basic syntax
            if ! grep -q "import inquirer from 'inquirer'" "$NODEJS_DIR/$template"; then
                if ! grep -q "inquirer" "$NODEJS_DIR/$template"; then
                    warning "$template might be missing inquirer import"
                fi
            fi
            success "Node.js template exists: $template"
        fi
    done
fi

echo

# Check Python templates
echo "📁 Checking Python templates..."
PYTHON_DIR="$SKILL_DIR/templates/python"

if [ ! -d "$PYTHON_DIR" ]; then
    error "Python templates directory not found"
else
    success "Python templates directory exists"

    REQUIRED_PYTHON_TEMPLATES=(
        "text_prompt.py"
        "list_prompt.py"
        "checkbox_prompt.py"
        "password_prompt.py"
        "autocomplete_prompt.py"
        "conditional_prompt.py"
    )

    for template in "${REQUIRED_PYTHON_TEMPLATES[@]}"; do
        if [ ! -f "$PYTHON_DIR/$template" ]; then
            error "Missing Python template: $template"
        else
            # Check for basic syntax
            if ! grep -q "import questionary" "$PYTHON_DIR/$template"; then
                warning "$template might be missing questionary import"
            fi
            success "Python template exists: $template"
        fi
    done
fi

echo

# Check scripts
echo "📁 Checking scripts..."
SCRIPTS_DIR="$SKILL_DIR/scripts"

REQUIRED_SCRIPTS=(
    "install-nodejs-deps.sh"
    "install-python-deps.sh"
    "validate-prompts.sh"
    "generate-prompt.sh"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ ! -f "$SCRIPTS_DIR/$script" ]; then
        error "Missing script: $script"
    else
        if [ ! -x "$SCRIPTS_DIR/$script" ]; then
            warning "Script not executable: $script"
        else
            success "Script exists and is executable: $script"
        fi
    fi
done

echo

# Check for hardcoded API keys or secrets (security check)
echo "🔒 Security check: Scanning for hardcoded secrets..."

# Patterns to search for
SECRET_PATTERNS=(
    "sk-[a-zA-Z0-9]{32,}"
    "pk-[a-zA-Z0-9]{32,}"
    "AIza[0-9A-Za-z_-]{35}"
    "password.*=.*['\"][^'\"]{8,}['\"]"
)

SECRETS_FOUND=0
for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -rE "$pattern" "$SKILL_DIR/templates" 2>/dev/null | grep -v "your_.*_key_here" | grep -v "example" > /dev/null; then
        error "Potential hardcoded secret found matching pattern: $pattern"
        ((SECRETS_FOUND++))
    fi
done

if [ $SECRETS_FOUND -eq 0 ]; then
    success "No hardcoded secrets found"
fi

echo

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "Validation Summary"
echo "═══════════════════════════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Validation passed with $WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${RED}❌ Validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    exit 1
fi
