---
description: Add rich terminal output (colors, tables, spinners)
argument-hint: [format-type] [format-type-2] [format-type-3] ...
allowed-tools: Task, AskUserQuestion, Bash, Read, Glob
---

**Arguments**: $ARGUMENTS

Goal: Orchestrate adding output formatting capabilities to CLI tool, launching parallel agents for 3+ format types.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 format types
- Launches MULTIPLE agents IN PARALLEL for 3+ format types (all in ONE message)

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
Goal: Count how many output format types to implement

Actions:
- Parse $ARGUMENTS to extract format types:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each format type:
  - If count = 0: Ask user for format type preference
  - If count = 1: Single format type mode
  - If count = 2: Two format types mode
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

Phase 4: Gather Requirements (for all format types)
Goal: Collect specifications

Actions:
- If no format types in $ARGUMENTS:
  - Ask user via AskUserQuestion:
    - Which format types? (colors, tables, spinners, progress-bars, boxes, icons, panels, syntax-highlighting)
    - Cross-platform support needed?
    - Unicode or ASCII output?
    - Specific styling preferences?
- For EACH format type from Phase 2:
  - Store format type (colors, tables, spinners, progress-bars, boxes, icons, panels, syntax-highlighting)
  - Determine library requirements
  - Plan styling approach

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 format types = single/sequential agents, 3+ format types = PARALLEL agents**

**For 1-2 Format Types:**

Task(
  description="Add output formatting to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add rich output formatting to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Format Types: {format_types}
Requirements:
- Libraries: {chalk/ora/cli-table3 for Node.js, rich/colorama/tqdm for Python}
- Format types: {colors/tables/spinners/progress-bars/boxes/icons/panels/syntax-highlighting}
- Cross-platform: {yes/no}
- Unicode or ASCII: {unicode/ascii/both}
- Styling: {styling_preferences}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Generate output formatting utilities, examples, documentation.

Deliverable: Working output formatting integrated into CLI"
)

**For 3+ Format Types - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add format type 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add output formatting for '{type_1}'.
Framework: {framework}
Language: {language}
Format type: {type_1}
Library: {library_1}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Output formatting code for {type_1}")

Task(description="Add format type 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add output formatting for '{type_2}'.
Framework: {framework}
Language: {language}
Format type: {type_2}
Library: {library_2}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Output formatting code for {type_2}")

Task(description="Add format type 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add output formatting for '{type_3}'.
Framework: {framework}
Language: {language}
Format type: {type_3}
Library: {library_3}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Output formatting code for {type_3}")

[Continue for all N format types...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all format types were added

Actions:
- For each format type:
  - Verify formatting code was generated
  - Check syntax if possible
  - Test output rendering
  - Verify cross-platform compatibility (if required)
- Test combined formatting (colors + tables, spinners + progress, etc.)
- Verify library dependencies installed
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Format types added: {count}
  - Framework: {framework}
  - Libraries installed: {libraries with versions}
  - Files modified/created
  - Unicode/ASCII support
- Show usage examples:
  - Colored output
  - Table formatting
  - Spinners and progress bars
  - Boxed messages
  - Icons and symbols
- Suggest next steps:
  - Create output utility module
  - Add formatting to existing commands
  - Implement log levels with colors
  - Add terminal width detection
  - Support NO_COLOR environment variable
