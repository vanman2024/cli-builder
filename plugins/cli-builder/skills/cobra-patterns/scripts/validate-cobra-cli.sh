#!/bin/bash

# Validate Cobra CLI structure and patterns
# Usage: ./validate-cobra-cli.sh <cli-directory>

set -euo pipefail

CLI_DIR="${1:-.}"

if [ ! -d "$CLI_DIR" ]; then
    echo "Error: Directory not found: $CLI_DIR"
    exit 1
fi

echo "Validating Cobra CLI structure in: $CLI_DIR"
echo ""

ERRORS=0
WARNINGS=0

# Check Go module
if [ ! -f "$CLI_DIR/go.mod" ]; then
    echo "❌ ERROR: go.mod not found"
    ((ERRORS++))
else
    echo "✓ go.mod found"
fi

# Check main.go
if [ ! -f "$CLI_DIR/main.go" ]; then
    echo "❌ ERROR: main.go not found"
    ((ERRORS++))
else
    echo "✓ main.go found"

    # Check if main.go has proper structure
    if ! grep -q "func main()" "$CLI_DIR/main.go"; then
        echo "❌ ERROR: main() function not found in main.go"
        ((ERRORS++))
    fi
fi

# Check cmd directory
if [ ! -d "$CLI_DIR/cmd" ]; then
    echo "⚠ WARNING: cmd/ directory not found (acceptable for simple CLIs)"
    ((WARNINGS++))
else
    echo "✓ cmd/ directory found"

    # Check root command
    if [ -f "$CLI_DIR/cmd/root.go" ]; then
        echo "✓ cmd/root.go found"

        # Validate root command structure
        if ! grep -q "var rootCmd" "$CLI_DIR/cmd/root.go"; then
            echo "❌ ERROR: rootCmd variable not found in root.go"
            ((ERRORS++))
        fi

        if ! grep -q "func Execute()" "$CLI_DIR/cmd/root.go"; then
            echo "❌ ERROR: Execute() function not found in root.go"
            ((ERRORS++))
        fi
    else
        echo "⚠ WARNING: cmd/root.go not found"
        ((WARNINGS++))
    fi
fi

# Check for Cobra dependency
if [ -f "$CLI_DIR/go.mod" ]; then
    if ! grep -q "github.com/spf13/cobra" "$CLI_DIR/go.mod"; then
        echo "❌ ERROR: Cobra dependency not found in go.mod"
        ((ERRORS++))
    else
        echo "✓ Cobra dependency found"
    fi
fi

# Validate command files have proper structure
if [ -d "$CLI_DIR/cmd" ]; then
    for cmd_file in "$CLI_DIR/cmd"/*.go; do
        if [ -f "$cmd_file" ]; then
            filename=$(basename "$cmd_file")

            # Check for command variable
            if grep -q "var.*Cmd = &cobra.Command" "$cmd_file"; then
                echo "✓ Command structure found in $filename"

                # Check for Use field
                if ! grep -A5 "var.*Cmd = &cobra.Command" "$cmd_file" | grep -q "Use:"; then
                    echo "⚠ WARNING: Use field missing in $filename"
                    ((WARNINGS++))
                fi

                # Check for Short description
                if ! grep -A10 "var.*Cmd = &cobra.Command" "$cmd_file" | grep -q "Short:"; then
                    echo "⚠ WARNING: Short description missing in $filename"
                    ((WARNINGS++))
                fi

                # Check for Run or RunE
                if ! grep -A15 "var.*Cmd = &cobra.Command" "$cmd_file" | grep -qE "Run:|RunE:"; then
                    echo "⚠ WARNING: Run/RunE function missing in $filename"
                    ((WARNINGS++))
                fi

                # Prefer RunE over Run for error handling
                if grep -A15 "var.*Cmd = &cobra.Command" "$cmd_file" | grep -q "Run:" && \
                   ! grep -A15 "var.*Cmd = &cobra.Command" "$cmd_file" | grep -q "RunE:"; then
                    echo "⚠ WARNING: Consider using RunE instead of Run in $filename for better error handling"
                    ((WARNINGS++))
                fi
            fi
        fi
    done
fi

# Check for .gitignore
if [ ! -f "$CLI_DIR/.gitignore" ]; then
    echo "⚠ WARNING: .gitignore not found"
    ((WARNINGS++))
else
    echo "✓ .gitignore found"
fi

# Check for README
if [ ! -f "$CLI_DIR/README.md" ]; then
    echo "⚠ WARNING: README.md not found"
    ((WARNINGS++))
else
    echo "✓ README.md found"
fi

# Check if Go code compiles
echo ""
echo "Checking if code compiles..."
cd "$CLI_DIR"
if go build -o /tmp/cobra-cli-test 2>&1 | head -20; then
    echo "✓ Code compiles successfully"
    rm -f /tmp/cobra-cli-test
else
    echo "❌ ERROR: Code does not compile"
    ((ERRORS++))
fi

# Check for common anti-patterns
echo ""
echo "Checking for anti-patterns..."

# Check for os.Exit in command handlers
if grep -r "os.Exit" "$CLI_DIR/cmd" 2>/dev/null | grep -v "import" | grep -v "//"; then
    echo "⚠ WARNING: Found os.Exit() in command handlers - prefer returning errors"
    ((WARNINGS++))
fi

# Check for panic in command handlers
if grep -r "panic(" "$CLI_DIR/cmd" 2>/dev/null | grep -v "import" | grep -v "//"; then
    echo "⚠ WARNING: Found panic() in command handlers - prefer returning errors"
    ((WARNINGS++))
fi

# Summary
echo ""
echo "================================"
echo "Validation Summary"
echo "================================"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✓ Validation passed!"
    if [ $WARNINGS -gt 0 ]; then
        echo "  ($WARNINGS warnings to review)"
    fi
    exit 0
else
    echo "❌ Validation failed with $ERRORS errors"
    exit 1
fi
