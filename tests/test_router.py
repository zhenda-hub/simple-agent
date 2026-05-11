"""Test cases for router functionality."""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from agents.router import route_node, create_router_llm, Route


class TestRouteModel:
    """Tests for Route pydantic model."""

    def test_route_model_accepts_all_agent_types(self):
        """Test Route model accepts all valid agent types."""
        valid_types = ["code", "file", "system", "web", "data", "planning"]

        for agent_type in valid_types:
            route = Route(next=agent_type)
            assert route.next == agent_type

    def test_route_model_rejects_invalid_type(self):
        """Test Route model rejects invalid agent types."""
        with pytest.raises(Exception):  # Pydantic validation error
            Route(next="invalid_agent")


class TestRouterNode:
    """Tests for route_node function."""

    @pytest.fixture
    def mock_state(self):
        """Create a mock state."""
        return {
            "messages": [HumanMessage(content="Write a Python function")],
            "next": ""
        }

    @patch('agents.router.create_router_llm')
    def test_route_node_returns_next_agent(self, mock_create_llm, mock_state):
        """Test route_node returns correct next agent."""
        # Mock the LLM response
        mock_llm = Mock()
        mock_route = Mock()
        mock_route.next = "code"
        mock_llm.invoke.return_value = mock_route
        mock_create_llm.return_value = mock_llm

        result = route_node(mock_state)

        assert isinstance(result, dict)
        assert "next" in result
        assert result["next"] == "code"

    @patch('agents.router.create_router_llm')
    def test_route_node_handles_all_agent_types(self, mock_create_llm):
        """Test router can route to all agent types."""
        agent_types = ["code", "file", "system", "web", "data", "planning"]

        for agent_type in agent_types:
            mock_state = {
                "messages": [HumanMessage(content=f"Route to {agent_type}")],
                "next": ""
            }

            mock_llm = Mock()
            mock_route = Mock()
            mock_route.next = agent_type
            mock_llm.invoke.return_value = mock_route
            mock_create_llm.return_value = mock_llm

            result = route_node(mock_state)
            assert result["next"] == agent_type


class TestCreateRouterLLM:
    """Tests for create_router_llm function."""

    @patch('agents.router.ChatOpenAI')
    @patch('config._detect_provider')
    def test_create_router_llm_siliconflow(self, mock_detect, mock_chat_openai):
        """Test router LLM creation with SiliconFlow provider."""
        mock_detect.return_value = ("siliconflow", "https://api.siliconflow.cn/v1", "test_key")

        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = Mock()
        mock_chat_openai.return_value = mock_llm

        result = create_router_llm()

        assert mock_chat_openai.called
        assert mock_llm.with_structured_output.called

    @patch('agents.router.ChatOpenAI')
    @patch('config._detect_provider')
    def test_create_router_llm_openrouter(self, mock_detect, mock_chat_openai):
        """Test router LLM creation with OpenRouter provider."""
        mock_detect.return_value = ("openrouter", "https://openrouter.ai/api/v1", "test_key")

        mock_llm = Mock()
        mock_llm.with_structured_output.return_value = Mock()
        mock_chat_openai.return_value = mock_llm

        result = create_router_llm()

        assert mock_chat_openai.called
        assert mock_llm.with_structured_output.called
