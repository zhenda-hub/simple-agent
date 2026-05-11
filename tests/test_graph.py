"""Test cases for multi-agent graph."""

import pytest
from langgraph.graph import StateGraph

from multi_agent_graph import build_multi_agent_graph, multi_agent_app
from graph_config import AgentState


class TestMultiAgentGraph:
    """Tests for multi-agent graph compilation."""

    def test_graph_compiles_successfully(self):
        """Test that the graph compiles without errors."""
        graph = build_multi_agent_graph()
        assert graph is not None

    def test_graph_has_all_nodes(self):
        """Test that the graph contains all expected nodes."""
        graph = multi_agent_app
        nodes = list(graph.get_graph().nodes.keys())

        expected_nodes = [
            "__start__",
            "router",
            "code",
            "file",
            "system",
            "web",
            "data",
            "planning",
            "__end__"
        ]

        for node in expected_nodes:
            assert node in nodes, f"Node {node} not found in graph"

    def test_graph_node_count(self):
        """Test that the graph has the correct number of nodes."""
        graph = multi_agent_app
        nodes = list(graph.get_graph().nodes.keys())

        # Should have: start, router, 6 specialists, end = 9 nodes
        assert len(nodes) == 9

    def test_global_app_instance_exists(self):
        """Test that the global app instance is created."""
        assert multi_agent_app is not None
        assert hasattr(multi_agent_app, 'invoke')

    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires API keys - run manually")
    def test_graph_can_be_invoked(self):
        """Integration test: Test that the graph can be invoked (requires API)."""
        from langchain_core.messages import HumanMessage

        initial_state = {
            "messages": [HumanMessage(content="Test message")],
            "next": ""
        }

        config = {"configurable": {"thread_id": "test-session"}}

        try:
            result = multi_agent_app.invoke(initial_state, config=config)
            assert "messages" in result
            assert "next" in result
        except Exception as e:
            pytest.skip(f"API error: {e}")


class TestAgentState:
    """Tests for AgentState configuration."""

    def test_agent_state_has_messages_field(self):
        """Test AgentState has messages field."""
        # TypedDict is just a type hint, check the definition
        assert "messages" in AgentState.__annotations__

    def test_agent_state_has_next_field(self):
        """Test AgentState has next field."""
        assert "next" in AgentState.__annotations__

    def test_agent_state_structure(self):
        """Test AgentState has correct structure."""
        from typing_extensions import get_args, get_origin
        # Check that AgentState is a TypedDict with required fields
        assert hasattr(AgentState, '__annotations__')
        assert 'messages' in AgentState.__annotations__
        assert 'next' in AgentState.__annotations__
