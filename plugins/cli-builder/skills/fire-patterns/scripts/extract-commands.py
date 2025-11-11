#!/usr/bin/env python3
"""Extract command structure from Fire CLI for documentation"""

import ast
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional


class CommandExtractor:
    """Extract command structure from Fire CLI Python files"""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.tree = None
        self.commands = []

    def extract(self) -> List[Dict]:
        """Extract all commands from Fire CLI"""
        try:
            content = self.filepath.read_text()
            self.tree = ast.parse(content)
        except Exception as e:
            print(f"Error parsing file: {e}", file=sys.stderr)
            return []

        # Find all classes
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                self._extract_from_class(node)

        return self.commands

    def _extract_from_class(self, class_node: ast.ClassDef, parent_path: str = ""):
        """Extract commands from a class"""
        class_name = class_node.name
        class_doc = ast.get_docstring(class_node) or ""

        current_path = f"{parent_path}.{class_name}" if parent_path else class_name

        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                # Skip private methods
                if item.name.startswith('_'):
                    continue

                command = self._extract_command(item, current_path)
                if command:
                    self.commands.append(command)

            elif isinstance(item, ast.ClassDef):
                # Nested class - recurse
                self._extract_from_class(item, current_path)

    def _extract_command(self, func_node: ast.FunctionDef, class_path: str) -> Optional[Dict]:
        """Extract command information from function"""
        func_name = func_node.name
        docstring = ast.get_docstring(func_node) or ""

        # Parse docstring for description and args
        description = ""
        args_help = {}

        if docstring:
            lines = docstring.split('\n')
            desc_lines = []
            in_args = False

            for line in lines:
                line = line.strip()
                if line.startswith('Args:'):
                    in_args = True
                    continue
                elif line.startswith('Returns:') or line.startswith('Raises:'):
                    in_args = False
                    continue

                if not in_args and line:
                    desc_lines.append(line)
                elif in_args and line:
                    # Parse arg line: "arg_name: description"
                    if ':' in line:
                        arg_name, arg_desc = line.split(':', 1)
                        args_help[arg_name.strip()] = arg_desc.strip()

            description = ' '.join(desc_lines)

        # Extract arguments
        args = []
        for arg in func_node.args.args:
            if arg.arg == 'self':
                continue

            arg_info = {
                'name': arg.arg,
                'type': self._get_type_annotation(arg),
                'help': args_help.get(arg.arg, ''),
            }

            # Check for default value
            defaults_offset = len(func_node.args.args) - len(func_node.args.defaults)
            arg_index = func_node.args.args.index(arg)
            if arg_index >= defaults_offset:
                default_index = arg_index - defaults_offset
                default_value = self._get_default_value(func_node.args.defaults[default_index])
                arg_info['default'] = default_value
                arg_info['required'] = False
            else:
                arg_info['required'] = True

            args.append(arg_info)

        return {
            'name': func_name,
            'path': f"{class_path}.{func_name}",
            'description': description,
            'arguments': args
        }

    def _get_type_annotation(self, arg: ast.arg) -> Optional[str]:
        """Extract type annotation from argument"""
        if arg.annotation:
            return ast.unparse(arg.annotation)
        return None

    def _get_default_value(self, node) -> str:
        """Extract default value from AST node"""
        try:
            return ast.unparse(node)
        except:
            return repr(node)

    def print_tree(self):
        """Print command tree in human-readable format"""
        print(f"\n{'='*60}")
        print(f"Fire CLI Commands: {self.filepath.name}")
        print(f"{'='*60}\n")

        for cmd in self.commands:
            print(f"📌 {cmd['path']}")
            if cmd['description']:
                print(f"   {cmd['description']}")
            if cmd['arguments']:
                print(f"   Arguments:")
                for arg in cmd['arguments']:
                    required = "required" if arg['required'] else "optional"
                    type_str = f": {arg['type']}" if arg['type'] else ""
                    default_str = f" = {arg['default']}" if 'default' in arg else ""
                    help_str = f" - {arg['help']}" if arg['help'] else ""
                    print(f"     • {arg['name']}{type_str}{default_str} ({required}){help_str}")
            print()

    def export_json(self) -> str:
        """Export commands as JSON"""
        return json.dumps(self.commands, indent=2)

    def export_markdown(self) -> str:
        """Export commands as Markdown"""
        lines = [f"# {self.filepath.name} Commands\n"]

        for cmd in self.commands:
            lines.append(f"## `{cmd['path']}`\n")

            if cmd['description']:
                lines.append(f"{cmd['description']}\n")

            if cmd['arguments']:
                lines.append("### Arguments\n")
                for arg in cmd['arguments']:
                    required = "**required**" if arg['required'] else "*optional*"
                    type_str = f" (`{arg['type']}`)" if arg['type'] else ""
                    default_str = f" Default: `{arg['default']}`" if 'default' in arg else ""

                    lines.append(f"- `{arg['name']}`{type_str} - {required}{default_str}")
                    if arg['help']:
                        lines.append(f"  - {arg['help']}")

            lines.append("")

        return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract-commands.py <fire-cli-file.py> [--json|--markdown]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    output_format = sys.argv[2] if len(sys.argv) > 2 else '--tree'

    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    extractor = CommandExtractor(filepath)
    extractor.extract()

    if output_format == '--json':
        print(extractor.export_json())
    elif output_format == '--markdown':
        print(extractor.export_markdown())
    else:
        extractor.print_tree()


if __name__ == '__main__':
    main()
