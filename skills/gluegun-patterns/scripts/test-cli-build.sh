#!/bin/bash

# Test Gluegun CLI build process
# Usage: ./test-cli-build.sh <cli-directory>

set -e

CLI_DIR="${1:-.}"
ERRORS=0

echo "🧪 Testing Gluegun CLI build: $CLI_DIR"
echo ""

# Check if directory exists
if [ ! -d "$CLI_DIR" ]; then
    echo "❌ Directory not found: $CLI_DIR"
    exit 1
fi

cd "$CLI_DIR"

# Check for package.json
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi

echo "📦 Checking dependencies..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found, running npm install..."
    npm install
fi

# Check if gluegun is installed
if [ -d "node_modules/gluegun" ]; then
    echo "  ✅ gluegun installed"
else
    echo "  ❌ gluegun not installed"
    ((ERRORS++))
fi

# Check for TypeScript
if [ -f "tsconfig.json" ]; then
    echo ""
    echo "🔨 TypeScript detected, checking compilation..."

    if npm run build > /dev/null 2>&1; then
        echo "  ✅ TypeScript compilation successful"
    else
        echo "  ❌ TypeScript compilation failed"
        echo "     Run 'npm run build' for details"
        ((ERRORS++))
    fi
fi

# Check for tests
echo ""
echo "🧪 Checking for tests..."

if [ -d "test" ] || [ -d "tests" ] || [ -d "__tests__" ]; then
    echo "  ✅ Test directory found"

    # Try to run tests
    if npm test > /dev/null 2>&1; then
        echo "  ✅ Tests passed"
    else
        echo "  ⚠️  Tests failed or not configured"
    fi
else
    echo "  ⚠️  No test directory found"
fi

# Check CLI execution
echo ""
echo "🚀 Testing CLI execution..."

# Get CLI entry point
cli_entry=""
if [ -f "bin/cli" ]; then
    cli_entry="bin/cli"
elif [ -f "bin/run" ]; then
    cli_entry="bin/run"
elif [ -f "dist/cli.js" ]; then
    cli_entry="node dist/cli.js"
fi

if [ -n "$cli_entry" ]; then
    echo "  Found CLI entry: $cli_entry"

    # Test help command
    if $cli_entry --help > /dev/null 2>&1; then
        echo "  ✅ CLI --help works"
    else
        echo "  ⚠️  CLI --help failed"
        ((ERRORS++))
    fi

    # Test version command
    if $cli_entry --version > /dev/null 2>&1; then
        echo "  ✅ CLI --version works"
    else
        echo "  ⚠️  CLI --version failed"
    fi
else
    echo "  ⚠️  CLI entry point not found"
fi

# Summary
echo ""
echo "================================"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All build tests passed!"
    exit 0
else
    echo "❌ Found $ERRORS error(s) during build test"
    exit 1
fi
