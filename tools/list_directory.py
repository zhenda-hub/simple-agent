"""List directory tool."""

import os
from pathlib import Path

from . import tool


@tool(
    name="list_directory",
    description="List files and directories at the given path.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the directory to list",
            },
        },
        "required": ["path"],
    },
)
def list_directory(path: str) -> str:
    dir_path = Path(path)
    if not dir_path.exists():
        return f"Error: Path not found: {path}"
    if not dir_path.is_dir():
        return f"Error: Not a directory: {path}"

    try:
        entries = sorted(dir_path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return f"Error: Permission denied: {path}"

    lines = []
    for entry in entries:
        prefix = "[DIR]  " if entry.is_dir() else "[FILE] "
        size = ""
        if entry.is_file():
            try:
                size = f" ({entry.stat().st_size} bytes)"
            except OSError:
                pass
        lines.append(f"{prefix}{entry.name}{size}")

    if not lines:
        return "(empty directory)"

    return "\n".join(lines)
