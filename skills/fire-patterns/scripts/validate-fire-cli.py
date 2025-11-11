#!/usr/bin/env python3
"""Validate Fire CLI structure and docstrings"""

import ast
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class FireCLIValidator:
    """Validates Fire CLI Python files for proper structure"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.tree = None

    def validate(self) -> bool:
        """Run all validation checks"""
        if not self._parse_file():
            return False

        self._check_fire_import()
        self._check_main_class()
        self._check_docstrings()
        self._check_fire_call()
        self._check_method_signatures()

        return len(self.errors) == 0

    def _parse_file(self) -> bool:
        """Parse Python file into AST"""
        try:
            content = self.filepath.read_text()
            self.tree = ast.parse(content)
            return True
        except SyntaxError as e:
            self.errors.append(f"Syntax error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to parse file: {e}")
            return False

    def _check_fire_import(self):
        """Check for fire import"""
        has_fire_import = False
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'fire':
                        has_fire_import = True
                        break
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'fire':
                    has_fire_import = True
                    break

        if not has_fire_import:
            self.errors.append("Missing 'import fire' statement")

    def _check_main_class(self):
        """Check for main CLI class"""
        classes = [node for node in self.tree.body if isinstance(node, ast.ClassDef)]

        if not classes:
            self.errors.append("No classes found - Fire CLI requires at least one class")
            return

        main_class = classes[0]  # Assume first class is main

        # Check class docstring
        docstring = ast.get_docstring(main_class)
        if not docstring:
            self.warnings.append(f"Class '{main_class.name}' missing docstring")

        # Check for __init__ method
        has_init = any(
            isinstance(node, ast.FunctionDef) and node.name == '__init__'
            for node in main_class.body
        )

        if not has_init:
            self.warnings.append(f"Class '{main_class.name}' missing __init__ method")

    def _check_docstrings(self):
        """Check method docstrings"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        # Skip private methods
                        if item.name.startswith('_'):
                            continue

                        docstring = ast.get_docstring(item)
                        if not docstring:
                            self.warnings.append(
                                f"Method '{item.name}' missing docstring "
                                "(used for Fire help text)"
                            )
                        else:
                            # Check for Args section in docstring
                            if item.args.args and len(item.args.args) > 1:  # Skip 'self'
                                if 'Args:' not in docstring:
                                    self.warnings.append(
                                        f"Method '{item.name}' docstring missing 'Args:' section"
                                    )

    def _check_fire_call(self):
        """Check for fire.Fire() call"""
        has_fire_call = False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if (isinstance(node.func.value, ast.Name) and
                        node.func.value.id == 'fire' and
                        node.func.attr == 'Fire'):
                        has_fire_call = True
                        break

        if not has_fire_call:
            self.errors.append("Missing 'fire.Fire()' call (required to run CLI)")

    def _check_method_signatures(self):
        """Check method signatures for Fire compatibility"""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        # Skip private and special methods
                        if item.name.startswith('_'):
                            continue

                        # Check for *args or **kwargs (Fire handles these but warn)
                        if item.args.vararg or item.args.kwarg:
                            self.warnings.append(
                                f"Method '{item.name}' uses *args or **kwargs - "
                                "Fire will handle these, but explicit params are clearer"
                            )

    def print_results(self):
        """Print validation results"""
        print(f"\n{'='*60}")
        print(f"Fire CLI Validation: {self.filepath.name}")
        print(f"{'='*60}\n")

        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
            print()

        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ All checks passed!")
        elif not self.errors:
            print(f"✅ Validation passed with {len(self.warnings)} warning(s)")
        else:
            print(f"❌ Validation failed with {len(self.errors)} error(s)")

        print()


def main():
    if len(sys.argv) != 2:
        print("Usage: validate-fire-cli.py <fire-cli-file.py>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    if not filepath.suffix == '.py':
        print(f"Error: File must be a Python file (.py): {filepath}")
        sys.exit(1)

    validator = FireCLIValidator(filepath)
    is_valid = validator.validate()
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
