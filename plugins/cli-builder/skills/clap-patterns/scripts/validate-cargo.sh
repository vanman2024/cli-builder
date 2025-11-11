#!/usr/bin/env bash
# Validate Cargo.toml for correct Clap configuration
#
# Usage: ./validate-cargo.sh [path-to-Cargo.toml]
#
# Checks:
# - Clap dependency exists
# - Clap version is 4.x or newer
# - Required features are enabled (derive)
# - Optional features (env, cargo) are present if needed

set -euo pipefail

CARGO_TOML="${1:-Cargo.toml}"

if [ ! -f "$CARGO_TOML" ]; then
    echo "❌ Error: $CARGO_TOML not found"
    exit 1
fi

echo "Validating Clap configuration in: $CARGO_TOML"
echo ""

# Check if clap is listed as a dependency
if ! grep -q "clap" "$CARGO_TOML"; then
    echo "❌ Clap not found in dependencies"
    echo ""
    echo "Add to $CARGO_TOML:"
    echo ""
    echo '[dependencies]'
    echo 'clap = { version = "4.5", features = ["derive"] }'
    exit 1
fi

echo "✓ Clap dependency found"

# Extract clap version
VERSION=$(grep -A 5 '^\[dependencies\]' "$CARGO_TOML" | grep 'clap' | head -1)

# Check version
if echo "$VERSION" | grep -q '"4\.' || echo "$VERSION" | grep -q "'4\."; then
    echo "✓ Clap version 4.x detected"
elif echo "$VERSION" | grep -q '"3\.' || echo "$VERSION" | grep -q "'3\."; then
    echo "⚠️  Warning: Clap version 3.x detected"
    echo "   Consider upgrading to 4.x for latest features"
else
    echo "⚠️  Warning: Could not determine Clap version"
fi

# Check for derive feature
if echo "$VERSION" | grep -q 'features.*derive' || echo "$VERSION" | grep -q 'derive.*features'; then
    echo "✓ 'derive' feature enabled"
else
    echo "❌ 'derive' feature not found"
    echo "   Add: features = [\"derive\"]"
    exit 1
fi

# Check for optional but recommended features
echo ""
echo "Optional features:"

if echo "$VERSION" | grep -q '"env"' || echo "$VERSION" | grep -q "'env'"; then
    echo "✓ 'env' feature enabled (environment variable support)"
else
    echo "  'env' feature not enabled"
    echo "  Add for environment variable support: features = [\"derive\", \"env\"]"
fi

if echo "$VERSION" | grep -q '"cargo"' || echo "$VERSION" | grep -q "'cargo'"; then
    echo "✓ 'cargo' feature enabled (automatic version from Cargo.toml)"
else
    echo "  'cargo' feature not enabled"
    echo "  Add for automatic version: features = [\"derive\", \"cargo\"]"
fi

if echo "$VERSION" | grep -q '"color"' || echo "$VERSION" | grep -q "'color'"; then
    echo "✓ 'color' feature enabled (colored output)"
else
    echo "  'color' feature not enabled"
    echo "  Add for colored help: features = [\"derive\", \"color\"]"
fi

echo ""

# Check for common patterns in src/
if [ -d "src" ]; then
    echo "Checking source files for Clap usage patterns..."

    if grep -r "use clap::Parser" src/ &>/dev/null; then
        echo "✓ Parser trait usage found"
    fi

    if grep -r "use clap::Subcommand" src/ &>/dev/null; then
        echo "✓ Subcommand trait usage found"
    fi

    if grep -r "use clap::ValueEnum" src/ &>/dev/null; then
        echo "✓ ValueEnum trait usage found"
    fi

    if grep -r "#\[derive(Parser)\]" src/ &>/dev/null; then
        echo "✓ Parser derive macro usage found"
    fi
fi

echo ""
echo "✓ Validation complete!"
echo ""
echo "Recommended Cargo.toml configuration:"
echo ""
echo '[dependencies]'
echo 'clap = { version = "4.5", features = ["derive", "env", "cargo"] }'
