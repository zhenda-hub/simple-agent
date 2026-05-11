"""Data analysis specialist agent."""

from agents.base import SpecialistAgent


class DataAgent(SpecialistAgent):
    """Specialist for data analysis and visualization."""

    def __init__(self):
        super().__init__("data")

    def get_system_prompt(self) -> str:
        return """You are a Data Analysis Specialist. You excel at:
- Analyzing structured data (CSV, JSON, Excel)
- Performing statistical analysis
- Creating data visualizations
- Generating insights and reports

Available tools: run_command, write_file

Guidelines:
1. Always inspect data structure first
2. Handle missing data appropriately
3. Use appropriate visualization types
4. Explain your findings clearly"""


def data_node(state: dict) -> dict:
    """Data agent node."""
    agent = DataAgent()
    return agent(state)
