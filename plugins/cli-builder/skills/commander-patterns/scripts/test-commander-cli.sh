#!/bin/bash
# Test Commander.js CLI with various inputs

set -euo pipefail

CLI_COMMAND="${1:?Usage: $0 <cli-command> [test-suite]}"
TEST_SUITE="${2:-basic}"

echo "🧪 Testing Commander.js CLI: $CLI_COMMAND"
echo "Test suite: $TEST_SUITE"
echo ""

PASSED=0
FAILED=0

# Helper function to run test
run_test() {
  local test_name="$1"
  local test_command="$2"
  local expected_exit_code="${3:-0}"

  echo -n "Testing: $test_name ... "

  if eval "$test_command" > /dev/null 2>&1; then
    actual_exit_code=0
  else
    actual_exit_code=$?
  fi

  if [[ $actual_exit_code -eq $expected_exit_code ]]; then
    echo "✅ PASS"
    ((PASSED++))
  else
    echo "❌ FAIL (expected exit code $expected_exit_code, got $actual_exit_code)"
    ((FAILED++))
  fi
}

# Basic tests
if [[ "$TEST_SUITE" == "basic" || "$TEST_SUITE" == "all" ]]; then
  echo "Running basic tests..."
  run_test "Help flag" "$CLI_COMMAND --help" 0
  run_test "Version flag" "$CLI_COMMAND --version" 0
  run_test "No arguments" "$CLI_COMMAND" 1
fi

# Command tests
if [[ "$TEST_SUITE" == "commands" || "$TEST_SUITE" == "all" ]]; then
  echo ""
  echo "Running command tests..."
  run_test "List commands" "$CLI_COMMAND --help | grep -q 'Commands:'" 0
fi

# Option tests
if [[ "$TEST_SUITE" == "options" || "$TEST_SUITE" == "all" ]]; then
  echo ""
  echo "Running option tests..."
  run_test "Unknown option" "$CLI_COMMAND --unknown-option" 1
  run_test "Short flag" "$CLI_COMMAND -v" 0
  run_test "Long flag" "$CLI_COMMAND --verbose" 0
fi

# Argument tests
if [[ "$TEST_SUITE" == "arguments" || "$TEST_SUITE" == "all" ]]; then
  echo ""
  echo "Running argument tests..."
  run_test "Required argument missing" "$CLI_COMMAND deploy" 1
  run_test "Required argument provided" "$CLI_COMMAND deploy production" 0
fi

echo ""
echo "Test Results:"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo ""

if [[ $FAILED -gt 0 ]]; then
  echo "❌ Some tests failed"
  exit 1
else
  echo "✅ All tests passed!"
  exit 0
fi
