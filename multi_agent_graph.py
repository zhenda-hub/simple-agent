"""Multi-agent system built with LangGraph."""

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from graph_config import AgentState

# Import nodes
from agents.router import route_node
from agents.code import code_node
from agents.file import file_node
from agents.system import system_node
from agents.web import web_node
from agents.data import data_node
from agents.planning import planning_node


def build_multi_agent_graph():
    """Build the multi-agent router + specialists graph."""

    # Create state graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", route_node)
    workflow.add_node("code", code_node)
    workflow.add_node("file", file_node)
    workflow.add_node("system", system_node)
    workflow.add_node("web", web_node)
    workflow.add_node("data", data_node)
    workflow.add_node("planning", planning_node)

    # Set entry point
    workflow.add_edge(START, "router")

    # Add conditional edges: router -> specialists
    workflow.add_conditional_edges(
        "router",
        lambda state: state["next"],  # Route based on 'next' field
        {
            "code": "code",
            "file": "file",
            "system": "system",
            "web": "web",
            "data": "data",
            "planning": "planning",
        }
    )

    # Each specialist ends after completion
    workflow.add_edge("code", END)
    workflow.add_edge("file", END)
    workflow.add_edge("system", END)
    workflow.add_edge("web", END)
    workflow.add_edge("data", END)
    workflow.add_edge("planning", END)

    # Compile graph with memory checkpointer for conversation history
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app


# Create global app instance
multi_agent_app = build_multi_agent_graph()
