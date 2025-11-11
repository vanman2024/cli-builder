---
description: Setup distribution packaging (npm, PyPI, Homebrew)
argument-hint: [type]
allowed-tools: AskUserQuestion, Bash, Read, Write, Edit
---

**Arguments**: $ARGUMENTS

Goal: Configure distribution packaging for CLI tool with version management, installation docs, and release automation.

Core Principles:
- Detect project type to suggest appropriate platforms
- Support multiple distribution channels
- Include version management and changelog
- Set up automated releases

Phase 1: Discovery
Goal: Understand project structure and determine packaging platform

Actions:
- Parse $ARGUMENTS for distribution type (npm, pypi, homebrew, binary, all)
- Detect project type from existing files
- Example: !{bash ls package.json setup.py pyproject.toml Cargo.toml go.mod 2>/dev/null}
- If project type detected, load main configuration file
- Example: @package.json or @pyproject.toml

Phase 2: Platform Selection
Goal: Confirm packaging platform(s) with user

Actions:
- If $ARGUMENTS specifies platform, use that
- Otherwise, use AskUserQuestion to ask:
  - Which distribution platform(s)? (npm, PyPI, Homebrew, Binary, Multiple)
  - What is your CLI tool name?
  - Current version? (default: 0.1.0)
  - GitHub repository URL? (for Homebrew formula and releases)

Phase 3: NPM Configuration
Goal: Set up npm packaging if selected

Actions:
- Update or create package.json with:
  - "bin" field pointing to CLI entry point
  - "files" array for distribution files
  - "prepublishOnly" script for build validation
  - Keywords for discoverability
- Create or update .npmignore to exclude dev files
- Add publish documentation to README or PUBLISH.md
- Example: !{bash npm pkg set bin.{CLI_NAME}="./bin/cli.js"}

Phase 4: PyPI Configuration
Goal: Set up PyPI packaging if selected

Actions:
- Create or update pyproject.toml with:
  - [project] section with metadata
  - [project.scripts] entry point
  - [build-system] with hatchling or setuptools
  - Classifiers for Python versions and OS
- Create MANIFEST.in if needed for data files
- Add twine to dev dependencies
- Create or update .pypirc template (without credentials)
- Add publish documentation

Phase 5: Homebrew Formula
Goal: Generate Homebrew formula template if selected

Actions:
- Create formula directory: !{bash mkdir -p Formula}
- Generate Ruby formula template with:
  - url pointing to GitHub release tarball
  - sha256 placeholder (filled on release)
  - install instructions for bin file
  - test block with version check
- Add instructions for tap creation
- Document formula update process

Phase 6: Binary Packaging
Goal: Set up binary compilation if selected

Actions:
- For Node.js: Configure pkg with targets
- For Python: Set up PyInstaller with spec file
- For Go: Create goreleaser.yaml config
- For Rust: Update Cargo.toml with release profile
- Add build scripts for each platform (linux, mac, windows)
- Configure output directory structure

Phase 7: Version Management
Goal: Add version bumping and changelog generation

Actions:
- Install version management tool based on platform:
  - npm: Use npm version command
  - Python: Create bump_version.py script
  - Universal: Add standard-version or release-it
- Create CHANGELOG.md if not exists
- Add git hooks for version tags
- Example: !{bash npm install --save-dev standard-version}

Phase 8: Release Automation
Goal: Set up GitHub Actions for automated releases

Actions:
- Create .github/workflows/release.yml with:
  - Trigger on version tags (v*)
  - Build step for all platforms
  - Checksum generation
  - GitHub Release creation
  - Platform-specific publishing (npm, PyPI)
  - Homebrew formula update (if applicable)
- Add release preparation checklist
- Create RELEASING.md with step-by-step guide

Phase 9: Installation Documentation
Goal: Create clear installation instructions

Actions:
- Add installation section to README.md with:
  - npm: npm install -g {CLI_NAME}
  - PyPI: pip install {CLI_NAME}
  - Homebrew: brew install {USER}/{TAP}/{CLI_NAME}
  - Binary: Download and install instructions
  - Building from source
- Add version check command: {CLI_NAME} --version
- Include troubleshooting common issues
- Add uninstall instructions

Phase 10: Summary
Goal: Report configured packaging and next steps

Actions:
- List all configured distribution platforms
- Show version management commands
- Display release workflow overview
- Provide next steps:
  - Test package installation locally
  - Create initial release
  - Update documentation with badge links
  - Set up CI/CD secrets if publishing automatically
