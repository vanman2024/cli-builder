#!/bin/bash

# Add a new command to existing Cobra CLI
# Usage: ./add-command.sh <command-name> [--parent parent-command]

set -euo pipefail

COMMAND_NAME="${1:-}"
PARENT_CMD=""

# Parse arguments
shift || true
while [ $# -gt 0 ]; do
    case "$1" in
        --parent)
            PARENT_CMD="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$COMMAND_NAME" ]; then
    echo "Error: Command name required"
    echo "Usage: $0 <command-name> [--parent parent-command]"
    exit 1
fi

if [ ! -d "cmd" ]; then
    echo "Error: cmd/ directory not found. Run from CLI root directory."
    exit 1
fi

# Determine file location
if [ -n "$PARENT_CMD" ]; then
    CMD_DIR="cmd/$PARENT_CMD"
    mkdir -p "$CMD_DIR"
    CMD_FILE="$CMD_DIR/$COMMAND_NAME.go"
    PACKAGE_NAME="$PARENT_CMD"
else
    CMD_FILE="cmd/$COMMAND_NAME.go"
    PACKAGE_NAME="cmd"
fi

if [ -f "$CMD_FILE" ]; then
    echo "Error: Command file already exists: $CMD_FILE"
    exit 1
fi

# Create command file
cat > "$CMD_FILE" << EOF
package $PACKAGE_NAME

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    // Add command-specific flags here
    ${COMMAND_NAME}Example string
)

var ${COMMAND_NAME}Cmd = &cobra.Command{
    Use:   "$COMMAND_NAME",
    Short: "Short description of $COMMAND_NAME",
    Long: \`Detailed description of the $COMMAND_NAME command.

This command does something useful. Add more details here.

Examples:
  mycli $COMMAND_NAME --example value\`,
    RunE: func(cmd *cobra.Command, args []string) error {
        fmt.Printf("Executing $COMMAND_NAME command\n")

        // Add command logic here

        return nil
    },
}

func init() {
    // Define flags
    ${COMMAND_NAME}Cmd.Flags().StringVar(&${COMMAND_NAME}Example, "example", "", "example flag")

    // Register command
EOF

if [ -n "$PARENT_CMD" ]; then
    cat >> "$CMD_FILE" << EOF
    ${PARENT_CMD}Cmd.AddCommand(${COMMAND_NAME}Cmd)
EOF
else
    cat >> "$CMD_FILE" << EOF
    rootCmd.AddCommand(${COMMAND_NAME}Cmd)
EOF
fi

cat >> "$CMD_FILE" << EOF
}
EOF

echo "✓ Created command file: $CMD_FILE"
echo ""
echo "Next steps:"
echo "1. Update the command logic in $CMD_FILE"
echo "2. Add any required flags"
echo "3. Build and test: go build"
echo ""
