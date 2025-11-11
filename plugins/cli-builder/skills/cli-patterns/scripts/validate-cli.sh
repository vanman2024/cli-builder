#!/bin/bash
# Validate CLI structure and best practices

set -euo pipefail

PROJECT_PATH="${1:-.}"

echo "🔍 Validating CLI project: $PROJECT_PATH"

cd "$PROJECT_PATH"

ERRORS=0

# Check if main.go exists
if [ ! -f "main.go" ]; then
    echo "❌ main.go not found"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ main.go exists"
fi

# Check if go.mod exists
if [ ! -f "go.mod" ]; then
    echo "❌ go.mod not found (run 'go mod init')"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ go.mod exists"
fi

# Check for urfave/cli dependency
if grep -q "github.com/urfave/cli/v2" go.mod 2>/dev/null; then
    echo "✅ urfave/cli dependency found"
else
    echo "⚠️  urfave/cli dependency not found"
fi

# Check for App definition
if grep -q "cli.App" main.go 2>/dev/null; then
    echo "✅ cli.App definition found"
else
    echo "❌ cli.App definition not found"
    ERRORS=$((ERRORS + 1))
fi

# Check for Usage field
if grep -q "Usage:" main.go 2>/dev/null; then
    echo "✅ Usage field defined"
else
    echo "⚠️  Usage field not found (recommended)"
fi

# Check for Version field
if grep -q "Version:" main.go 2>/dev/null; then
    echo "✅ Version field defined"
else
    echo "⚠️  Version field not found (recommended)"
fi

# Check if commands have descriptions
if grep -A 5 "Commands:" main.go 2>/dev/null | grep -q "Usage:"; then
    echo "✅ Commands have usage descriptions"
else
    echo "⚠️  Some commands might be missing usage descriptions"
fi

# Check for proper error handling
if grep -q "if err := app.Run" main.go 2>/dev/null; then
    echo "✅ Proper error handling in main"
else
    echo "❌ Missing error handling for app.Run"
    ERRORS=$((ERRORS + 1))
fi

# Try to build
echo ""
echo "🔨 Attempting build..."
if go build -o /tmp/test_build . 2>&1; then
    echo "✅ Build successful"
    rm -f /tmp/test_build
else
    echo "❌ Build failed"
    ERRORS=$((ERRORS + 1))
fi

# Run go vet
echo ""
echo "🔍 Running go vet..."
if go vet ./... 2>&1; then
    echo "✅ go vet passed"
else
    echo "⚠️  go vet found issues"
fi

# Summary
echo ""
echo "================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ Validation passed! No critical errors found."
    exit 0
else
    echo "❌ Validation failed with $ERRORS critical error(s)"
    exit 1
fi
