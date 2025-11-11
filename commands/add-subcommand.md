---
description: Add structured subcommands to CLI tool
argument-hint: <command-name>
allowed-tools: Task, AskUserQuestion, Bash, Read, Write, Edit, Glob
---

**Arguments**: $ARGUMENTS

Goal: Add a well-structured subcommand to existing CLI tool matching framework patterns

Core Principles:
- Detect framework before generating code
- Match existing code patterns and conventions
- Include validation and error handling
- Generate idiomatic framework-specific code

Phase 1: Discovery
Goal: Understand CLI project structure and framework

Actions:
- Parse $ARGUMENTS for subcommand name
- If no name provided, ask user for subcommand name
- Detect language: !{bash ls package.json tsconfig.json pyproject.toml setup.py go.mod Cargo.toml 2>/dev/null}
- Identify framework:
  - Node.js: Check package.json for commander, yargs, oclif
  - Python: Search for click, typer, argparse imports in main file
  - Go: Check go.mod for cobra or cli packages
  - Rust: Check Cargo.toml for clap
- Load existing CLI entry point to understand structure

Phase 2: Gather Requirements
Goal: Collect subcommand specifications

Actions:
- Use AskUserQuestion to gather:
  - Subcommand description and purpose
  - Required positional arguments
  - Optional flags and options
  - Validation requirements
- Document requirements for implementation

Phase 3: Implementation
Goal: Generate and integrate subcommand code

Actions:

Invoke cli-feature-impl agent to generate framework-specific code.

Task(description="Generate subcommand implementation", subagent_type="cli-feature-impl", prompt="You are the cli-feature-impl agent. Generate a subcommand named $ARGUMENTS for the detected CLI framework.

Context:
- Framework detected: DETECTED_FRAMEWORK
- Language: DETECTED_LANGUAGE
- User requirements: USER_REQUIREMENTS

Requirements:
- Match existing code style and patterns
- Include argument/option definitions with validation
- Add comprehensive error handling
- Generate help text and descriptions
- Follow framework best practices
- Include inline comments for clarity

Deliverable:
- Complete subcommand code ready for integration
- List of files to create or modify
- Import statements needed
- Integration instructions")

Phase 4: Integration and Validation
Goal: Add code to project and verify

Actions:
- Review generated code from agent
- Integrate into appropriate location:
  - Separate command file if framework uses that pattern
  - Add to main file if inline commands
- Add necessary imports and dependencies
- Test syntax validation:
  - Node.js: !{bash npm run typecheck 2>&1 || echo "Syntax check skipped"}
  - Python: !{bash python -m py_compile MAIN_FILE 2>&1}
- Test help output: !{bash TOOL_NAME COMMAND_NAME --help 2>&1}

Phase 5: Summary
Goal: Document changes and next steps

Actions:
- Report files modified or created
- Show example usage:
  - TOOL_NAME COMMAND_NAME --help
  - TOOL_NAME COMMAND_NAME [arguments] [options]
- List next steps:
  - Implement business logic
  - Add tests
  - Update documentation
