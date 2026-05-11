"""LangGraph configuration for multi-agent system."""

from typing import TypedDict, Annotated, List
from operator import add
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State for the multi-agent graph."""
    messages: Annotated[List[BaseMessage], add]
    next: str  # Next agent to route to


# Define available agent types
AGENT_TYPES = {
    "code": "Code specialist for programming, debugging, and code review",
    "file": "File specialist for file operations and directory management",
    "system": "System specialist for shell commands and system operations",
}
