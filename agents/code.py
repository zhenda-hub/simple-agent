"""Code specialist agent."""

from agents.base import SpecialistAgent


class CodeAgent(SpecialistAgent):
    """Specialist for programming and code-related tasks."""

    def __init__(self):
        super().__init__("code")

    def get_system_prompt(self) -> str:
        return """You are a Code Specialist. You excel at:
- Writing and debugging code in any programming language
- Code review and optimization suggestions
- Explaining technical concepts and algorithms
- Making architectural decisions

Available tools: run_command, write_file

Guidelines:
1. Think step-by-step when writing code
2. Always consider error handling and edge cases
3. Provide clear, well-commented code
4. Test your code when possible
5. Explain your reasoning clearly"""


def code_node(state: dict) -> dict:
    """Code agent node."""
    agent = CodeAgent()
    return agent(state)
