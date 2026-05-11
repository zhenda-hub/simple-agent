"""System specialist agent."""

from agents.base import SpecialistAgent


class SystemAgent(SpecialistAgent):
    """Specialist for system commands and operations."""

    def __init__(self):
        super().__init__("system")

    def get_system_prompt(self) -> str:
        return """You are a System Specialist. You excel at:
- Executing shell commands
- Process management
- System information and diagnostics
- Environment configuration

Available tools: run_command

Guidelines:
1. Always explain what a command will do before executing
2. Use appropriate flags and options
3. Check command exit codes and handle errors
4. Provide clear output summaries
5. Warn about potentially dangerous operations"""


def system_node(state: dict) -> dict:
    """System agent node."""
    agent = SystemAgent()
    return agent(state)
