#!/usr/bin/env bash
# Generate bash/zsh completion script for yargs-based CLI

set -euo pipefail

CLI_NAME="${1:-mycli}"
OUTPUT_FILE="${2:-${CLI_NAME}-completion.sh}"

cat > "$OUTPUT_FILE" <<EOF
#!/usr/bin/env bash
# Bash completion script for ${CLI_NAME}
# Source this file to enable completion: source ${OUTPUT_FILE}

_${CLI_NAME}_completions()
{
    local cur prev opts
    COMPREPLY=()
    cur="\${COMP_WORDS[COMP_CWORD]}"
    prev="\${COMP_WORDS[COMP_CWORD-1]}"

    # Get completion from yargs
    COMP_LINE=\$COMP_LINE COMP_POINT=\$COMP_POINT ${CLI_NAME} --get-yargs-completions "\${COMP_WORDS[@]:1}" 2>/dev/null | while read -r line; do
        COMPREPLY+=("\$line")
    done

    return 0
}

complete -F _${CLI_NAME}_completions ${CLI_NAME}
EOF

chmod +x "$OUTPUT_FILE"

echo "✅ Completion script generated: $OUTPUT_FILE"
echo ""
echo "To enable completion, add this to your ~/.bashrc or ~/.zshrc:"
echo "  source $(pwd)/$OUTPUT_FILE"
