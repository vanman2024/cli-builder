#!/bin/bash
# Validate Commander.js CLI structure and patterns

set -euo pipefail

CLI_FILE="${1:?Usage: $0 <cli-file.ts|js>}"

if [[ ! -f "$CLI_FILE" ]]; then
  echo "Error: File not found: $CLI_FILE"
  exit 1
fi

echo "🔍 Validating Commander.js CLI structure: $CLI_FILE"
echo ""

ERRORS=0
WARNINGS=0

# Check for Commander import
if grep -q "from 'commander'" "$CLI_FILE" || grep -q 'require("commander")' "$CLI_FILE"; then
  echo "✅ Commander.js import found"
else
  echo "❌ Missing Commander.js import"
  ((ERRORS++))
fi

# Check for Command instantiation
if grep -q "new Command()" "$CLI_FILE" || grep -q "= program" "$CLI_FILE"; then
  echo "✅ Command instance created"
else
  echo "❌ No Command instance found"
  ((ERRORS++))
fi

# Check for program.parse()
if grep -q "\.parse()" "$CLI_FILE"; then
  echo "✅ program.parse() called"
else
  echo "❌ Missing program.parse() call"
  ((ERRORS++))
fi

# Check for .name()
if grep -q "\.name(" "$CLI_FILE"; then
  echo "✅ CLI name defined"
else
  echo "⚠️  CLI name not set (recommended)"
  ((WARNINGS++))
fi

# Check for .description()
if grep -q "\.description(" "$CLI_FILE"; then
  echo "✅ CLI description defined"
else
  echo "⚠️  CLI description not set (recommended)"
  ((WARNINGS++))
fi

# Check for .version()
if grep -q "\.version(" "$CLI_FILE"; then
  echo "✅ CLI version defined"
else
  echo "⚠️  CLI version not set (recommended)"
  ((WARNINGS++))
fi

# Check for commands
COMMAND_COUNT=$(grep -c "\.command(" "$CLI_FILE" || echo "0")
if [[ $COMMAND_COUNT -gt 0 ]]; then
  echo "✅ Found $COMMAND_COUNT command(s)"
else
  echo "⚠️  No commands defined"
  ((WARNINGS++))
fi

# Check for action handlers
ACTION_COUNT=$(grep -c "\.action(" "$CLI_FILE" || echo "0")
if [[ $ACTION_COUNT -gt 0 ]]; then
  echo "✅ Found $ACTION_COUNT action handler(s)"
else
  echo "⚠️  No action handlers defined"
  ((WARNINGS++))
fi

# Check for options
OPTION_COUNT=$(grep -c "\.option(" "$CLI_FILE" || echo "0")
ADDOPTION_COUNT=$(grep -c "\.addOption(" "$CLI_FILE" || echo "0")
TOTAL_OPTIONS=$((OPTION_COUNT + ADDOPTION_COUNT))
if [[ $TOTAL_OPTIONS -gt 0 ]]; then
  echo "✅ Found $TOTAL_OPTIONS option(s)"
else
  echo "⚠️  No options defined"
  ((WARNINGS++))
fi

# Check for arguments
ARGUMENT_COUNT=$(grep -c "\.argument(" "$CLI_FILE" || echo "0")
if [[ $ARGUMENT_COUNT -gt 0 ]]; then
  echo "✅ Found $ARGUMENT_COUNT argument(s)"
fi

# Check for Option class usage
if grep -q "new Option(" "$CLI_FILE"; then
  echo "✅ Option class used (advanced)"
fi

# Check for error handling
if grep -q "try\|catch" "$CLI_FILE" || grep -q "\.exitOverride()" "$CLI_FILE"; then
  echo "✅ Error handling present"
else
  echo "⚠️  No error handling detected (recommended)"
  ((WARNINGS++))
fi

# Check for TypeScript
if [[ "$CLI_FILE" == *.ts ]]; then
  echo "✅ TypeScript file"
  # Check for types
  if grep -q "import.*Command.*Option.*from 'commander'" "$CLI_FILE"; then
    echo "✅ Proper TypeScript imports"
  fi
fi

echo ""
echo "Summary:"
echo "  Errors: $ERRORS"
echo "  Warnings: $WARNINGS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
  echo "❌ Validation failed with $ERRORS error(s)"
  exit 1
elif [[ $WARNINGS -gt 0 ]]; then
  echo "⚠️  Validation passed with $WARNINGS warning(s)"
  exit 0
else
  echo "✅ Validation passed - excellent CLI structure!"
  exit 0
fi
