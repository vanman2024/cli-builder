#!/usr/bin/env bash
# Test argparse parser with various argument combinations

set -euo pipefail

usage() {
    cat <<EOF
Test argparse parser with various arguments

Usage: $(basename "$0") PARSER_FILE

Tests:
    - Help display (--help)
    - Version display (--version)
    - Missing required arguments
    - Invalid choices
    - Type validation
    - Subcommands (if present)

Examples:
    $(basename "$0") mycli.py
    $(basename "$0") ../templates/basic-parser.py
EOF
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

PARSER_FILE="$1"

if [ ! -f "$PARSER_FILE" ]; then
    echo "Error: File not found: $PARSER_FILE"
    exit 1
fi

# Make executable if needed
if [ ! -x "$PARSER_FILE" ]; then
    chmod +x "$PARSER_FILE"
fi

echo "Testing argparse parser: $PARSER_FILE"
echo ""

PASSED=0
FAILED=0

run_test() {
    local description="$1"
    shift
    local expected_result="$1"
    shift

    echo -n "Testing: $description ... "

    if "$PARSER_FILE" "$@" >/dev/null 2>&1; then
        result="success"
    else
        result="failure"
    fi

    if [ "$result" = "$expected_result" ]; then
        echo "✓ PASS"
        ((PASSED++))
    else
        echo "✗ FAIL (expected $expected_result, got $result)"
        ((FAILED++))
    fi
}

# Test --help
run_test "Help display" "success" --help

# Test --version
if grep -q "action='version'" "$PARSER_FILE"; then
    run_test "Version display" "success" --version
fi

# Test with no arguments
run_test "No arguments" "failure"

# Test invalid option
run_test "Invalid option" "failure" --invalid-option

# Detect and test subcommands
if grep -q "add_subparsers(" "$PARSER_FILE"; then
    echo ""
    echo "Subcommands detected, testing subcommand patterns..."

    # Try to extract subcommand names
    subcommands=$(grep -oP "add_parser\('\K[^']+(?=')" "$PARSER_FILE" || true)

    if [ -n "$subcommands" ]; then
        for cmd in $subcommands; do
            run_test "Subcommand: $cmd --help" "success" "$cmd" --help
        done
    fi
fi

# Test choices if present
if grep -q "choices=\[" "$PARSER_FILE"; then
    echo ""
    echo "Choices validation detected, testing..."

    # Extract valid and invalid choices
    valid_choice=$(grep -oP "choices=\[\s*'([^']+)" "$PARSER_FILE" | head -n1 | grep -oP "'[^']+'" | tr -d "'" || echo "valid")
    invalid_choice="invalid_choice_12345"

    if grep -q "add_subparsers(" "$PARSER_FILE" && [ -n "$subcommands" ]; then
        first_cmd=$(echo "$subcommands" | head -n1)
        run_test "Valid choice" "success" "$first_cmd" target --env "$valid_choice" 2>/dev/null || true
        run_test "Invalid choice" "failure" "$first_cmd" target --env "$invalid_choice" 2>/dev/null || true
    fi
fi

# Test type validation if present
if grep -q "type=int" "$PARSER_FILE"; then
    echo ""
    echo "Type validation detected, testing..."

    run_test "Valid integer" "success" --port 8080 2>/dev/null || true
    run_test "Invalid integer" "failure" --port invalid 2>/dev/null || true
fi

# Test boolean flags if present
if grep -q "action='store_true'" "$PARSER_FILE"; then
    echo ""
    echo "Boolean flags detected, testing..."

    run_test "Boolean flag present" "success" --verbose 2>/dev/null || true
fi

# Summary
echo ""
echo "Test Summary:"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "  Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo "✓ All tests passed"
    exit 0
else
    echo ""
    echo "✗ Some tests failed"
    exit 1
fi
