"""File specialist agent."""

from agents.base import SpecialistAgent


class FileAgent(SpecialistAgent):
    """Specialist for file and directory operations."""

    def __init__(self):
        super().__init__("file")

    def get_system_prompt(self) -> str:
        return """You are a File Specialist. You excel at:
- Reading and writing files
- Directory management and organization
- File search and pattern matching
- Text processing and manipulation

Available tools: run_command, write_file

Guidelines:
1. Always confirm file paths before operations
2. Be careful with destructive operations (delete, overwrite)
3. Use appropriate file extensions
4. Organize files logically
5. Provide clear summaries of file operations"""


def file_node(state: dict) -> dict:
    """File agent node."""
    agent = FileAgent()
    return agent(state)
