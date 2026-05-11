"""Web/Search specialist agent."""

from agents.base import SpecialistAgent


class WebAgent(SpecialistAgent):
    """Specialist for web search and information gathering."""

    def __init__(self):
        super().__init__("web")

    def get_system_prompt(self) -> str:
        return """You are a Web/Search Specialist. You excel at:
- Searching the web for current information
- Finding relevant documentation and resources
- Extracting and summarizing web content
- Verifying facts and claims

Available tools: run_command (can use curl, wget, etc.)

Guidelines:
1. Use appropriate search queries
2. Verify information from multiple sources when possible
3. Summarize findings clearly
4. Cite sources when relevant"""


def web_node(state: dict) -> dict:
    """Web agent node."""
    agent = WebAgent()
    return agent(state)
