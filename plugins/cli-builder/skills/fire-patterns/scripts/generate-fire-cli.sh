#!/bin/bash
# Generate Fire CLI from specification

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$(dirname "$SCRIPT_DIR")/templates"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Generate a Python Fire CLI application from templates.

OPTIONS:
    -n, --name NAME          CLI name (required)
    -d, --description DESC   CLI description (required)
    -t, --template TYPE      Template type: basic, nested, rich, typed, config, multi (default: basic)
    -o, --output FILE        Output file path (required)
    -c, --class-name NAME    Main class name (default: CLI)
    -v, --version VERSION    Version number (default: 1.0.0)
    -h, --help              Show this help message

TEMPLATE TYPES:
    basic   - Simple single-class Fire CLI
    nested  - Multi-class CLI with command groups
    rich    - Fire CLI with rich console output
    typed   - Type-annotated Fire CLI with full type hints
    config  - Fire CLI with comprehensive configuration management
    multi   - Complex multi-command Fire CLI

EXAMPLES:
    $(basename "$0") -n mycli -d "My CLI tool" -o mycli.py
    $(basename "$0") -n deploy-tool -d "Deployment CLI" -t nested -o deploy.py
    $(basename "$0") -n mytool -d "Advanced tool" -t typed -c MyTool -o tool.py

EOF
    exit 1
}

# Parse command line arguments
CLI_NAME=""
DESCRIPTION=""
TEMPLATE="basic"
OUTPUT_FILE=""
CLASS_NAME="CLI"
VERSION="1.0.0"

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            CLI_NAME="$2"
            shift 2
            ;;
        -d|--description)
            DESCRIPTION="$2"
            shift 2
            ;;
        -t|--template)
            TEMPLATE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -c|--class-name)
            CLASS_NAME="$2"
            shift 2
            ;;
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Error: Unknown option $1${NC}"
            usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$CLI_NAME" ]]; then
    echo -e "${RED}Error: CLI name is required${NC}"
    usage
fi

if [[ -z "$DESCRIPTION" ]]; then
    echo -e "${RED}Error: Description is required${NC}"
    usage
fi

if [[ -z "$OUTPUT_FILE" ]]; then
    echo -e "${RED}Error: Output file is required${NC}"
    usage
fi

# Validate template type
TEMPLATE_FILE=""
case $TEMPLATE in
    basic)
        TEMPLATE_FILE="$TEMPLATES_DIR/basic-fire-cli.py.template"
        ;;
    nested)
        TEMPLATE_FILE="$TEMPLATES_DIR/nested-fire-cli.py.template"
        ;;
    rich)
        TEMPLATE_FILE="$TEMPLATES_DIR/rich-fire-cli.py.template"
        ;;
    typed)
        TEMPLATE_FILE="$TEMPLATES_DIR/typed-fire-cli.py.template"
        ;;
    config)
        TEMPLATE_FILE="$TEMPLATES_DIR/config-fire-cli.py.template"
        ;;
    multi)
        TEMPLATE_FILE="$TEMPLATES_DIR/multi-command-fire-cli.py.template"
        ;;
    *)
        echo -e "${RED}Error: Invalid template type: $TEMPLATE${NC}"
        echo "Valid types: basic, nested, rich, typed, config, multi"
        exit 1
        ;;
esac

if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo -e "${RED}Error: Template file not found: $TEMPLATE_FILE${NC}"
    exit 1
fi

# Prepare variables
CLI_NAME_LOWER=$(echo "$CLI_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
DEFAULT_PROJECT_NAME="my-project"
SUBCOMMAND_GROUP_NAME="Resources"
SUBCOMMAND_GROUP_DESCRIPTION="Resource management commands"
SUBCOMMAND_GROUP_NAME_LOWER="resources"
RESOURCE_NAME="resource"

echo -e "${BLUE}Generating Fire CLI...${NC}"
echo -e "${BLUE}  Name:        ${NC}$CLI_NAME"
echo -e "${BLUE}  Description: ${NC}$DESCRIPTION"
echo -e "${BLUE}  Template:    ${NC}$TEMPLATE"
echo -e "${BLUE}  Class:       ${NC}$CLASS_NAME"
echo -e "${BLUE}  Version:     ${NC}$VERSION"
echo -e "${BLUE}  Output:      ${NC}$OUTPUT_FILE"

# Generate CLI by replacing template variables
sed -e "s/{{CLI_NAME}}/$CLI_NAME/g" \
    -e "s/{{CLI_DESCRIPTION}}/$DESCRIPTION/g" \
    -e "s/{{CLASS_NAME}}/$CLASS_NAME/g" \
    -e "s/{{CLI_NAME_LOWER}}/$CLI_NAME_LOWER/g" \
    -e "s/{{VERSION}}/$VERSION/g" \
    -e "s/{{DEFAULT_PROJECT_NAME}}/$DEFAULT_PROJECT_NAME/g" \
    -e "s/{{SUBCOMMAND_GROUP_NAME}}/$SUBCOMMAND_GROUP_NAME/g" \
    -e "s/{{SUBCOMMAND_GROUP_DESCRIPTION}}/$SUBCOMMAND_GROUP_DESCRIPTION/g" \
    -e "s/{{SUBCOMMAND_GROUP_NAME_LOWER}}/$SUBCOMMAND_GROUP_NAME_LOWER/g" \
    -e "s/{{RESOURCE_NAME}}/$RESOURCE_NAME/g" \
    "$TEMPLATE_FILE" > "$OUTPUT_FILE"

# Make executable
chmod +x "$OUTPUT_FILE"

echo -e "${GREEN}✓ Generated Fire CLI: $OUTPUT_FILE${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Review and customize: ${BLUE}$OUTPUT_FILE${NC}"
echo -e "  2. Install dependencies: ${BLUE}pip install fire rich${NC}"
echo -e "  3. Test the CLI: ${BLUE}python $OUTPUT_FILE --help${NC}"
echo -e "  4. Validate: ${BLUE}$SCRIPT_DIR/validate-fire-cli.py $OUTPUT_FILE${NC}"
