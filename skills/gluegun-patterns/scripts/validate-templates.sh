#!/bin/bash

# Validate EJS template syntax
# Usage: ./validate-templates.sh <templates-directory>

set -e

TEMPLATES_DIR="${1:-templates}"
ERRORS=0
WARNINGS=0

echo "🔍 Validating EJS templates: $TEMPLATES_DIR"
echo ""

# Check if directory exists
if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "❌ Directory not found: $TEMPLATES_DIR"
    exit 1
fi

# Find all template files
template_files=$(find "$TEMPLATES_DIR" -type f \( -name "*.ejs" -o -name "*.ejs.t" \))

if [ -z "$template_files" ]; then
    echo "⚠️  No template files found in $TEMPLATES_DIR"
    exit 0
fi

echo "Found $(echo "$template_files" | wc -l) template file(s)"
echo ""

# Validate each template
while IFS= read -r file; do
    echo "📄 Validating: $file"

    # Check for balanced EJS tags
    open_tags=$(grep -o "<%[^>]*" "$file" | wc -l || echo "0")
    close_tags=$(grep -o "%>" "$file" | wc -l || echo "0")

    if [ "$open_tags" -eq "$close_tags" ]; then
        echo "  ✅ Balanced EJS tags ($open_tags opening, $close_tags closing)"
    else
        echo "  ❌ Unbalanced EJS tags ($open_tags opening, $close_tags closing)"
        ((ERRORS++))
    fi

    # Check for common EJS patterns
    if grep -q "<%=" "$file" || grep -q "<%_" "$file" || grep -q "<%#" "$file"; then
        echo "  ✅ Contains EJS output tags"
    else
        echo "  ⚠️  No EJS output tags detected (might be plain template)"
        ((WARNINGS++))
    fi

    # Check for control flow
    if grep -q "<%\s*if" "$file" || grep -q "<%\s*for" "$file"; then
        echo "  ✅ Uses control flow"
    fi

    # Check for variable usage
    if grep -q "<%= [a-zA-Z]" "$file"; then
        echo "  ✅ Uses template variables"
    else
        echo "  ⚠️  No template variables found"
        ((WARNINGS++))
    fi

    # Validate basic syntax (check for common errors)
    if grep -q "<%\s*%>" "$file"; then
        echo "  ⚠️  Empty EJS tag detected"
        ((WARNINGS++))
    fi

    # Check for unclosed quotes in EJS tags
    if grep -P '<%[^%]*"[^"]*%>' "$file" | grep -v '<%[^%]*"[^"]*"[^%]*%>' > /dev/null 2>&1; then
        echo "  ⚠️  Possible unclosed quotes in EJS tags"
        ((WARNINGS++))
    fi

    echo ""

done <<< "$template_files"

# Summary
echo "================================"
echo "Templates validated: $(echo "$template_files" | wc -l)"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ All critical checks passed!"
    if [ $WARNINGS -gt 0 ]; then
        echo "⚠️  Consider reviewing $WARNINGS warning(s)"
    fi
    exit 0
else
    echo "❌ Found $ERRORS error(s)"
    exit 1
fi
