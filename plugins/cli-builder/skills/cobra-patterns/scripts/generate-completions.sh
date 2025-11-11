#!/bin/bash

# Generate shell completion scripts for Cobra CLI
# Usage: ./generate-completions.sh <cli-binary> [output-dir]

set -euo pipefail

CLI_BINARY="${1:-}"
OUTPUT_DIR="${2:-./completions}"

if [ -z "$CLI_BINARY" ]; then
    echo "Error: CLI binary path required"
    echo "Usage: $0 <cli-binary> [output-dir]"
    exit 1
fi

if [ ! -f "$CLI_BINARY" ]; then
    echo "Error: Binary not found: $CLI_BINARY"
    exit 1
fi

if [ ! -x "$CLI_BINARY" ]; then
    echo "Error: Binary is not executable: $CLI_BINARY"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

CLI_NAME=$(basename "$CLI_BINARY")

echo "Generating shell completions for $CLI_NAME..."
echo ""

# Generate Bash completion
if "$CLI_BINARY" completion bash > "$OUTPUT_DIR/$CLI_NAME.bash" 2>/dev/null; then
    echo "✓ Bash completion: $OUTPUT_DIR/$CLI_NAME.bash"
    echo "  Install: source $OUTPUT_DIR/$CLI_NAME.bash"
else
    echo "⚠ Bash completion not available"
fi

# Generate Zsh completion
if "$CLI_BINARY" completion zsh > "$OUTPUT_DIR/_$CLI_NAME" 2>/dev/null; then
    echo "✓ Zsh completion: $OUTPUT_DIR/_$CLI_NAME"
    echo "  Install: Place in \$fpath directory"
else
    echo "⚠ Zsh completion not available"
fi

# Generate Fish completion
if "$CLI_BINARY" completion fish > "$OUTPUT_DIR/$CLI_NAME.fish" 2>/dev/null; then
    echo "✓ Fish completion: $OUTPUT_DIR/$CLI_NAME.fish"
    echo "  Install: source $OUTPUT_DIR/$CLI_NAME.fish"
else
    echo "⚠ Fish completion not available"
fi

# Generate PowerShell completion
if "$CLI_BINARY" completion powershell > "$OUTPUT_DIR/$CLI_NAME.ps1" 2>/dev/null; then
    echo "✓ PowerShell completion: $OUTPUT_DIR/$CLI_NAME.ps1"
    echo "  Install: & $OUTPUT_DIR/$CLI_NAME.ps1"
else
    echo "⚠ PowerShell completion not available"
fi

echo ""
echo "Completions generated in: $OUTPUT_DIR"
echo ""
echo "Installation instructions:"
echo ""
echo "Bash:"
echo "  echo 'source $OUTPUT_DIR/$CLI_NAME.bash' >> ~/.bashrc"
echo ""
echo "Zsh:"
echo "  mkdir -p ~/.zsh/completions"
echo "  cp $OUTPUT_DIR/_$CLI_NAME ~/.zsh/completions/"
echo "  Add to ~/.zshrc: fpath=(~/.zsh/completions \$fpath)"
echo ""
echo "Fish:"
echo "  mkdir -p ~/.config/fish/completions"
echo "  cp $OUTPUT_DIR/$CLI_NAME.fish ~/.config/fish/completions/"
echo ""
