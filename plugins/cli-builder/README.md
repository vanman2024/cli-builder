# CLI Tool Builder Plugin

A comprehensive plugin for building professional CLI tools with best practices

## Overview

This plugin enables rapid development of command-line interfaces with industry best practices built-in.

## Features

- 🚀 Quick CLI project initialization
- 📦 Multiple framework support (Click, Typer, Commander.js, yargs, etc.)
- 🎨 Rich terminal output (colors, tables, spinners)
- ⚙️ Configuration management (JSON, YAML, TOML, .env)
- 🤖 Interactive prompts and wizards
- 📝 Argument parsing and validation
- 🧪 Testing patterns and examples
- 📦 Distribution setup (npm, PyPI, Homebrew)

## Installation

Install this plugin from a marketplace or local directory:

```bash
/plugin install cli-tool-builder
```

## Available Commands

### `/cli-tool-builder:new-cli [tool-name]`
Initialize a new CLI tool project with framework selection

### `/cli-tool-builder:add-subcommand [command-name]`
Add structured subcommands to your CLI

### `/cli-tool-builder:add-config [config-type]`
Add configuration file management (JSON, YAML, TOML, env)

### `/cli-tool-builder:add-interactive`
Add interactive prompts and menus

### `/cli-tool-builder:add-args-parser`
Add advanced argument parsing

### `/cli-tool-builder:add-output-formatting`
Add rich terminal output (colors, tables, progress bars)

### `/cli-tool-builder:add-package [type]`
Setup distribution packaging (npm, PyPI, Homebrew)

## Supported Frameworks

### Python
- Click - Popular decorator-based framework
- Typer - Modern type-hint based framework
- argparse - Built-in Python standard library
- Fire - Auto-generate CLI from Python code

### Node.js/TypeScript
- Commander.js - Simple and elegant
- yargs - Advanced argument parsing
- oclif - Enterprise CLI framework
- gluegun - CLI with generators

### Go
- Cobra - Production-ready (used by kubectl, hugo)
- cli - Lightweight and fast

### Rust
- clap - Full-featured with derive macros

## Quick Start

```bash
# Create a new CLI tool
/cli-tool-builder:new-cli my-deploy-tool

# Add deployment subcommand
/cli-tool-builder:add-subcommand deploy

# Add interactive wizard
/cli-tool-builder:add-interactive

# Add rich output formatting
/cli-tool-builder:add-output-formatting

# Package for distribution
/cli-tool-builder:add-package npm
```

## Documentation

See the [design document](docs/CLI-TOOL-BUILDER-PLUGIN-DESIGN.md) for complete details.

## License

MIT
