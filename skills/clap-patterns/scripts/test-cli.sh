#!/usr/bin/env bash
# Test a Clap CLI application with various argument combinations
#
# Usage: ./test-cli.sh <binary-path> [test-suite]
#
# Test suites: basic, subcommands, validation, env, all (default)

set -euo pipefail

BINARY="${1:-}"
TEST_SUITE="${2:-all}"

if [ -z "$BINARY" ]; then
    echo "Error: Binary path required"
    echo "Usage: $0 <binary-path> [test-suite]"
    echo ""
    echo "Test suites:"
    echo "  basic       - Test help, version, basic flags"
    echo "  subcommands - Test subcommand routing"
    echo "  validation  - Test input validation"
    echo "  env         - Test environment variables"
    echo "  all         - Run all tests (default)"
    exit 1
fi

if [ ! -x "$BINARY" ]; then
    echo "Error: Binary not found or not executable: $BINARY"
    exit 1
fi

PASS=0
FAIL=0

run_test() {
    local name="$1"
    local expected_exit="$2"
    shift 2

    echo -n "Testing: $name ... "

    if "$BINARY" "$@" &>/dev/null; then
        actual_exit=0
    else
        actual_exit=$?
    fi

    if [ "$actual_exit" -eq "$expected_exit" ]; then
        echo "✓ PASS"
        ((PASS++))
    else
        echo "❌ FAIL (expected exit $expected_exit, got $actual_exit)"
        ((FAIL++))
    fi
}

test_basic() {
    echo ""
    echo "=== Basic Tests ==="

    run_test "Help output" 0 --help
    run_test "Version output" 0 --version
    run_test "Short help" 0 -h
    run_test "Invalid flag" 1 --invalid-flag
    run_test "No arguments (might fail for some CLIs)" 0
}

test_subcommands() {
    echo ""
    echo "=== Subcommand Tests ==="

    run_test "Subcommand help" 0 help
    run_test "Invalid subcommand" 1 invalid-command

    # Try common subcommands
    for cmd in init add build test deploy; do
        if "$BINARY" help 2>&1 | grep -q "$cmd"; then
            run_test "Subcommand '$cmd' help" 0 "$cmd" --help
        fi
    done
}

test_validation() {
    echo ""
    echo "=== Validation Tests ==="

    # Test file arguments with non-existent files
    run_test "Non-existent file" 1 --input /nonexistent/file.txt

    # Test numeric ranges
    run_test "Invalid number" 1 --count abc
    run_test "Negative number" 1 --count -5

    # Test conflicting flags
    if "$BINARY" --help 2>&1 | grep -q "conflicts with"; then
        echo "  (Found conflicting arguments in help text)"
    fi
}

test_env() {
    echo ""
    echo "=== Environment Variable Tests ==="

    # Check if binary supports environment variables
    if "$BINARY" --help 2>&1 | grep -q "\[env:"; then
        echo "✓ Environment variable support detected"

        # Extract env vars from help text
        ENV_VARS=$("$BINARY" --help 2>&1 | grep -o '\[env: [A-Z_]*\]' | sed 's/\[env: \(.*\)\]/\1/' || true)

        if [ -n "$ENV_VARS" ]; then
            echo "Found environment variables:"
            echo "$ENV_VARS" | while read -r var; do
                echo "  - $var"
            done
        fi
    else
        echo "  No environment variable support detected"
    fi
}

# Run requested test suite
case "$TEST_SUITE" in
    basic)
        test_basic
        ;;
    subcommands)
        test_subcommands
        ;;
    validation)
        test_validation
        ;;
    env)
        test_env
        ;;
    all)
        test_basic
        test_subcommands
        test_validation
        test_env
        ;;
    *)
        echo "Error: Unknown test suite: $TEST_SUITE"
        exit 1
        ;;
esac

echo ""
echo "=== Test Summary ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "❌ Some tests failed"
    exit 1
else
    echo "✓ All tests passed!"
    exit 0
fi
