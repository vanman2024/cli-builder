# Inquirer Patterns Skill

Comprehensive interactive prompt patterns for building CLI tools with rich user input capabilities.

## Overview

This skill provides templates, examples, and utilities for implementing interactive CLI prompts in both **Node.js** (using `inquirer`) and **Python** (using `questionary`). It covers all major prompt types with validation, conditional logic, and real-world examples.

## Prompt Types Covered

### 1. Text Input
- Simple string input
- Email, URL, and path validation
- Numeric input with range validation
- Multi-line text

### 2. List Selection
- Single choice from options
- Categorized options with separators
- Options with descriptions and shortcuts
- Dynamic choices based on context

### 3. Checkbox
- Multiple selections
- Pre-selected defaults
- Grouped options
- Validation (min/max selections)

### 4. Password
- Hidden input with mask characters
- Password confirmation
- Strength validation
- API key and token input

### 5. Autocomplete
- Type-ahead search
- Fuzzy matching
- Large option lists
- Dynamic filtering

### 6. Conditional Questions
- Skip logic based on answers
- Dynamic question flow
- Branching paths
- Context-dependent validation

## Directory Structure

```
inquirer-patterns/
├── SKILL.md                          # Main skill documentation
├── README.md                         # This file
├── templates/
│   ├── nodejs/
│   │   ├── text-prompt.js           # Text input examples
│   │   ├── list-prompt.js           # List selection examples
│   │   ├── checkbox-prompt.js       # Checkbox examples
│   │   ├── password-prompt.js       # Password/secure input
│   │   ├── autocomplete-prompt.js   # Autocomplete examples
│   │   ├── conditional-prompt.js    # Conditional logic
│   │   └── comprehensive-example.js # Complete wizard
│   └── python/
│       ├── text_prompt.py
│       ├── list_prompt.py
│       ├── checkbox_prompt.py
│       ├── password_prompt.py
│       ├── autocomplete_prompt.py
│       └── conditional_prompt.py
├── scripts/
│   ├── install-nodejs-deps.sh       # Install Node.js packages
│   ├── install-python-deps.sh       # Install Python packages
│   ├── validate-prompts.sh          # Validate skill structure
│   └── generate-prompt.sh           # Generate boilerplate code
└── examples/
    ├── nodejs/
    │   └── project-init-wizard.js   # Full project setup wizard
    └── python/
        └── project_init_wizard.py   # Full project setup wizard
```

## Quick Start

### Node.js

1. **Install dependencies:**
   ```bash
   ./scripts/install-nodejs-deps.sh
   ```

2. **Run an example:**
   ```bash
   node templates/nodejs/text-prompt.js
   node templates/nodejs/comprehensive-example.js
   ```

3. **Generate boilerplate:**
   ```bash
   ./scripts/generate-prompt.sh --type checkbox --lang js --output my-prompt.js
   ```

### Python

1. **Install dependencies:**
   ```bash
   ./scripts/install-python-deps.sh
   ```

2. **Run an example:**
   ```bash
   python3 templates/python/text_prompt.py
   python3 templates/python/conditional_prompt.py
   ```

3. **Generate boilerplate:**
   ```bash
   ./scripts/generate-prompt.sh --type list --lang py --output my_prompt.py
   ```

## Key Features

### Validation Patterns

All templates include comprehensive validation examples:
- **Required fields**: Ensure input is not empty
- **Format validation**: Email, URL, regex patterns
- **Range validation**: Numeric min/max values
- **Custom validation**: Business logic rules
- **Cross-field validation**: Compare multiple answers

### Error Handling

Examples demonstrate proper error handling:
- Graceful Ctrl+C handling
- TTY detection for non-interactive environments
- User-friendly error messages
- Validation feedback

### Best Practices

Templates follow CLI best practices:
- Clear, descriptive prompts
- Sensible defaults
- Keyboard shortcuts
- Progressive disclosure
- Accessibility considerations

## Usage Examples

### Text Input with Validation

