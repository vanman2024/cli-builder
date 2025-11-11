#!/bin/bash

# Validate Gluegun CLI structure
# Usage: ./validate-cli-structure.sh <cli-directory>

set -e

CLI_DIR="${1:-.}"
ERRORS=0

echo "🔍 Validating Gluegun CLI structure: $CLI_DIR"
echo ""

# Check if directory exists
if [ ! -d "$CLI_DIR" ]; then
    echo "❌ Directory not found: $CLI_DIR"
    exit 1
fi

cd "$CLI_DIR"

# Check for required files
echo "📁 Checking required files..."

required_files=(
    "package.json"
    "tsconfig.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
        ((ERRORS++))
    fi
done

# Check for required directories
echo ""
echo "📂 Checking directory structure..."

required_dirs=(
    "src"
    "src/commands"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ Missing: $dir/"
        ((ERRORS++))
    fi
done

# Check optional but recommended directories
optional_dirs=(
    "src/extensions"
    "templates"
    "src/plugins"
)

echo ""
echo "📂 Checking optional directories..."

for dir in "${optional_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/ (optional)"
    else
        echo "  ⚠️  Missing: $dir/ (optional but recommended)"
    fi
done

# Check package.json for gluegun dependency
echo ""
echo "📦 Checking dependencies..."

if [ -f "package.json" ]; then
    if grep -q '"gluegun"' package.json; then
        echo "  ✅ gluegun dependency found"
    else
        echo "  ❌ gluegun dependency not found in package.json"
        ((ERRORS++))
    fi
fi

# Check for commands
echo ""
echo "🎯 Checking commands..."

if [ -d "src/commands" ]; then
    command_count=$(find src/commands -type f \( -name "*.ts" -o -name "*.js" \) | wc -l)
    echo "  Found $command_count command file(s)"

    if [ "$command_count" -eq 0 ]; then
        echo "  ⚠️  No command files found"
    fi
fi

# Check for CLI entry point
echo ""
echo "🚀 Checking CLI entry point..."

if [ -f "src/cli.ts" ] || [ -f "src/index.ts" ]; then
    echo "  ✅ Entry point found"
else
    echo "  ❌ No entry point found (src/cli.ts or src/index.ts)"
    ((ERRORS++))
fi

# Summary
echo ""
echo "================================"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed!"
    exit 0
else
    echo "❌ Found $ERRORS error(s)"
    exit 1
fi
