---
description: Add rich terminal output (colors, tables, spinners)
argument-hint: none
allowed-tools: Bash(*), Read(*), Write, Edit
---

**Arguments**: $ARGUMENTS

Goal: Add rich terminal output formatting capabilities including colors, tables, progress bars, spinners, and icons to CLI tool projects.

Core Principles:
- Detect language and use appropriate libraries
- Generate comprehensive examples for all formatting types
- Install dependencies automatically
- Create utility modules with ready-to-use functions
- Provide clear documentation

Phase 1: Discovery
Goal: Detect project language and current structure

Actions:
- Detect project type by checking for language-specific files
- Check for package.json (Node.js) or pyproject.toml/setup.py (Python)
- Example: !{bash ls package.json pyproject.toml setup.py 2>/dev/null | head -1}
- Identify project structure to determine where to place output utilities

Phase 2: Installation
Goal: Install appropriate formatting libraries based on detected language

Actions:
- For Node.js projects:
  - Install chalk (terminal colors)
  - Install ora (elegant spinners)
  - Install cli-table3 (ASCII/unicode tables)
  - Install boxen (box drawing)
  - Install log-symbols (colored symbols)
  - Example: !{bash npm install chalk ora cli-table3 boxen log-symbols --save}

- For Python projects:
  - Install colorama (cross-platform terminal colors)
  - Install rich (rich terminal output with tables, progress bars, syntax highlighting)
  - Install tqdm (progress bars)
  - Install tabulate (table formatting)
  - Example: !{bash pip install colorama rich tqdm tabulate}

Phase 3: Generate Utilities
Goal: Create output formatting utility module with examples

Actions:
- For Node.js: Create src/utils/output.js or lib/output.js with:
  - Color functions (success, error, warning, info)
  - Spinner helpers for async operations
  - Table formatting (ASCII and unicode)
  - Box drawing for important messages
  - Symbol utilities (✓, ✖, ⚠, ℹ)

- For Python: Create src/utils/output.py or lib/output.py with:
  - Colorama-based color functions
  - Rich console for advanced formatting
  - Progress bar utilities using tqdm
  - Table formatting with tabulate
  - Status symbols

Phase 4: Generate Examples
Goal: Create comprehensive example file demonstrating all formatting capabilities

Actions:
- For Node.js: Create examples/output-demo.js with:
  - Colored output examples (success, error, warning, info)
  - Spinner demonstration for async operations
  - Table formatting (both ASCII and unicode styles)
  - Boxed messages for highlighting
  - Icon/symbol usage

- For Python: Create examples/output_demo.py with:
  - Colorama basic colors
  - Rich console features (tables, syntax highlighting, panels)
  - Progress bar demonstrations
  - Tabulate table examples
  - Status symbols

Phase 5: Documentation
Goal: Create usage documentation for output formatting

Actions:
- Add OUTPUT_FORMATTING.md to docs/ or root:
  - Quick start guide
  - Color function usage
  - Spinner examples
  - Table formatting options
  - Progress bar usage
  - Icon/symbol reference
- Include screenshot examples if possible
- Add troubleshooting section for common issues

Phase 6: Summary
Goal: Report what was installed and created

Actions:
- Display installed packages with versions
- List created files (utilities, examples, docs)
- Show quick usage example
- Suggest next steps for integration
- Provide links to library documentation
