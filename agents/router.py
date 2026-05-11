"""Router agent for task classification and routing."""

from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from config import load_config


class Route(BaseModel):
    """Route a user query to the appropriate specialist agent."""

    next: Literal["code", "file", "system", "web", "data", "planning"] = Field(
        description="Given a user request, choose the most appropriate specialist agent:\n"
        "- code: For programming, debugging, code review, technical questions\n"
        "- file: For file operations, reading/writing files, directory management\n"
        "- system: For shell commands, system operations, process management\n"
        "- web: For web search, information gathering, documentation lookup\n"
        "- data: For data analysis, statistics, visualization, CSV/JSON processing\n"
        "- planning: For task planning, project breakdown, creating execution plans"
    )


def create_router_llm():
    """Create LLM with structured output for routing."""
    # Use available provider, but use a general model ID that should work
    from config import _detect_provider
    provider, base_url, api_key = _detect_provider()

    # Use a simple model ID that should exist on most providers
    # For SiliconFlow, use a commonly available model
    if provider == "siliconflow":
        model = "Qwen/Qwen2.5-7B-Instruct"  # Commonly available
    else:  # openrouter
        model = "meta-llama/llama-3-8b-instruct:free"

    llm = ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=0
    )
    return llm.with_structured_output(Route)


def route_node(state: dict) -> dict:
    """Router node: classify the task and determine the next agent."""
    messages = state["messages"]

    # Get the last user message
    last_message = messages[-1]
    user_input = last_message.content

    # Use LLM for routing decision
    router_llm = create_router_llm()
    route_decision = router_llm.invoke(f"User request: {user_input}")

    print(f"🔀 Router → {route_decision.next} agent")

    return {"next": route_decision.next}
