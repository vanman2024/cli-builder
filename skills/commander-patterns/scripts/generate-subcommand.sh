#!/bin/bash
# Generate nested subcommand structure for Commander.js

set -euo pipefail

PARENT_COMMAND="${1:?Usage: $0 <parent-command> <subcommand> [output-file]}"
SUBCOMMAND="${2:?Usage: $0 <parent-command> <subcommand> [output-file]}"
OUTPUT_FILE="${3:-src/commands/${PARENT_COMMAND}/${SUBCOMMAND}.ts}"

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "📝 Generating subcommand: $PARENT_COMMAND $SUBCOMMAND"

cat > "$OUTPUT_FILE" << 'EOF'
import { Command } from 'commander';
import chalk from 'chalk';

export function create{{SUBCOMMAND_PASCAL}}Command(): Command {
  const command = new Command('{{SUBCOMMAND}}')
    .description('{{DESCRIPTION}}')
    .action(async (options) => {
      try {
        console.log(chalk.blue(`Running {{PARENT_COMMAND}} {{SUBCOMMAND}}...`));

        // TODO: Implement subcommand logic

        console.log(chalk.green('✓ Subcommand completed'));
      } catch (error) {
        console.error(chalk.red('✗ Subcommand failed:'), error.message);
        process.exit(1);
      }
    });

  return command;
}
EOF

# Convert to PascalCase
SUBCOMMAND_PASCAL=$(echo "$SUBCOMMAND" | sed -r 's/(^|-)([a-z])/\U\2/g')

# Replace placeholders
sed -i "s/{{PARENT_COMMAND}}/$PARENT_COMMAND/g" "$OUTPUT_FILE"
sed -i "s/{{SUBCOMMAND}}/$SUBCOMMAND/g" "$OUTPUT_FILE"
sed -i "s/{{SUBCOMMAND_PASCAL}}/$SUBCOMMAND_PASCAL/g" "$OUTPUT_FILE"
sed -i "s/{{DESCRIPTION}}/$SUBCOMMAND operation for $PARENT_COMMAND/g" "$OUTPUT_FILE"

# Generate parent command file if it doesn't exist
PARENT_FILE="src/commands/${PARENT_COMMAND}/index.ts"
if [[ ! -f "$PARENT_FILE" ]]; then
  mkdir -p "$(dirname "$PARENT_FILE")"
  cat > "$PARENT_FILE" << EOF
import { Command } from 'commander';
import { create${SUBCOMMAND_PASCAL}Command } from './${SUBCOMMAND}';

export function create${PARENT_COMMAND^}Command(): Command {
  const command = new Command('${PARENT_COMMAND}')
    .description('${PARENT_COMMAND^} operations');

  // Add subcommands
  command.addCommand(create${SUBCOMMAND_PASCAL}Command());

  return command;
}
EOF
  echo "✅ Created parent command: $PARENT_FILE"
fi

echo "✅ Subcommand generated: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Implement subcommand logic"
echo "  2. Add to parent command: ${PARENT_FILE}"
echo "  3. Import parent in main CLI: program.addCommand(create${PARENT_COMMAND^}Command())"
echo ""
