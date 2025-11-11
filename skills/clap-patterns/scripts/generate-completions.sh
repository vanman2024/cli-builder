#!/usr/bin/env bash
# Generate shell completions for Clap CLI applications
#
# Usage: ./generate-completions.sh <binary-name> [output-dir]
#
# This script generates shell completion scripts for bash, zsh, fish, and powershell.
# The CLI binary must support the --generate-completions flag (built with Clap).

set -euo pipefail

BINARY="${1:-}"
OUTPUT_DIR="${2:-completions}"

if [ -z "$BINARY" ]; then
    echo "Error: Binary name required"
    echo "Usage: $0 <binary-name> [output-dir]"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Generating shell completions for: $BINARY"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Check if binary exists
if ! command -v "$BINARY" &> /dev/null; then
    echo "Warning: Binary '$BINARY' not found in PATH"
    echo "Make sure to build and install it first: cargo install --path ."
    exit 1
fi

# Generate completions for each shell
for shell in bash zsh fish powershell elvish; do
    echo "Generating $shell completions..."

    case "$shell" in
        bash)
            "$BINARY" --generate-completion "$shell" > "$OUTPUT_DIR/${BINARY}.bash" 2>/dev/null || {
                echo "  ⚠️  Failed (CLI may not support --generate-completion)"
                continue
            }
            echo "  ✓ Generated: $OUTPUT_DIR/${BINARY}.bash"
            ;;
        zsh)
            "$BINARY" --generate-completion "$shell" > "$OUTPUT_DIR/_${BINARY}" 2>/dev/null || {
                echo "  ⚠️  Failed"
                continue
            }
            echo "  ✓ Generated: $OUTPUT_DIR/_${BINARY}"
            ;;
        fish)
            "$BINARY" --generate-completion "$shell" > "$OUTPUT_DIR/${BINARY}.fish" 2>/dev/null || {
                echo "  ⚠️  Failed"
                continue
            }
            echo "  ✓ Generated: $OUTPUT_DIR/${BINARY}.fish"
            ;;
        powershell)
            "$BINARY" --generate-completion "$shell" > "$OUTPUT_DIR/_${BINARY}.ps1" 2>/dev/null || {
                echo "  ⚠️  Failed"
                continue
            }
            echo "  ✓ Generated: $OUTPUT_DIR/_${BINARY}.ps1"
            ;;
        elvish)
            "$BINARY" --generate-completion "$shell" > "$OUTPUT_DIR/${BINARY}.elv" 2>/dev/null || {
                echo "  ⚠️  Failed"
                continue
            }
            echo "  ✓ Generated: $OUTPUT_DIR/${BINARY}.elv"
            ;;
    esac
done

echo ""
echo "✓ Completion generation complete!"
echo ""
echo "Installation instructions:"
echo ""
echo "Bash:"
echo "  sudo cp $OUTPUT_DIR/${BINARY}.bash /etc/bash_completion.d/"
echo "  Or: echo 'source $PWD/$OUTPUT_DIR/${BINARY}.bash' >> ~/.bashrc"
echo ""
echo "Zsh:"
echo "  cp $OUTPUT_DIR/_${BINARY} /usr/local/share/zsh/site-functions/"
echo "  Or add to fpath: fpath=($PWD/$OUTPUT_DIR \$fpath)"
echo ""
echo "Fish:"
echo "  cp $OUTPUT_DIR/${BINARY}.fish ~/.config/fish/completions/"
echo ""
echo "PowerShell:"
echo "  Add to profile: . $PWD/$OUTPUT_DIR/_${BINARY}.ps1"
