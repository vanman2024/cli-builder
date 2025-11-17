---
description: Initialize new CLI tool project with framework selection
argument-hint: <tool-name>
allowed-tools: Task, AskUserQuestion, Bash, Read
---

---
🚨 **EXECUTION NOTICE FOR CLAUDE**

When you invoke this command via SlashCommand, the system returns THESE INSTRUCTIONS below.

**YOU are the executor. This is NOT an autonomous subprocess.**

- ✅ The phases below are YOUR execution checklist
- ✅ YOU must run each phase immediately using tools (Bash, Read, Write, Edit, TodoWrite)
- ✅ Complete ALL phases before considering this command done
- ❌ DON't wait for "the command to complete" - YOU complete it by executing the phases
- ❌ DON't treat this as status output - it IS your instruction set

**Immediately after SlashCommand returns, start executing Phase 0, then Phase 1, etc.**

See `@CLAUDE.md` section "SlashCommand Execution - YOU Are The Executor" for detailed explanation.

---


**Arguments**: $ARGUMENTS

Goal: Orchestrate CLI project initialization by gathering requirements and delegating to the cli-setup agent for implementation.

**Architectural Context:**

This command follows the composition pattern:
- **Commands are orchestrators** - They ask questions and delegate
- **Agents are workers** - They do the complex implementation
- Commands invoke agents via Task tool, not implement directly

Phase 1: Load Architectural Framework
Goal: Understand component composition patterns

Actions:
- Load the complete component decision framework:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- This provides critical understanding of:
  - Commands are the primitive (orchestrators)
  - Agents are for complex multi-step workflows
  - Proper composition: Command → Agent → Skills
  - When to delegate vs when to execute directly

Phase 2: Gather Requirements
Goal: Collect user preferences for the CLI project

Actions:
- Parse $ARGUMENTS for tool name
- If no tool name provided, ask user for it via AskUserQuestion
- Ask user for language preference:
  - Options: TypeScript, Python, Go, Rust
  - Include descriptions of each language's strengths
- Based on language selection, ask for framework:
  - **Python**: Click (decorator-based), Typer (type-safe), argparse (stdlib), Fire (auto-generate)
  - **TypeScript/Node.js**: Commander.js (simple), yargs (advanced), oclif (enterprise), gluegun (generators)
  - **Go**: Cobra (production), cli (lightweight)
  - **Rust**: clap (full-featured)
- Ask for package manager preference:
  - Python: pip, poetry, pipenv
  - Node.js: npm, yarn, pnpm
  - Go: go modules (automatic)
  - Rust: cargo (automatic)

Phase 3: Environment Validation
Goal: Verify required tools are available

Actions:
- Check if selected language runtime is installed:
  - Python: !{bash python3 --version 2>/dev/null || echo "Not found"}
  - Node.js: !{bash node --version 2>/dev/null || echo "Not found"}
  - Go: !{bash go version 2>/dev/null || echo "Not found"}
  - Rust: !{bash rustc --version 2>/dev/null || echo "Not found"}
- Check if selected package manager is available
- If any tools missing, inform user and provide installation instructions
- If critical tools missing, stop and ask user to install them first

Phase 4: Delegate to CLI Setup Agent
Goal: Hand off implementation to specialized agent

Actions:

**Invoke the cli-setup agent to perform the actual implementation:**

Task(
  description="Initialize CLI project with chosen framework",
  subagent_type="cli-tool-builder:cli-setup",
  prompt="You are the cli-setup agent. Initialize a new CLI tool project with the specifications provided.

**Project Details:**
- Tool Name: {tool_name from Phase 2}
- Language: {language from Phase 2}
- Framework: {framework from Phase 2}
- Package Manager: {package_manager from Phase 2}

**User Requirements:**
Create a complete CLI tool project with:
1. Proper directory structure for the chosen framework
2. Entry point file with correct shebang
3. Package configuration (package.json, setup.py, Cargo.toml, or go.mod)
4. Executable bin/entry point configuration
5. Dependencies installation for chosen framework
6. Basic command structure following framework conventions
7. README with usage instructions
8. LICENSE file (MIT)
9. .gitignore for the language
10. Git repository initialization

**Skills Available:**
- Use Skill(cli-tool-builder:{framework}-patterns) for framework-specific patterns
- Example: Skill(cli-tool-builder:click-patterns) for Python Click
- Example: Skill(cli-tool-builder:commander-patterns) for Commander.js

**Implementation:**
Follow the phased approach in your agent definition:
1. Discovery: Confirm requirements
2. Analysis: Determine exact dependencies and structure
3. Planning: Design directory layout and files
4. Implementation: Create all files and install dependencies
5. Verification: Test that CLI works and passes validation

Deliverable: Complete working CLI project in ./{tool_name}/ directory"
)

Wait for agent to complete. Agent will use framework-specific skills and create the complete project.

Phase 5: Verification
Goal: Confirm project was created successfully

Actions:
- Check that project directory exists: !{bash ls -la {tool_name}/}
- Verify key files were created:
  - Entry point file
  - Package configuration
  - README
  - LICENSE
  - .gitignore
- Display project structure to user

Phase 6: Summary
Goal: Report success and provide next steps

Actions:
- Display project creation summary:
  - Tool name
  - Language and framework
  - Project location
  - Entry point file
- Show next steps:
  1. cd {tool_name}
  2. Test CLI: ./{tool_name} --help (or appropriate command)
  3. Add subcommands: /cli-tool-builder:add-subcommand <command-name>
  4. Add features: /cli-tool-builder:add-interactive, /cli-tool-builder:add-output-formatting
  5. Package for distribution: /cli-tool-builder:add-package
- Encourage user to explore the generated code and customize it
