---
description: Add advanced argument parsing capabilities
argument-hint: [feature] [feature-2] [feature-3] ...
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

Goal: Orchestrate adding argument parsing features to CLI tool, launching parallel agents for 3+ parsing features.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 parsing features
- Launches MULTIPLE agents IN PARALLEL for 3+ parsing features (all in ONE message)

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
Goal: Count how many parsing features to implement

Actions:
- Parse $ARGUMENTS to extract parsing features:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each parsing feature:
  - If count = 0: Ask user for feature preferences
  - If count = 1: Single feature mode
  - If count = 2: Two features mode
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

Phase 4: Gather Requirements (for all parsing features)
Goal: Collect specifications

Actions:
- If no features in $ARGUMENTS:
  - Ask user via AskUserQuestion:
    - Which parsing features? (positional-args, flags, options, type-coercion, validators, mutually-exclusive, environment-vars)
    - Type validation needed? (string, int, float, file, url, email, enum)
    - Advanced features? (subcommands, variadic args, dependent options)
    - Help generation preferences?
- For EACH feature from Phase 2:
  - Store feature type
  - Determine validation requirements
  - Plan integration approach

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 features = single/sequential agents, 3+ features = PARALLEL agents**

**For 1-2 Parsing Features:**

Task(
  description="Add argument parsing to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add comprehensive argument parsing to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Parsing Features: {features}
Requirements:
- Positional arguments: {yes/no}
- Options/Flags: {short/long forms}
- Type coercion: {types (string, int, float, file, url, email, enum)}
- Validators: {validation_requirements}
- Advanced features: {mutually-exclusive, dependent-options, variadic, env-vars}
- Help generation: {auto-generate with examples}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Generate argument parsing code, validators, help text.

Deliverable: Working argument parsing integrated into CLI"
)

**For 3+ Parsing Features - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add parsing feature 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add argument parsing feature '{feature_1}'.
Framework: {framework}
Language: {language}
Feature type: {feature_1}
Validation: {validation_1}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Argument parsing code for {feature_1}")

Task(description="Add parsing feature 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add argument parsing feature '{feature_2}'.
Framework: {framework}
Language: {language}
Feature type: {feature_2}
Validation: {validation_2}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Argument parsing code for {feature_2}")

Task(description="Add parsing feature 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add argument parsing feature '{feature_3}'.
Framework: {framework}
Language: {language}
Feature type: {feature_3}
Validation: {validation_3}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Argument parsing code for {feature_3}")

[Continue for all N parsing features...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all parsing features were added

Actions:
- For each parsing feature:
  - Verify parsing code was generated
  - Check syntax if possible
  - Test with valid arguments
  - Test validation with invalid inputs
- Verify mutually exclusive options work (if applicable)
- Test environment variable fallbacks (if added)
- Test help generation
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Parsing features added: {count}
  - Framework: {framework}
  - Files modified/created
  - Validators included
  - Advanced features enabled
- Show usage examples:
  - Positional arguments
  - Options and flags
  - Type validation
  - Help command output
- Suggest next steps:
  - Add more validators
  - Implement command aliases
  - Add bash/zsh completion
  - Document all arguments in README
