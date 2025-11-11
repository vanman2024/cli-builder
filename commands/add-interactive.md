---
description: Add interactive prompts and menus
argument-hint: none
allowed-tools: Bash, Read, Write, Edit
---

**Arguments**: $ARGUMENTS

Goal: Add interactive prompt capabilities to CLI tools with language-specific libraries and example implementations.

Core Principles:
- Detect project language before installing dependencies
- Install appropriate library for Node.js or Python
- Generate comprehensive examples covering all prompt types
- Provide validation patterns and conditional logic examples

Phase 1: Discovery
Goal: Detect project language and structure

Actions:
- Check for package.json (Node.js) or pyproject.toml/requirements.txt (Python)
- Detect existing dependencies to avoid conflicts
- Example: !{bash ls package.json pyproject.toml requirements.txt setup.py 2>/dev/null}

Phase 2: Dependency Installation
Goal: Install appropriate interactive prompt library

Actions:

For Node.js projects (package.json exists):
- Install inquirer (most popular, comprehensive features)
- Example: !{bash npm install inquirer @types/inquirer --save}
- Alternative: prompts (lightweight) or enquirer (fast, minimal)

For Python projects:
- Install questionary (modern, intuitive API)
- Example: !{bash pip install questionary}
- Alternative: PyInquirer (feature-rich but older)

Confirm installation success with version check.

Phase 3: Generate Examples
Goal: Create comprehensive interactive prompt examples

Actions:

Create examples/interactive-prompts directory.

Generate example file with ALL prompt types:

**For Node.js (inquirer):**
- Text input with validation
- Select menu (single choice)
- Multi-select checkbox
- Password input (masked)
- Confirmation (yes/no)
- Number input with range validation
- Editor input (multi-line)
- Conditional questions (show based on previous answers)

**For Python (questionary):**
- Text input with validation
- Select menu with autocomplete
- Checkbox (multi-select)
- Password input (hidden)
- Confirmation
- Path input with file browser
- Conditional questions

Example structure:
- examples/interactive-prompts/basic-prompts.js (or basic-prompts.py)
- examples/interactive-prompts/wizard-example.js (or wizard-example.py)
- examples/interactive-prompts/validation-patterns.js (or validation-patterns.py)

Phase 4: Implementation Files
Goal: Write example code files

Actions:

Write basic-prompts file with:
- Import statements
- Simple examples for each prompt type
- Comments explaining usage
- Error handling

Write wizard-example file with:
- Multi-step interactive wizard
- Conditional logic
- Data collection and summary
- User-friendly output

Write validation-patterns file with:
- Email validation
- URL validation
- Number range validation
- Required field validation
- Custom validation functions

Phase 5: Documentation
Goal: Create usage documentation

Actions:

Create INTERACTIVE-PROMPTS.md in docs/ with:
- Library overview and installation
- Quick start guide
- All prompt types with examples
- Validation patterns
- Best practices
- Troubleshooting tips

Include code snippets for common use cases:
- Simple yes/no confirmation
- Configuration wizard
- Multi-step form
- Dynamic menu generation

Phase 6: Summary
Goal: Report what was added

Actions:
- Display installed library and version
- List generated example files with paths
- Show quick start command to run examples
- Suggest next steps for integration
