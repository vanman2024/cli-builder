#!/bin/bash
# Generate Commander.js command with options and arguments

set -euo pipefail

COMMAND_NAME="${1:?Usage: $0 <command-name> [output-file]}"
OUTPUT_FILE="${2:-src/commands/${COMMAND_NAME}.ts}"

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "📝 Generating Commander.js command: $COMMAND_NAME"

cat > "$OUTPUT_FILE" << 'EOF'
import { Command, Option } from 'commander';
import chalk from 'chalk';

export function create{{COMMAND_NAME_PASCAL}}Command(): Command {
  const command = new Command('{{COMMAND_NAME}}')
    .description('{{DESCRIPTION}}')
    .option('-v, --verbose', 'verbose output', false)
    .addOption(
      new Option('-e, --environment <env>', 'target environment')
        .choices(['dev', 'staging', 'prod'])
        .default('dev')
    )
    .action(async (options) => {
      try {
        console.log(chalk.blue(`Running {{COMMAND_NAME}} command...`));
        console.log('Options:', options);

        // TODO: Implement command logic

        console.log(chalk.green('✓ Command completed successfully'));
      } catch (error) {
        console.error(chalk.red('✗ Command failed:'), error.message);
        process.exit(1);
      }
    });

  return command;
}
EOF

# Convert command name to PascalCase
COMMAND_NAME_PASCAL=$(echo "$COMMAND_NAME" | sed -r 's/(^|-)([a-z])/\U\2/g')

# Replace placeholders
sed -i "s/{{COMMAND_NAME}}/$COMMAND_NAME/g" "$OUTPUT_FILE"
sed -i "s/{{COMMAND_NAME_PASCAL}}/$COMMAND_NAME_PASCAL/g" "$OUTPUT_FILE"
sed -i "s/{{DESCRIPTION}}/Execute $COMMAND_NAME operation/g" "$OUTPUT_FILE"

echo "✅ Command generated: $OUTPUT_FILE"
echo ""
echo "Next steps:"
echo "  1. Implement command logic in the action handler"
echo "  2. Add custom options and arguments as needed"
echo "  3. Import and add to main CLI: program.addCommand(create${COMMAND_NAME_PASCAL}Command())"
echo ""
