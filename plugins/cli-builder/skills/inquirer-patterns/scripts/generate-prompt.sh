#!/bin/bash

# generate-prompt.sh
# Generate boilerplate prompt code for Node.js or Python

set -e

# Default values
PROMPT_TYPE=""
LANGUAGE=""
OUTPUT_FILE=""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage information
usage() {
    echo "Usage: $0 --type <prompt-type> --lang <language> [--output <file>]"
    echo
    echo "Options:"
    echo "  --type    Prompt type: text, list, checkbox, password, autocomplete, conditional"
    echo "  --lang    Language: js (Node.js) or py (Python)"
    echo "  --output  Output file path (optional)"
    echo
    echo "Examples:"
    echo "  $0 --type text --lang js --output my-prompt.js"
    echo "  $0 --type checkbox --lang py"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --type)
            PROMPT_TYPE="$2"
            shift 2
            ;;
        --lang)
            LANGUAGE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate arguments
if [ -z "$PROMPT_TYPE" ] || [ -z "$LANGUAGE" ]; then
    echo "Error: --type and --lang are required"
    usage
fi

# Validate prompt type
VALID_TYPES=("text" "list" "checkbox" "password" "autocomplete" "conditional")
if [[ ! " ${VALID_TYPES[@]} " =~ " ${PROMPT_TYPE} " ]]; then
    echo "Error: Invalid prompt type '$PROMPT_TYPE'"
    echo "Valid types: ${VALID_TYPES[*]}"
    exit 1
fi

# Validate language
if [ "$LANGUAGE" != "js" ] && [ "$LANGUAGE" != "py" ]; then
    echo "Error: Language must be 'js' or 'py'"
    exit 1
fi

# Set default output file if not specified
if [ -z "$OUTPUT_FILE" ]; then
    if [ "$LANGUAGE" == "js" ]; then
        OUTPUT_FILE="${PROMPT_TYPE}-prompt.js"
    else
        OUTPUT_FILE="${PROMPT_TYPE}_prompt.py"
    fi
fi

echo -e "${BLUE}🔧 Generating $PROMPT_TYPE prompt for $LANGUAGE...${NC}"
echo

# Generate Node.js code
if [ "$LANGUAGE" == "js" ]; then
    case $PROMPT_TYPE in
        text)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';

async function textPrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'fieldName',
      message: 'Enter value:',
      validate: (input) => input.length > 0 || 'This field is required'
    }
  ]);

  console.log('Answer:', answers.fieldName);
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  textPrompt().then(() => process.exit(0)).catch(console.error);
}

export { textPrompt };
EOF
            ;;
        list)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';

async function listPrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'list',
      name: 'selection',
      message: 'Choose an option:',
      choices: ['Option 1', 'Option 2', 'Option 3']
    }
  ]);

  console.log('Selected:', answers.selection);
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  listPrompt().then(() => process.exit(0)).catch(console.error);
}

export { listPrompt };
EOF
            ;;
        checkbox)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';

async function checkboxPrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'checkbox',
      name: 'selections',
      message: 'Select options:',
      choices: ['Option 1', 'Option 2', 'Option 3'],
      validate: (choices) => choices.length > 0 || 'Select at least one option'
    }
  ]);

  console.log('Selected:', answers.selections);
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  checkboxPrompt().then(() => process.exit(0)).catch(console.error);
}

export { checkboxPrompt };
EOF
            ;;
        password)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';

async function passwordPrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'password',
      name: 'password',
      message: 'Enter password:',
      mask: '*',
      validate: (input) => input.length >= 8 || 'Password must be at least 8 characters'
    },
    {
      type: 'password',
      name: 'confirm',
      message: 'Confirm password:',
      mask: '*',
      validate: (input, answers) => input === answers.password || 'Passwords do not match'
    }
  ]);

  console.log('Password set successfully');
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  passwordPrompt().then(() => process.exit(0)).catch(console.error);
}

export { passwordPrompt };
EOF
            ;;
        autocomplete)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';
import inquirerAutocomplete from 'inquirer-autocomplete-prompt';

inquirer.registerPrompt('autocomplete', inquirerAutocomplete);

