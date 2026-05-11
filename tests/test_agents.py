"""Test cases for specialist agents."""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from agents.code import CodeAgent, code_node
from agents.file import FileAgent, file_node
from agents.system import SystemAgent, system_node
from agents.web import WebAgent, web_node
from agents.data import DataAgent, data_node
from agents.planning import PlanningAgent, planning_node


class TestAgentSystemPrompts:
    """Test system prompts for all agents."""

    def test_code_agent_system_prompt(self):
        """Test CodeAgent has appropriate system prompt."""
        prompt = CodeAgent.get_system_prompt(CodeAgent)
        assert "Code Specialist" in prompt
        assert "programming" in prompt.lower()
        assert "debugging" in prompt.lower()

    def test_file_agent_system_prompt(self):
        """Test FileAgent has appropriate system prompt."""
        prompt = FileAgent.get_system_prompt(FileAgent)
        assert "File Specialist" in prompt
        assert "file operations" in prompt.lower()

    def test_system_agent_system_prompt(self):
        """Test SystemAgent has appropriate system prompt."""
        prompt = SystemAgent.get_system_prompt(SystemAgent)
        assert "System Specialist" in prompt
        assert "shell commands" in prompt.lower()

    def test_web_agent_system_prompt(self):
        """Test WebAgent has appropriate system prompt."""
        prompt = WebAgent.get_system_prompt(WebAgent)
        assert "Web/Search Specialist" in prompt
        assert "search" in prompt.lower()

    def test_data_agent_system_prompt(self):
        """TestDataAgent has appropriate system prompt."""
        prompt = DataAgent.get_system_prompt(DataAgent)
        assert "Data Analysis Specialist" in prompt
        assert "data" in prompt.lower()

    def test_planning_agent_system_prompt(self):
        """Test PlanningAgent has appropriate system prompt."""
        prompt = PlanningAgent.get_system_prompt(PlanningAgent)
        assert "Planning Specialist" in prompt
        assert "planning" in prompt.lower()


class TestAgentNodes:
    """Test agent node functions."""

    @pytest.fixture
    def mock_state(self):
        """Create a mock state."""
        return {
            "messages": [HumanMessage(content="Test message")],
            "next": ""
        }

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_code_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test code_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = code_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_file_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test file_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = file_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_system_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test system_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = system_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_web_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test web_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = web_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_data_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test data_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = data_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result

    @patch('agents.base.SpecialistAgent.__init__', return_value=None)
    @patch('agents.base.SpecialistAgent.__call__')
    def test_planning_node_returns_dict(self, mock_call, mock_init, mock_state):
        """Test planning_node returns proper dict structure."""
        mock_call.return_value = {"messages": [Mock(content="Response")]}
        result = planning_node(mock_state)
        assert isinstance(result, dict)
        assert "messages" in result
