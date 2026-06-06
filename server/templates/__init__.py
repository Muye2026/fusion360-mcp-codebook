"""Template loader — reads tested code templates from the codebook .py files."""

import os
import re
from pathlib import Path

from . import config


def get_codebook_root() -> Path:
    """Return the path to the codebook root directory."""
    return Path(config.CODEBOOK_ROOT)


def load_template(category: str, function_name: str) -> str:
    """Load a tested code template from the codebook.

    Args:
        category: Subdirectory name (e.g., 'basic_shapes', 'features').
        function_name: Python file name without .py extension (e.g., 'create_cube').

    Returns:
        The raw Python source code as a string.

    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    path = get_codebook_root() / category / f"{function_name}.py"
    if not path.exists():
        raise FileNotFoundError(f"Codebook template not found: {path}")
    return path.read_text(encoding="utf-8")


def extract_function_code(template_source: str, function_name: str) -> str:
    """Extract just the function definition from a template source.

    Strips the header comments and the standalone call at the bottom,
    returning only the function definition that can be called with custom args.

    Args:
        template_source: Full source code from a .py file.
        function_name: Name of the function to extract.

    Returns:
        The function definition code (def ... to the end of function body).
    """
    lines = template_source.split("\n")
    # Find the function def line
    func_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"def {function_name}"):
            func_start = i
            break

    if func_start is None:
        # No function wrapper — return the whole source minus header comments
        code_lines = []
        for line in lines:
            if line.strip().startswith("#") and func_start is None:
                continue
            code_lines.append(line)
        return "\n".join(code_lines).strip()

    # Find the end of the function (next line at same or lower indent level that's not blank)
    func_lines = [lines[func_start]]
    for i in range(func_start + 1, len(lines)):
        line = lines[i]
        # If line is not blank and not indented deeper than the function body, we've exited the function
        if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
            break
        func_lines.append(line)

    return "\n".join(func_lines)


def build_execution_code(template_source: str, function_name: str, call_args: str) -> str:
    """Build complete executable code from a template.

    Takes a codebook .py file, extracts the function definition,
    and appends a custom call with the given arguments.

    Args:
        template_source: Full source code from a .py file.
        function_name: Name of the function to call.
        call_args: Argument string for the call, e.g., 'width=2.0, height=2.0, depth=2.0, name="Cube"'.

    Returns:
        Complete Python code ready to execute via execute_python.
    """
    lines = template_source.split("\n")

    # Collect: import lines + function definition
    import_lines = []
    func_lines = []
    in_function = False
    func_indent = None

    for line in lines:
        stripped = line.strip()

        # Skip header comments
        if stripped.startswith("#") and not in_function:
            continue

        # Collect import lines
        if stripped.startswith("import ") or stripped.startswith("from "):
            import_lines.append(line)
            continue

        # Detect function start
        if stripped.startswith(f"def {function_name}"):
            in_function = True
            func_lines.append(line)
            func_indent = len(line) - len(line.lstrip())
            continue

        # Collect function body
        if in_function:
            # Check if we've exited the function
            if stripped and not stripped.startswith("#"):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= func_indent and not stripped.startswith("def "):
                    # We've left the function
                    break
            func_lines.append(line)

    # Build final code
    code_parts = []
    if import_lines:
        code_parts.append("\n".join(import_lines))
    if func_lines:
        code_parts.append("\n".join(func_lines))
    code_parts.append(f'{function_name}({call_args})')

    return "\n\n".join(code_parts)
