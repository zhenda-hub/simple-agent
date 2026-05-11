# 测试文档

本项目使用 **pytest** 作为测试框架，包含完整的单元测试和集成测试。

## 测试概览

```
tests/
├── __init__.py          # 测试模块初始化
├── conftest.py          # Pytest 配置和 fixtures
├── test_agents.py       # Agent 测试（18个测试）
├── test_router.py       # 路由测试（6个测试）
└── test_graph.py        # Graph 测试（5个测试）
```

## 运行测试

### 运行所有测试

```bash
uv run pytest tests/ -v
```

### 运行测试并查看覆盖率

```bash
uv run pytest tests/ --cov=agents --cov=multi_agent_graph --cov-report=term-missing
```

### 运行特定测试文件

```bash
uv run pytest tests/test_agents.py -v
```

### 运行特定测试类或函数

```bash
# 运行 CodeAgent 相关测试
uv run pytest tests/test_agents.py::TestAgentSystemPrompts::test_code_agent_system_prompt -v

# 运行路由相关测试
uv run pytest tests/test_router.py -v
```

### 只运行单元测试（跳过集成测试）

```bash
uv run pytest tests/ -m "not integration"
```

## 测试结果

当前测试覆盖率：**86%**

| 模块 | 覆盖率 | 状态 |
|------|--------|------|
| `agents/router.py` | 100% | ✅ |
| `agents/code.py` | 100% | ✅ |
| `agents/file.py` | 100% | ✅ |
| `agents/system.py` | 100% | ✅ |
| `agents/web.py` | 100% | ✅ |
| `agents/data.py` | 100% | ✅ |
| `agents/planning.py` | 100% | ✅ |
| `multi_agent_graph.py` | 100% | ✅ |
| `agents/base.py` | 33% | ⚠️  需要 LLM 调用 |

## 编写测试

### 测试文件结构

```python
"""Test cases for <module>."""

import pytest
from unittest.mock import Mock, patch

from your_module import YourClass


class TestYourClass:
    """Tests for YourClass."""

    def test_something_simple(self):
        """Test simple functionality."""
        result = YourClass.method()
        assert result == expected_value

    @patch('module.external_dependency')
    def test_with_mock(self, mock_dep):
        """Test with mocked dependency."""
        mock_dep.return_value = "mocked"
        result = YourClass.method()
        assert result == "mocked"
```

### 使用 Fixtures

```python
# conftest.py
@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {"key": "value"}

# test file
def test_with_fixture(sample_data):
    """Test using fixture."""
    assert sample_data["key"] == "value"
```

### Mock LLM 调用

```python
@patch('agents.base.ChatOpenAI')
@patch('agents.base.get_tool_schemas')
def test_agent_with_mocks(self, mock_tools, mock_llm):
    """Test agent without real LLM calls."""
    mock_llm_instance = Mock()
    mock_llm_instance.invoke.return_value = Mock(content="Test response")
    mock_llm.return_value = mock_llm_instance
    mock_tools.return_value = []

    # Your test code here
```

## CI/CD 集成

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run tests
        run: uv run pytest tests/ --cov
```

## 相关资源

- [pytest 文档](https://docs.pytest.org/)
- [pytest-mock 文档](https://pytest-mock.readthedocs.io/)
- [pytest-cov 文档](https://pytest-cov.readthedocs.io/)
