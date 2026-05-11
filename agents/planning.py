"""Planning specialist agent."""

from agents.base import SpecialistAgent


class PlanningAgent(SpecialistAgent):
    """Specialist for task planning and decomposition."""

    def __init__(self):
        super().__init__("planning")

    def get_system_prompt(self) -> str:
        return """You are a Planning Specialist. You excel at:
- Breaking down complex tasks into subtasks
- Identifying dependencies and prerequisites
- Estimating effort and resources needed
- Creating execution plans

Available tools: run_command, write_file

Guidelines:
1. Think step-by-step and logically
2. Identify clear deliverables for each step
3. Consider potential risks and alternatives
4. Present plans in a structured format (numbered lists, tables, etc.)"""


def planning_node(state: dict) -> dict:
    """Planning agent node."""
    agent = PlanningAgent()
    return agent(state)
