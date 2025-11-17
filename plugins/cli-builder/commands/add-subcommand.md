---
description: Add structured subcommands to CLI tool
argument-hint: <command-name> [command-2] [command-3] ...
allowed-tools: Task, AskUserQuestion, Bash, Read, Glob
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

Goal: Orchestrate adding one or multiple subcommands to a CLI tool, launching parallel agents for 3+ subcommands.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 subcommands
- Launches MULTIPLE agents IN PARALLEL for 3+ subcommands (all in ONE message)

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
Goal: Count how many subcommands to create

Actions:
- Parse $ARGUMENTS to extract subcommand names:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each subcommand name:
  - If count = 1: Single subcommand mode
  - If count = 2: Two subcommands mode
  - If count >= 3: **PARALLEL MODE** - multiple agents

Phase 3: Detect Existing CLI Framework
Goal: Identify the framework to match patterns

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
- Store detected framework

Phase 4: Gather Requirements (for all subcommands)
Goal: Collect specifications

Actions:
- For EACH subcommand name from Phase 2:
  - Ask user via AskUserQuestion:
    - Description/purpose
    - Required arguments
    - Optional flags
    - Validation needs
  - Store requirements for that subcommand

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 subcommands = single/sequential agents, 3+ subcommands = PARALLEL agents**

**For 1-2 Subcommands:**

Task(
  description="Add subcommand to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add subcommand '{name}' to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Subcommand: {name}
Description: {description}
Arguments: {arguments}
Flags: {flags}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Generate code, integrate it, test syntax.

Deliverable: Working subcommand integrated into CLI"
)

**For 3+ Subcommands - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add subcommand 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add subcommand '{name_1}'.
Framework: {framework}
Description: {desc_1}
Arguments: {args_1}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Subcommand 1 code")

Task(description="Add subcommand 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add subcommand '{name_2}'.
Framework: {framework}
Description: {desc_2}
Arguments: {args_2}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Subcommand 2 code")

Task(description="Add subcommand 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add subcommand '{name_3}'.
Framework: {framework}
Description: {desc_3}
Arguments: {args_3}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Subcommand 3 code")

[Continue for all N subcommands...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all subcommands were added

Actions:
- For each subcommand:
  - Verify code was generated
  - Check syntax if possible
  - Test help output
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Subcommands added: {count}
  - Framework: {framework}
  - Files modified/created
- Show usage examples for each subcommand
- Suggest next steps:
  - Test each subcommand
  - Add interactive prompts: /cli-tool-builder:add-interactive
  - Add output formatting: /cli-tool-builder:add-output-formatting
  - Add validation: /cli-tool-builder:add-args-parser
