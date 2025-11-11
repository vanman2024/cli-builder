#!/bin/bash
# Extract help text from Commander.js CLI for documentation

set -euo pipefail

CLI_COMMAND="${1:?Usage: $0 <cli-command> [output-file]}"
OUTPUT_FILE="${2:-docs/CLI-REFERENCE.md}"

echo "📚 Extracting help documentation from: $CLI_COMMAND"

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Start markdown file
cat > "$OUTPUT_FILE" << EOF
# CLI Reference

Auto-generated documentation for $CLI_COMMAND

---

## Main Command

\`\`\`
EOF

# Get main help
$CLI_COMMAND --help >> "$OUTPUT_FILE" || true

cat >> "$OUTPUT_FILE" << 'EOF'
```

---

## Commands

EOF

# Extract all commands
COMMANDS=$($CLI_COMMAND --help | grep -A 100 "Commands:" | tail -n +2 | awk '{print $1}' | grep -v "^$" || echo "")

if [[ -n "$COMMANDS" ]]; then
  for cmd in $COMMANDS; do
    echo "### \`$cmd\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "\`\`\`" >> "$OUTPUT_FILE"
    $CLI_COMMAND $cmd --help >> "$OUTPUT_FILE" 2>&1 || true
    echo "\`\`\`" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
  done
else
  echo "No subcommands found." >> "$OUTPUT_FILE"
fi

cat >> "$OUTPUT_FILE" << EOF

---

*Generated: $(date)*
*CLI Version: $($CLI_COMMAND --version 2>/dev/null || echo "unknown")*
EOF

echo "✅ Documentation generated: $OUTPUT_FILE"
echo ""
echo "Preview:"
head -n 20 "$OUTPUT_FILE"
echo "..."
