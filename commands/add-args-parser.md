---
description: Add advanced argument parsing capabilities
argument-hint: none
allowed-tools: Task, Read, Write, Edit, Bash, Glob
---

**Arguments**: $ARGUMENTS

Goal: Add comprehensive argument parsing with positional args, flags, options, validators, and type coercion

Core Principles:
- Detect framework first, don't assume
- Match existing code style and patterns
- Support all common parsing features
- Provide clear usage examples

Phase 1: Discovery
Goal: Detect CLI framework and current structure

Actions:
- Find main CLI file: !{bash ls bin/* src/cli.* cli.* 2>/dev/null | head -5}
- Detect language and framework by checking for:
  - Python: argparse, click, typer imports
  - Node.js: commander, yargs, minimist requires
  - Go: flag, cobra, urfave/cli imports
  - Bash: getopt usage
- Load main CLI file for analysis
- Check if argument parsing already exists

Phase 2: Analysis
Goal: Understand current argument handling

Actions:
- Read the main CLI file identified
- Identify current parsing approach (if any)
- Find where commands are defined
- Determine integration points for new parsing logic
- Check package dependencies for CLI libraries

Phase 3: Implementation
Goal: Add comprehensive argument parsing capabilities

Actions:

Task(description="Add argument parsing", subagent_type="args-parser-agent", prompt="You are the args-parser-agent. Add comprehensive argument parsing to this CLI tool.

Framework Detection:
- Analyze existing code to identify language and framework
- Use the most appropriate parsing library for the detected framework
- If no framework exists, choose the most suitable one

Parsing Features to Implement:
1. Positional Arguments:
   - Define named positional args
   - Support optional vs required
   - Set default values
   - Add help text for each

2. Options/Flags:
   - Short form: -v, -h, -o
   - Long form: --verbose, --help, --output
   - Boolean flags (no value needed)
   - Value options (--name VALUE)
   - Multiple values (--tag tag1 --tag tag2)

3. Type Coercion:
   - String, integer, float types
   - File path validation
   - URL validation
   - Email validation
   - Enum/choice types

4. Advanced Features:
   - Mutually exclusive options (--json OR --yaml)
   - Dependent options (--output requires --format)
   - Variadic arguments (accept multiple values)
   - Subcommands if applicable
   - Environment variable fallbacks

5. Validation:
   - Required vs optional enforcement
   - Value range checking (min/max)
   - Pattern matching (regex)
   - Custom validator functions
   - Clear error messages

6. Help Generation:
   - Auto-generate usage text
   - Group options by category
   - Show examples
   - Display defaults

Example Patterns by Framework:
- Python argparse: parser.add_argument('--verbose', action='store_true')
- Python click: @click.option('--verbose', is_flag=True)
- Node commander: program.option('-v, --verbose', 'verbose output')
- Go flag: flag.Bool(\"verbose\", false, \"verbose output\")

Requirements:
- Match existing code style (indentation, naming)
- Add clear inline comments
- Include usage examples in help text
- Set sensible defaults
- Provide type hints/annotations where applicable
- Handle errors gracefully with helpful messages

Deliverable: Updated CLI file with comprehensive argument parsing")

Phase 4: Verification
Goal: Ensure parsing works correctly

Actions:
- Check syntax based on language:
  - Python: !{bash python -m py_compile bin/* 2>&1 | head -20}
  - Node.js: !{bash node -c "require('./cli.js')" 2>&1}
  - Go: !{bash go build . 2>&1 | head -20}
- Display key changes made
- Show example usage commands

Phase 5: Summary
Goal: Document the implementation

Actions:
- Summarize argument parsing features added:
  - Positional arguments defined
  - Options and flags available
  - Validators and types configured
  - Special features (mutually exclusive, etc.)
- Provide usage examples
- Note any framework-specific considerations
- Suggest testing approach
