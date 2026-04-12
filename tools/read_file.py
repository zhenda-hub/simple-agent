"""Read file tool."""

from pathlib import Path

from . import tool

MAX_LENGTH = 10000


@tool(
    name="read_file",
    description="Read the contents of a file. Supports offset and limit for reading specific line ranges.",
    parameters={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to read",
            },
            "offset": {
                "type": "integer",
                "description": "Line number to start reading from (0-indexed, default 0)",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of lines to read",
            },
        },
        "required": ["path"],
    },
)
def read_file(path: str, offset: int = 0, limit: int | None = None) -> str:
    file_path = Path(path)
    if not file_path.exists():
        return f"Error: File not found: {path}"
    if not file_path.is_file():
        return f"Error: Not a file: {path}"

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as e:
        return f"Error reading file: {type(e).__name__}: {e}"

    sliced = lines[offset:]
    if limit is not None:
        sliced = sliced[:limit]
    content = "".join(sliced)

    if len(content) > MAX_LENGTH:
        content = content[:MAX_LENGTH] + f"\n... (truncated, {len(content)} total chars)"
    return content