const choices = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5'];

function searchChoices(input) {
  if (!input) return choices;
  return choices.filter(choice => choice.toLowerCase().includes(input.toLowerCase()));
}

async function autocompletePrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'autocomplete',
      name: 'selection',
      message: 'Search for an option:',
      source: (answersSoFar, input) => Promise.resolve(searchChoices(input))
    }
  ]);

  console.log('Selected:', answers.selection);
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  autocompletePrompt().then(() => process.exit(0)).catch(console.error);
}

export { autocompletePrompt };
EOF
            ;;
        conditional)
            cat > "$OUTPUT_FILE" << 'EOF'
import inquirer from 'inquirer';

async function conditionalPrompt() {
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'continue',
      message: 'Do you want to continue?',
      default: true
    },
    {
      type: 'input',
      name: 'details',
      message: 'Enter details:',
      when: (answers) => answers.continue,
      validate: (input) => input.length > 0 || 'Details required'
    }
  ]);

  console.log('Answers:', answers);
  return answers;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  conditionalPrompt().then(() => process.exit(0)).catch(console.error);
}

export { conditionalPrompt };
EOF
            ;;
    esac
fi

# Generate Python code
if [ "$LANGUAGE" == "py" ]; then
    case $PROMPT_TYPE in
        text)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def text_prompt():
    answer = questionary.text(
        "Enter value:",
        validate=lambda text: len(text) > 0 or "This field is required"
    ).ask()

    print(f"Answer: {answer}")
    return answer

if __name__ == "__main__":
    text_prompt()
EOF
            ;;
        list)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def list_prompt():
    answer = questionary.select(
        "Choose an option:",
        choices=['Option 1', 'Option 2', 'Option 3']
    ).ask()

    print(f"Selected: {answer}")
    return answer

if __name__ == "__main__":
    list_prompt()
EOF
            ;;
        checkbox)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def checkbox_prompt():
    answers = questionary.checkbox(
        "Select options:",
        choices=['Option 1', 'Option 2', 'Option 3'],
        validate=lambda choices: len(choices) > 0 or "Select at least one option"
    ).ask()

    print(f"Selected: {answers}")
    return answers

if __name__ == "__main__":
    checkbox_prompt()
EOF
            ;;
        password)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def password_prompt():
    password = questionary.password(
        "Enter password:",
        validate=lambda text: len(text) >= 8 or "Password must be at least 8 characters"
    ).ask()

    confirm = questionary.password(
        "Confirm password:",
        validate=lambda text: text == password or "Passwords do not match"
    ).ask()

    print("Password set successfully")
    return password

if __name__ == "__main__":
    password_prompt()
EOF
            ;;
        autocomplete)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def autocomplete_prompt():
    choices = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option 5']

    answer = questionary.autocomplete(
        "Search for an option:",
        choices=choices
    ).ask()

    print(f"Selected: {answer}")
    return answer

if __name__ == "__main__":
    autocomplete_prompt()
EOF
            ;;
        conditional)
            cat > "$OUTPUT_FILE" << 'EOF'
import questionary

def conditional_prompt():
    continue_prompt = questionary.confirm(
        "Do you want to continue?",
        default=True
    ).ask()

    details = None
    if continue_prompt:
        details = questionary.text(
            "Enter details:",
            validate=lambda text: len(text) > 0 or "Details required"
        ).ask()

    result = {
        'continue': continue_prompt,
        'details': details
    }

    print(f"Answers: {result}")
    return result

if __name__ == "__main__":
    conditional_prompt()
EOF
            ;;
    esac
fi

# Make Python files executable
if [ "$LANGUAGE" == "py" ]; then
    chmod +x "$OUTPUT_FILE"
fi

echo -e "${GREEN}✅ Generated: $OUTPUT_FILE${NC}"
echo
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "  1. Edit the generated file to customize your prompt"
if [ "$LANGUAGE" == "js" ]; then
    echo "  2. Run: node $OUTPUT_FILE"
else
    echo "  2. Run: python3 $OUTPUT_FILE"
fi
echo

echo -e "${BLUE}💡 Tip: Check out the templates directory for more advanced examples${NC}"
