#!/bin/bash
# Add a new command to existing CLI

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <app-name> <command-name> [category]"
    echo "Example: $0 myapp backup Deploy"
    exit 1
fi

APP_NAME="$1"
COMMAND_NAME="$2"
CATEGORY="${3:-General}"

if [ ! -d "$APP_NAME" ]; then
    echo "Error: Directory $APP_NAME not found"
    exit 1
fi

cd "$APP_NAME"

# Create command implementation
FUNC_NAME="${COMMAND_NAME}Command"

cat >> commands.go <<EOF

func ${FUNC_NAME}(c *cli.Context) error {
    fmt.Println("Executing ${COMMAND_NAME} command...")
    // TODO: Implement ${COMMAND_NAME} logic
    return nil
}
EOF

# Generate command definition
cat > /tmp/new_command.txt <<EOF
            {
                Name:     "${COMMAND_NAME}",
                Category: "${CATEGORY}",
                Usage:    "TODO: Add usage description",
                Action:   ${FUNC_NAME},
            },
EOF

echo "✅ Command stub created!"
echo ""
echo "Next steps:"
echo "1. Add the following to your Commands slice in main.go:"
cat /tmp/new_command.txt
echo ""
echo "2. Implement the logic in commands.go:${FUNC_NAME}"
echo "3. Add flags if needed"
