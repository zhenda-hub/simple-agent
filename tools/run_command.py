"""Command execution tool with user confirmation for dangerous commands."""

import os
import subprocess

from . import tool

_timeout = int(os.getenv("CODE_EXECUTION_TIMEOUT", "30"))
MAX_OUTPUT = 10000

# Commands that need user confirmation
_DANGEROUS_PATTERNS = (
    "rm ", "del ", "rmdir", "rd ", "format ", "shutdown",
    "taskkill", "reg ", "net ", "netsh ", "mklink",
    "cipher", "diskpart", "bcdedit",
)


def _truncate(text: str) -> str:
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n... (truncated, {len(text)} total chars)"


def _is_dangerous(cmd: str) -> bool:
    lower = cmd.lower().strip()
    for pattern in _DANGEROUS_PATTERNS:
        if lower.startswith(pattern) or f" {pattern}" in lower or f"&&{pattern}" in lower or f"&{pattern}" in lower:
            return True
    return False


@tool(
    name="run_command",
    description="Execute a shell command and return stdout, stderr, and exit code. OS is Windows.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to execute",
            },
        },
        "required": ["command"],
    },
)
def run_command(command: str) -> str:
    if _is_dangerous(command):
        from formatter import console
        console.print(f"\n[bold red]Dangerous command detected:[/bold red] {command}")
        try:
            confirm = console.input("[bold yellow]Allow? (y/N): [/bold yellow]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "Error: Command rejected by user."
        if confirm != "y":
            return "Error: Command rejected by user."

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=_timeout,
            shell=True,
        )
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {_timeout} seconds."

    parts = [f"Exit code: {result.returncode}"]
    if result.stdout:
        parts.append(f"Stdout:\n{_truncate(result.stdout)}")
    if result.stderr:
        parts.append(f"Stderr:\n{_truncate(result.stderr)}")
    return "\n".join(parts) if len(parts) > 1 else parts[0]
