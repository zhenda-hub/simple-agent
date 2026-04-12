"""Sandboxed Python code execution tool."""

import os
import subprocess
import tempfile

from . import tool

_timeout = int(os.getenv("CODE_EXECUTION_TIMEOUT", "30"))

MAX_OUTPUT = 5000


def _truncate(text: str) -> str:
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n... (truncated, {len(text)} total chars)"


@tool(
    name="execute_code",
    description="Execute Python code in a sandboxed subprocess and return stdout, stderr, and exit code.",
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Python code to execute",
            },
        },
        "required": ["code"],
    },
)
def execute_code(code: str) -> str:
    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=_timeout,
            cwd=tempfile.gettempdir(),
            env={"PATH": os.environ.get("PATH", "")},  # Clean env, no API keys
        )
    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out after {_timeout} seconds."

    parts = [f"Exit code: {result.returncode}"]
    if result.stdout:
        parts.append(f"Stdout:\n{_truncate(result.stdout)}")
    if result.stderr:
        parts.append(f"Stderr:\n{_truncate(result.stderr)}")
    return "\n".join(parts)
