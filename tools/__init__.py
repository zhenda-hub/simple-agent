"""Tool registry with decorator-based registration."""

import json
from dataclasses import dataclass
from typing import Any, Callable

_TOOL_REGISTRY: dict[str, "ToolDefinition"] = {}


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: dict
    fn: Callable[..., Any]


def tool(name: str, description: str, parameters: dict):
    """Decorator that registers a function as a tool."""

    def decorator(fn: Callable):
        _TOOL_REGISTRY[name] = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            fn=fn,
        )
        return fn

    return decorator


def get_tool_schemas() -> list[dict]:
    """Return tool definitions in OpenAI API format."""
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            },
        }
        for t in _TOOL_REGISTRY.values()
    ]


def execute_tool(name: str, arguments: dict) -> str:
    """Look up and execute a tool by name. Returns string result."""
    if name not in _TOOL_REGISTRY:
        return f"Error: Unknown tool '{name}'"
    tool_def = _TOOL_REGISTRY[name]
    try:
        result = tool_def.fn(**arguments)
        return str(result)
    except Exception as e:
        return f"Error executing {name}: {type(e).__name__}: {e}"


# Import all tool modules to trigger @tool registration
from tools import execute_code, list_directory, read_file, write_file  # noqa: E402, F401
