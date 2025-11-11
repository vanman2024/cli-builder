#!/bin/bash

# Validate Gluegun command files
# Usage: ./validate-commands.sh <commands-directory>

set -e

COMMANDS_DIR="${1:-src/commands}"
ERRORS=0
WARNINGS=0

echo "🔍 Validating Gluegun commands: $COMMANDS_DIR"
echo ""

# Check if directory exists
if [ ! -d "$COMMANDS_DIR" ]; then
    echo "❌ Directory not found: $COMMANDS_DIR"
    exit 1
fi

# Find all command files
command_files=$(find "$COMMANDS_DIR" -type f \( -name "*.ts" -o -name "*.js" \))

if [ -z "$command_files" ]; then
    echo "❌ No command files found in $COMMANDS_DIR"
    exit 1
fi

echo "Found $(echo "$command_files" | wc -l) command file(s)"
echo ""

# Validate each command file
while IFS= read -r file; do
    echo "📄 Validating: $file"

    # Check for required exports
    if grep -q "module.exports" "$file" || grep -q "export.*GluegunCommand" "$file"; then
        echo "  ✅ Has command export"
    else
        echo "  ❌ Missing command export"
        ((ERRORS++))
    fi

    # Check for name property
    if grep -q "name:" "$file"; then
        echo "  ✅ Has name property"
    else
        echo "  ❌ Missing name property"
        ((ERRORS++))
    fi

    # Check for run function
    if grep -q "run:" "$file" || grep -q "run =" "$file"; then
        echo "  ✅ Has run function"
    else
        echo "  ❌ Missing run function"
        ((ERRORS++))
    fi

    # Check for toolbox parameter
    if grep -q "toolbox" "$file"; then
        echo "  ✅ Uses toolbox"
    else
        echo "  ⚠️  No toolbox parameter (might be unused)"
        ((WARNINGS++))
    fi

    # Check for description (recommended)
    if grep -q "description:" "$file"; then
        echo "  ✅ Has description (good practice)"
    else
        echo "  ⚠️  Missing description (recommended)"
        ((WARNINGS++))
    fi

    # Check for async/await pattern
    if grep -q "async" "$file"; then
        echo "  ✅ Uses async/await"
    else
        echo "  ⚠️  No async/await detected"
    fi

    echo ""

done <<< "$command_files"

# Summary
echo "================================"
echo "Commands validated: $(echo "$command_files" | wc -l)"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ All critical checks passed!"
    if [ $WARNINGS -gt 0 ]; then
        echo "⚠️  Consider addressing $WARNINGS warning(s)"
    fi
    exit 0
else
    echo "❌ Found $ERRORS error(s)"
    exit 1
fi
