#!/usr/bin/env python3
"""Test Fire CLI commands programmatically"""

import sys
import importlib.util
import inspect
from pathlib import Path
from typing import Any, List, Dict
import json


class FireCLITester:
    """Test Fire CLI commands without running them"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.module = None
        self.cli_class = None

    def load_cli(self) -> bool:
        """Load CLI module dynamically"""
        try:
            spec = importlib.util.spec_from_file_location("cli_module", self.filepath)
            self.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.module)

            # Find main CLI class (first class in module)
            for name, obj in inspect.getmembers(self.module):
                if inspect.isclass(obj) and obj.__module__ == self.module.__name__:
                    self.cli_class = obj
                    break

            if not self.cli_class:
                print("Error: No CLI class found in module", file=sys.stderr)
                return False

            return True

        except Exception as e:
            print(f"Error loading CLI module: {e}", file=sys.stderr)
            return False

    def get_commands(self) -> Dict[str, Any]:
        """Get all available commands"""
        if not self.cli_class:
            return {}

        commands = {}
        instance = self.cli_class()

        # Get methods from main class
        for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
            if not name.startswith('_'):
                commands[name] = {
                    'type': 'method',
                    'signature': str(inspect.signature(method)),
                    'doc': inspect.getdoc(method) or 'No documentation'
                }

        # Get nested classes (command groups)
        for name, obj in inspect.getmembers(self.cli_class):
            if inspect.isclass(obj) and not name.startswith('_'):
                commands[name] = {
                    'type': 'command_group',
                    'doc': inspect.getdoc(obj) or 'No documentation',
                    'methods': {}
                }

                # Get methods from nested class
                for method_name, method in inspect.getmembers(obj, predicate=inspect.isfunction):
                    if not method_name.startswith('_'):
                        commands[name]['methods'][method_name] = {
                            'signature': str(inspect.signature(method)),
                            'doc': inspect.getdoc(method) or 'No documentation'
                        }

        return commands

    def test_instantiation(self) -> bool:
        """Test if CLI class can be instantiated"""
        try:
            instance = self.cli_class()
            print("✅ CLI class instantiation: PASSED")
            return True
        except Exception as e:
            print(f"❌ CLI class instantiation: FAILED - {e}")
            return False

    def test_method_signatures(self) -> bool:
        """Test if all methods have valid signatures"""
        try:
            instance = self.cli_class()
            errors = []

            for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
                if name.startswith('_'):
                    continue

                try:
                    sig = inspect.signature(method)
                    # Check for invalid parameter types
                    for param_name, param in sig.parameters.items():
                        if param.kind == inspect.Parameter.VAR_KEYWORD:
                            errors.append(f"Method '{name}' uses **kwargs (works but not recommended)")
                except Exception as e:
                    errors.append(f"Method '{name}' signature error: {e}")

            if errors:
                print("⚠️  Method signatures: WARNINGS")
                for error in errors:
                    print(f"    • {error}")
                return True  # Warnings, not failures
            else:
                print("✅ Method signatures: PASSED")
                return True

        except Exception as e:
            print(f"❌ Method signatures: FAILED - {e}")
            return False

    def test_docstrings(self) -> bool:
        """Test if all public methods have docstrings"""
        try:
            instance = self.cli_class()
            missing = []

            for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
                if name.startswith('_'):
                    continue

                doc = inspect.getdoc(method)
                if not doc:
                    missing.append(name)

            if missing:
                print("⚠️  Docstrings: WARNINGS")
                print(f"    Missing docstrings for: {', '.join(missing)}")
                return True  # Warnings, not failures
            else:
                print("✅ Docstrings: PASSED")
                return True

        except Exception as e:
            print(f"❌ Docstrings: FAILED - {e}")
            return False

    def print_summary(self):
        """Print CLI summary"""
        commands = self.get_commands()

        print(f"\n{'='*60}")
        print(f"Fire CLI Test Report: {self.filepath.name}")
        print(f"{'='*60}\n")

        print(f"CLI Class: {self.cli_class.__name__}")
        print(f"Total Commands: {len(commands)}\n")

        print("Available Commands:")
        for cmd_name, cmd_info in commands.items():
            if cmd_info['type'] == 'method':
                print(f"  • {cmd_name}{cmd_info['signature']}")
            elif cmd_info['type'] == 'command_group':
                print(f"  • {cmd_name}/ (command group)")
                for method_name, method_info in cmd_info['methods'].items():
                    print(f"    ◦ {method_name}{method_info['signature']}")

        print()

    def run_tests(self) -> bool:
        """Run all tests"""
        print(f"\nTesting Fire CLI: {self.filepath.name}\n")

        results = []
        results.append(self.test_instantiation())
        results.append(self.test_method_signatures())
        results.append(self.test_docstrings())

        print()
        return all(results)


def main():
    if len(sys.argv) < 2:
        print("Usage: test-fire-cli.py <fire-cli-file.py> [--summary]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    show_summary = '--summary' in sys.argv

    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    tester = FireCLITester(filepath)

    if not tester.load_cli():
        sys.exit(1)

    if show_summary:
        tester.print_summary()
    else:
        passed = tester.run_tests()
        tester.print_summary()
        sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
