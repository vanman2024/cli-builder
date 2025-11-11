---
description: Add interactive prompts and menus
argument-hint: [prompt-type] [prompt-type-2] [prompt-type-3] ...
allowed-tools: Task, AskUserQuestion, Bash, Read, Glob
---

**Arguments**: $ARGUMENTS

Goal: Orchestrate adding interactive prompt capabilities to CLI tool, launching parallel agents for 3+ prompt types.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 prompt types
- Launches MULTIPLE agents IN PARALLEL for 3+ prompt types (all in ONE message)

Phase 1: Load Architectural Framework
Goal: Understand composition and parallelization patterns

Actions:
- Load component decision framework:
  !{Read ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/docs/frameworks/claude/reference/component-decision-framework.md}
- Key patterns:
  - Commands orchestrate, agents implement
  - For 3+ items: Launch multiple agents in PARALLEL
  - Send ALL Task() calls in SINGLE message
  - Agents run concurrently for faster execution

Phase 2: Parse Arguments & Determine Mode
Goal: Count how many prompt types to implement

Actions:
- Parse $ARGUMENTS to extract prompt types:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each prompt type:
  - If count = 0: Ask user for prompt type preference
  - If count = 1: Single prompt type mode
  - If count = 2: Two prompt types mode
  - If count >= 3: **PARALLEL MODE** - multiple agents

Phase 3: Detect Existing CLI Framework
Goal: Identify the framework and language

Actions:
- Check for language indicators:
  - !{bash ls -1 package.json setup.py pyproject.toml go.mod Cargo.toml 2>/dev/null | head -1}
- For Node.js (package.json found):
  - !{bash grep -E '"(commander|yargs|oclif|gluegun)"' package.json 2>/dev/null | head -1}
- For Python files:
  - !{bash grep -r "import click\|import typer\|import argparse\|import fire" . --include="*.py" 2>/dev/null | head -1}
- For Go:
  - !{bash grep -r "github.com/spf13/cobra\|github.com/urfave/cli" . --include="*.go" 2>/dev/null | head -1}
- For Rust:
  - !{bash grep "clap" Cargo.toml 2>/dev/null}
- Store detected framework and language

Phase 4: Gather Requirements (for all prompt types)
Goal: Collect specifications

Actions:
- If no prompt types in $ARGUMENTS:
  - Ask user via AskUserQuestion:
    - Which prompt types? (text, select, checkbox, password, confirm, number, editor, path)
    - Interactive wizard needed?
    - Validation patterns required?
    - Conditional logic needed?
- For EACH prompt type from Phase 2:
  - Store prompt type (text, select, checkbox, password, confirm, number, editor, path)
  - Determine validation requirements
  - Plan conditional logic (if applicable)

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 prompt types = single/sequential agents, 3+ prompt types = PARALLEL agents**

**For 1-2 Prompt Types:**

Task(
  description="Add interactive prompts to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add interactive prompt capabilities to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Prompt Type: {prompt_type}
Requirements:
- Library to use: {inquirer for Node.js, questionary for Python}
- Prompt type: {text/select/checkbox/password/confirm/number/editor/path}
- Validation: {validation_requirements}
- Conditional logic: {yes/no}
- Interactive wizard: {yes/no}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Use Skill(cli-tool-builder:inquirer-patterns) for interactive prompt patterns.
Generate prompt code, validation, example files.

Deliverable: Working interactive prompts integrated into CLI"
)

**For 3+ Prompt Types - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add prompt type 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add interactive prompt for '{type_1}'.
Framework: {framework}
Language: {language}
Prompt type: {type_1}
Validation: {validation_1}
Use Skill(cli-tool-builder:inquirer-patterns).
Deliverable: Interactive prompt code for {type_1}")

Task(description="Add prompt type 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add interactive prompt for '{type_2}'.
Framework: {framework}
Language: {language}
Prompt type: {type_2}
Validation: {validation_2}
Use Skill(cli-tool-builder:inquirer-patterns).
Deliverable: Interactive prompt code for {type_2}")

Task(description="Add prompt type 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add interactive prompt for '{type_3}'.
Framework: {framework}
Language: {language}
Prompt type: {type_3}
Validation: {validation_3}
Use Skill(cli-tool-builder:inquirer-patterns).
Deliverable: Interactive prompt code for {type_3}")

[Continue for all N prompt types...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all prompt types were added

Actions:
- For each prompt type:
  - Verify prompt code was generated
  - Check syntax if possible
  - Test prompt with valid inputs
  - Test validation with invalid inputs
- Verify conditional logic works (if applicable)
- Test interactive wizard flow (if added)
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Prompt types added: {count}
  - Framework: {framework}
  - Library installed: {inquirer/questionary}
  - Files modified/created
  - Validation patterns included
- Show usage examples:
  - Running interactive prompts
  - Validation patterns
  - Conditional logic examples
- Suggest next steps:
  - Integrate prompts into subcommands
  - Add keyboard shortcuts
  - Implement multi-step wizards
  - Add accessibility features
