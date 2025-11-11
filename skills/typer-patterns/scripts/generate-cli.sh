#!/bin/bash
# Generate a Typer CLI from template

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Usage
usage() {
    cat << EOF
Usage: $0 <template-name> <output-file> [options]

Templates:
  basic       - Basic typed command
  enum        - Enum-based options
  subapp      - Sub-application structure
  factory     - Factory pattern
  validation  - Advanced validation

Options:
  --app-name NAME    Set application name (default: mycli)
  --help            Show this help

Example:
  $0 basic my_cli.py --app-name myapp
EOF
    exit 0
}

# Parse arguments
if [ $# -lt 2 ]; then
    usage
fi

TEMPLATE="$1"
OUTPUT="$2"
APP_NAME="mycli"

shift 2

while [ $# -gt 0 ]; do
    case "$1" in
        --app-name)
            APP_NAME="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$(dirname "$SCRIPT_DIR")/templates"

# Map template name to file
case "$TEMPLATE" in
    basic)
        TEMPLATE_FILE="$TEMPLATE_DIR/basic-typed-command.py"
        ;;
    enum)
        TEMPLATE_FILE="$TEMPLATE_DIR/enum-options.py"
        ;;
    subapp)
        TEMPLATE_FILE="$TEMPLATE_DIR/sub-app-structure.py"
        ;;
    factory)
        TEMPLATE_FILE="$TEMPLATE_DIR/typer-instance.py"
        ;;
    validation)
        TEMPLATE_FILE="$TEMPLATE_DIR/advanced-validation.py"
        ;;
    *)
        echo "Unknown template: $TEMPLATE"
        usage
        ;;
esac

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${YELLOW}✗ Template not found: $TEMPLATE_FILE${NC}"
    exit 1
fi

# Copy and customize template
cp "$TEMPLATE_FILE" "$OUTPUT"

# Replace app name if not default
if [ "$APP_NAME" != "mycli" ]; then
    sed -i "s/mycli/$APP_NAME/g" "$OUTPUT"
    sed -i "s/myapp/$APP_NAME/g" "$OUTPUT"
fi

# Make executable
chmod +x "$OUTPUT"

echo -e "${GREEN}✓ Generated CLI: $OUTPUT${NC}"
echo "  Template: $TEMPLATE"
echo "  App name: $APP_NAME"
echo ""
echo "Next steps:"
echo "  1. Review and customize the generated file"
echo "  2. Install dependencies: pip install typer"
echo "  3. Run: python $OUTPUT --help"
echo "  4. Validate: ./scripts/validate-types.sh $OUTPUT"
