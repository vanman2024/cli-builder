---
description: Add configuration file management (JSON, YAML, TOML, env)
argument-hint: [config-type] [config-type-2] [config-type-3] ...
allowed-tools: Task, AskUserQuestion, Bash, Read, Glob
---

**Arguments**: $ARGUMENTS

Goal: Orchestrate adding configuration file support to CLI tool, launching parallel agents for 3+ config types.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 config types
- Launches MULTIPLE agents IN PARALLEL for 3+ config types (all in ONE message)

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
Goal: Count how many config types to implement

Actions:
- Parse $ARGUMENTS to extract config types:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each config type:
  - If count = 0: Ask user for config type preference
  - If count = 1: Single config type mode
  - If count = 2: Two config types mode
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

Phase 4: Gather Requirements (for all config types)
Goal: Collect specifications

Actions:
- If no config types in $ARGUMENTS:
  - Ask user via AskUserQuestion:
    - Which config formats? (JSON, YAML, TOML, env, rc)
    - Config locations preference? (~/.config/toolname or .toolnamerc)
    - Which settings should be configurable?
    - Support environment variable overrides?
    - Need config validation schemas?
    - Interactive config wizard desired?
- For EACH config type from Phase 2:
  - Store config type (json, yaml, toml, env, rc)
  - Determine priority in cascading config system
  - Plan validation approach

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 config types = single/sequential agents, 3+ config types = PARALLEL agents**

**For 1-2 Config Types:**

Task(
  description="Add config support to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add configuration file support to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Config Type: {config_type}
Requirements:
- Config format: {format (json/yaml/toml/env)}
- Config locations: {locations}
- Cascading priority: CLI flags > env vars > project config > user config > system config > defaults
- Environment variable overrides: {yes/no}
- Validation: {validation_approach}
- Interactive wizard: {yes/no}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Generate config loader, validation, example files.

Deliverable: Working configuration system integrated into CLI"
)

**For 3+ Config Types - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add config type 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add config support for '{type_1}'.
Framework: {framework}
Config format: {format_1}
Priority level: {priority_1}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Config loader for {type_1}")

Task(description="Add config type 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add config support for '{type_2}'.
Framework: {framework}
Config format: {format_2}
Priority level: {priority_2}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Config loader for {type_2}")

Task(description="Add config type 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add config support for '{type_3}'.
Framework: {framework}
Config format: {format_3}
Priority level: {priority_3}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Config loader for {type_3}")

[Continue for all N config types...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all config types were added

Actions:
- For each config type:
  - Verify config loader code was generated
  - Check syntax if possible
  - Test config loading from different locations
  - Verify environment variable overrides work
- Test cascading priority (CLI flags > env > project > user > system > defaults)
- Verify validation works for malformed configs
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Config types added: {count}
  - Framework: {framework}
  - Files modified/created
  - Config locations supported
  - Cascading priority order
- Show usage examples:
  - Creating config file
  - Environment variable naming
  - Interactive wizard (if added)
- Suggest next steps:
  - Add config options to CLI flags
  - Implement config validation tests
  - Document config options in --help output
  - Add config file templates to repo
