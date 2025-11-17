---
description: Setup distribution packaging (npm, PyPI, Homebrew)
argument-hint: [platform] [platform-2] [platform-3] ...
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

Goal: Orchestrate setting up distribution packaging for CLI tool, launching parallel agents for 3+ platforms.

**Architectural Context:**

This command is an **orchestrator** that:
- Detects the CLI framework
- Gathers requirements
- Launches 1 agent for 1-2 distribution platforms
- Launches MULTIPLE agents IN PARALLEL for 3+ platforms (all in ONE message)

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
Goal: Count how many distribution platforms to configure

Actions:
- Parse $ARGUMENTS to extract platforms:
  !{bash echo "$ARGUMENTS" | wc -w}
- Store count
- Extract each platform:
  - If count = 0: Ask user for platform preference
  - If count = 1: Single platform mode
  - If count = 2: Two platforms mode
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

Phase 4: Gather Requirements (for all platforms)
Goal: Collect specifications

Actions:
- If no platforms in $ARGUMENTS:
  - Ask user via AskUserQuestion:
    - Which distribution platforms? (npm, pypi, homebrew, binary, cargo, go-install)
    - CLI tool name?
    - Current version? (default: 0.1.0)
    - GitHub repository URL? (for releases)
    - Automated releases via GitHub Actions?
- For EACH platform from Phase 2:
  - Store platform type (npm, pypi, homebrew, binary, cargo, go-install)
  - Determine version management approach
  - Plan release automation

Phase 5: Launch Agent(s) for Implementation
Goal: Delegate to cli-feature-impl agent(s)

Actions:

**Decision: 1-2 platforms = single/sequential agents, 3+ platforms = PARALLEL agents**

**For 1-2 Distribution Platforms:**

Task(
  description="Add package distribution to CLI",
  subagent_type="cli-tool-builder:cli-feature-impl",
  prompt="You are cli-feature-impl. Add distribution packaging to the CLI.

Framework: {detected_framework}
Language: {detected_language}

Distribution Platforms: {platforms}
Requirements:
- Platforms: {npm/pypi/homebrew/binary/cargo/go-install}
- CLI tool name: {tool_name}
- Version: {version}
- GitHub repo: {github_url}
- Automated releases: {yes/no}
- Version management: {standard-version/bump2version/goreleaser}

Use Skill(cli-tool-builder:{framework}-patterns) for patterns.
Generate package configuration, release workflows, installation docs.

Deliverable: Working package distribution setup for CLI"
)

**For 3+ Distribution Platforms - CRITICAL: Send ALL Task() calls in ONE MESSAGE:**

Task(description="Add platform 1", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add distribution packaging for '{platform_1}'.
Framework: {framework}
Language: {language}
Platform: {platform_1}
Tool name: {tool_name}
Version: {version}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Package config for {platform_1}")

Task(description="Add platform 2", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add distribution packaging for '{platform_2}'.
Framework: {framework}
Language: {language}
Platform: {platform_2}
Tool name: {tool_name}
Version: {version}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Package config for {platform_2}")

Task(description="Add platform 3", subagent_type="cli-tool-builder:cli-feature-impl", prompt="Add distribution packaging for '{platform_3}'.
Framework: {framework}
Language: {language}
Platform: {platform_3}
Tool name: {tool_name}
Version: {version}
Use Skill(cli-tool-builder:{framework}-patterns).
Deliverable: Package config for {platform_3}")

[Continue for all N platforms...]

**DO NOT wait between Task() calls - send them ALL at once!**

Agents run in parallel. Proceed to Phase 6 only after ALL complete.

Phase 6: Verification
Goal: Confirm all platforms were configured

Actions:
- For each platform:
  - Verify package configuration was generated
  - Check syntax if possible
  - Test build process (if applicable)
  - Verify version management works
- Test release workflow (dry-run if applicable)
- Verify installation documentation complete
- Report any failures

Phase 7: Summary
Goal: Report results and next steps

Actions:
- Display summary:
  - Platforms configured: {count}
  - Framework: {framework}
  - Tool name: {tool_name}
  - Version: {version}
  - Files modified/created
  - Release automation configured
- Show installation commands for each platform:
  - npm: npm install -g {tool_name}
  - PyPI: pip install {tool_name}
  - Homebrew: brew install {user}/{tap}/{tool_name}
  - Binary: Download and install instructions
  - Cargo: cargo install {tool_name}
  - Go: go install github.com/{user}/{tool_name}@latest
- Suggest next steps:
  - Test package installation locally
  - Create initial release tag
  - Update documentation with badges
  - Set up CI/CD secrets for automated publishing
  - Test version bumping workflow
  - Create CHANGELOG.md
