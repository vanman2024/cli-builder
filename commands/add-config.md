---
description: Add configuration file management (JSON, YAML, TOML, env)
argument-hint: [config-type]
allowed-tools: AskUserQuestion, Bash, Read, Write, Edit
---

**Arguments**: $ARGUMENTS

Goal: Add comprehensive configuration file management to CLI tool with support for multiple formats, environment variables, validation, and user-friendly defaults.

Core Principles:
- Detect language and adapt code generation accordingly
- Support multiple config formats and locations
- Provide sensible defaults with clear override paths
- Include validation and error handling

Phase 1: Discovery
Goal: Understand project context and configuration needs

Actions:
- Parse $ARGUMENTS for config type preference (json, yaml, toml, env, rc)
- Detect project language and structure
- Example: !{bash ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null}
- Check existing config files to avoid conflicts
- Example: !{bash ls .env* config.* *.config.js 2>/dev/null}

Phase 2: Requirements Gathering
Goal: Clarify configuration needs and preferences

Actions:
- Use AskUserQuestion to determine:
  - Config file format preference (if not in $ARGUMENTS)
  - Config locations (user prefers ~/.config/toolname or .toolnamerc?)
  - Which settings should be configurable?
  - Should it support environment variable overrides?
  - Need for config validation schemas?
  - Interactive config wizard desired?

Phase 3: Analysis
Goal: Determine implementation approach based on language

Actions:
- Identify project language from discovery phase
- Map config format to appropriate library:
  - Python: json (stdlib), yaml (pyyaml), toml (tomli/tomllib), env (python-dotenv)
  - JavaScript/TypeScript: json (fs), yaml (js-yaml), toml (toml), env (dotenv)
  - Go: json (encoding/json), yaml (gopkg.in/yaml.v3), toml (BurntSushi/toml), env (godotenv)
  - Rust: json (serde_json), yaml (serde_yaml), toml (toml), env (dotenv)
- Determine config loading strategy (cascading priorities)
- Plan directory structure for config files

Phase 4: Code Generation
Goal: Generate configuration management code

Actions:
- Create config module/package structure appropriate for language
- Generate config schema/struct definition with common CLI settings:
  - verbosity/log level
  - output format
  - default paths
  - API endpoints (if applicable)
  - timeout values
- Implement config loader with cascading priority:
  1. Command-line flags (highest priority)
  2. Environment variables
  3. Project-level config (.toolnamerc in current dir)
  4. User-level config (~/.config/toolname/config.format)
  5. System-level config (/etc/toolname/config.format)
  6. Built-in defaults (lowest priority)
- Add validation logic with helpful error messages
- Include config file generation/initialization function

Phase 5: Config File Templates
Goal: Create example config files and documentation

Actions:
- Generate example config file with all available options documented
- Create .gitignore entries for sensitive config files
- Add environment variable template (.env.example)
- Document config precedence in README or docs
- Create config initialization command helper

Phase 6: Interactive Wizard (Optional)
Goal: Add user-friendly config setup experience

Actions:
- If user requested wizard, generate interactive setup:
  - Prompt for each config option with defaults
  - Validate inputs in real-time
  - Save to chosen location
  - Display summary of configuration
- Make wizard accessible via CLI flag (e.g., --init-config)

Phase 7: Testing & Validation
Goal: Verify config system works correctly

Actions:
- Test config loading from different locations
- Verify environment variable overrides work
- Validate error handling for malformed config files
- Check that defaults apply correctly
- Example: !{bash cat test-config.json | python -m json.tool}

Phase 8: Summary
Goal: Document what was added

Actions:
- Summarize configuration system features:
  - Supported config formats
  - Config file locations and precedence
  - Environment variable naming conventions
  - Validation rules applied
- List files created/modified:
  - Config loader module
  - Example config files
  - Documentation updates
- Provide usage examples:
  - How to create config file
  - How to override with env vars
  - How to run interactive setup
- Suggest next steps:
  - Add config options to CLI flags
  - Implement config validation tests
  - Document config options in --help output