**Node.js:**
```javascript
import inquirer from 'inquirer';

const answer = await inquirer.prompt([{
  type: 'input',
  name: 'email',
  message: 'Enter your email:',
  validate: (input) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(input) || 'Invalid email address';
  }
}]);
```

**Python:**
```python
import questionary

email = questionary.text(
    "Enter your email:",
    validate=lambda text: bool(re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', text))
                         or "Invalid email address"
).ask()
```

### Conditional Questions

**Node.js:**
```javascript
const answers = await inquirer.prompt([
  {
    type: 'confirm',
    name: 'useDatabase',
    message: 'Use database?',
    default: true
  },
  {
    type: 'list',
    name: 'dbType',
    message: 'Database type:',
    choices: ['PostgreSQL', 'MySQL', 'MongoDB'],
    when: (answers) => answers.useDatabase
  }
]);
```

**Python:**
```python
use_database = questionary.confirm("Use database?", default=True).ask()

if use_database:
    db_type = questionary.select(
        "Database type:",
        choices=['PostgreSQL', 'MySQL', 'MongoDB']
    ).ask()
```

### Multiple Selections

**Node.js:**
```javascript
const answers = await inquirer.prompt([{
  type: 'checkbox',
  name: 'features',
  message: 'Select features:',
  choices: ['Auth', 'Database', 'API Docs', 'Testing'],
  validate: (choices) => choices.length > 0 || 'Select at least one'
}]);
```

**Python:**
```python
features = questionary.checkbox(
    "Select features:",
    choices=['Auth', 'Database', 'API Docs', 'Testing'],
    validate=lambda c: len(c) > 0 or "Select at least one"
).ask()
```

## Validation

Run the validation script to check skill structure:

```bash
./scripts/validate-prompts.sh
```

This checks:
- ✅ SKILL.md structure and frontmatter
- ✅ Required templates exist
- ✅ Scripts are executable
- ✅ No hardcoded secrets
- ✅ Basic syntax validation

## Dependencies

### Node.js
- `inquirer@^9.0.0` - Core prompting library
- `inquirer-autocomplete-prompt@^3.0.0` - Autocomplete support
- `chalk@^5.0.0` - Terminal colors (optional)

### Python
- `questionary>=2.0.0` - Core prompting library
- `prompt_toolkit>=3.0.0` - Terminal UI toolkit
- `colorama` - Windows color support (optional)

## Real-World Use Cases

### Project Initialization
See `examples/nodejs/project-init-wizard.js` and `examples/python/project_init_wizard.py` for complete project setup wizards.

### Configuration Management
Templates show how to build interactive config generators for:
- Database connections
- API credentials
- Deployment settings
- Feature flags
- CI/CD pipelines

### Interactive Installers
Examples demonstrate building user-friendly installers with:
- Dependency selection
- Environment setup
- Credential collection
- Validation and verification

## Troubleshooting

### Node.js: "Error [ERR_REQUIRE_ESM]"
**Solution**: Use `import` instead of `require`, or add `"type": "module"` to package.json

### Python: "No module named 'questionary'"
**Solution**: Run `./scripts/install-python-deps.sh` or `pip install questionary`

### Autocomplete not working
**Solution**: Install the autocomplete plugin:
- Node.js: `npm install inquirer-autocomplete-prompt`
- Python: Built into questionary

### Terminal rendering issues
**Solution**: Ensure terminal supports ANSI escape codes. On Windows, install `colorama`.

## Contributing

When adding new patterns:
1. Add template to both `templates/nodejs/` and `templates/python/`
2. Include comprehensive validation examples
3. Add real-world usage examples
4. Update this README
5. Run validation: `./scripts/validate-prompts.sh`

## License

Part of the CLI Builder plugin.

## Resources

- **Inquirer.js**: https://github.com/SBoudrias/Inquirer.js
- **Questionary**: https://github.com/tmbo/questionary
- **Prompt Toolkit**: https://github.com/prompt-toolkit/python-prompt-toolkit
- **CLI Best Practices**: https://clig.dev/

---

**Created**: 2025
**Maintained by**: CLI Builder Plugin
**Skill Version**: 1.0.0
