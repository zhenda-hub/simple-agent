"""Pytest configuration and fixtures."""

import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for tests."""
    with patch.dict(os.environ, {
        "SILICONFLOW_API_KEY": "test-key-for-testing",
        "OPENROUTER_API_KEY": "test-key-for-testing",
    }):
        yield


@pytest.fixture
def sample_state():
    """Create a sample agent state."""
    from langchain_core.messages import HumanMessage
    return {
        "messages": [HumanMessage(content="Test message")],
        "next": ""
    }
