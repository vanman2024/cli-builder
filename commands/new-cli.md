---
description: Initialize new CLI tool project with framework selection
argument-hint: <tool-name>
allowed-tools: AskUserQuestion, Bash(*), Read, Write, Edit
---

**Arguments**: $ARGUMENTS

Goal: Initialize a new CLI tool project with user-selected language and framework, complete with proper structure, dependencies, and configuration.

Core Principles:
- Ask user for preferences before generating
- Detect package managers available in environment
- Follow framework conventions for each language
- Generate working entry point with proper shebang
- Initialize git repository and create essential files

Phase 1: Gather Requirements
Goal: Collect user preferences for language and framework

Actions:
- Parse $ARGUMENTS for tool name
- If no tool name provided, ask user for it
- Ask user for language preference using AskUserQuestion:
  - Options: TypeScript, Python, Go, Rust
- Based on language selection, ask for framework:
  - Python: Click, Typer, argparse, Fire
  - TypeScript: Commander.js, yargs, oclif, gluegun
  - Go: Cobra, cli
  - Rust: clap
- Ask for package manager preference if applicable

Phase 2: Environment Validation
Goal: Verify required tools are available

Actions:
- Check if selected language runtime is installed
- Example: !{bash python3 --version 2>/dev/null || echo "Not found"}
- Example: !{bash node --version 2>/dev/null || echo "Not found"}
- Example: !{bash go version 2>/dev/null || echo "Not found"}
- Example: !{bash rustc --version 2>/dev/null || echo "Not found"}
- Check if selected package manager is available
- Report any missing dependencies to user

Phase 3: Project Structure Creation
Goal: Create directory structure for CLI tool

Actions:
- Create project directory: !{bash mkdir -p "$ARGUMENTS"}
- For Python projects: !{bash mkdir -p "$ARGUMENTS/src/$ARGUMENTS" "$ARGUMENTS/tests"}
- For TypeScript projects: !{bash mkdir -p "$ARGUMENTS/src" "$ARGUMENTS/dist" "$ARGUMENTS/tests"}
- For Go projects: !{bash mkdir -p "$ARGUMENTS/cmd/$ARGUMENTS" "$ARGUMENTS/pkg"}
- For Rust projects: !{bash mkdir -p "$ARGUMENTS/src"}
- Create basic directory structure following language conventions

Phase 4: Generate Entry Point
Goal: Create main CLI entry point with framework setup

Actions:
- Generate appropriate entry point file based on language and framework:
  - Python: src/$ARGUMENTS/__main__.py or src/$ARGUMENTS/cli.py
  - TypeScript: src/index.ts or src/cli.ts
  - Go: cmd/$ARGUMENTS/main.go
  - Rust: src/main.rs
- Include proper shebang for interpreted languages
- Set up framework imports and basic command structure
- Create example command with help text
- Make entry point executable if needed

Phase 5: Package Configuration
Goal: Set up package manager configuration files

Actions:
- For Python: Create setup.py or pyproject.toml with entry_points
- For TypeScript: Create package.json with bin field
- For Go: Create go.mod with module path
- For Rust: Create Cargo.toml with [[bin]] section
- Include project metadata: name, version, description, author
- Add framework dependency
- Configure development dependencies (testing, linting)

Phase 6: Install Dependencies
Goal: Install required framework and dependencies

Actions:
- For Python: !{bash cd "$ARGUMENTS" && pip install -e .}
- For TypeScript: !{bash cd "$ARGUMENTS" && npm install}
- For Go: !{bash cd "$ARGUMENTS" && go mod tidy}
- For Rust: !{bash cd "$ARGUMENTS" && cargo build}
- Verify installation completed successfully
- Report any installation errors

Phase 7: Additional Files
Goal: Create README, LICENSE, and configuration files

Actions:
- Generate README.md with:
  - Project name and description
  - Installation instructions
  - Basic usage examples
  - Development setup
- Create LICENSE file (MIT by default)
- Add .gitignore for language-specific files
- Create basic test file demonstrating framework usage
- Add configuration files (.editorconfig, etc.)

Phase 8: Git Initialization
Goal: Initialize git repository with initial commit

Actions:
- Initialize git: !{bash cd "$ARGUMENTS" && git init}
- Stage all files: !{bash cd "$ARGUMENTS" && git add .}
- Create initial commit: !{bash cd "$ARGUMENTS" && git commit -m "Initial commit: CLI tool scaffold"}
- Report git repository location

Phase 9: Summary
Goal: Report what was created and next steps

Actions:
- Display project structure created
- Show entry point location and how to run tool
- List installed dependencies
- Provide next steps:
  - cd into project directory
  - Run the tool to verify it works
  - Start adding custom commands
  - Configure additional options
- Show example command to run the tool
