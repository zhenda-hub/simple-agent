# Multi-Agent System

本项目使用 **LangGraph** 构建了多 Agent 系统，采用 **Router + Specialists** 架构，实现任务智能分发和专门化处理。

## 架构概览

```
                    ┌─────────────┐
                    │    START    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Router    │ ← 任务分类与路由
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │  Code   │  │  File   │  │ System  │
        │  Agent  │  │  Agent  │  │  Agent  │
        └─────────┘  └─────────┘  └─────────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌─────────────┐
                    │     END     │
                    └─────────────┘
```

## Agent 列表

### 🔀 Router Agent

**文件**: `agents/router.py`

**功能**: 任务路由器，负责分析用户请求并将其分发到最合适的 Specialist Agent。

**路由规则**:
| 用户需求类型 | 路由到 |
|-------------|--------|
| 编程、调试、代码审查 | Code Agent |
| 文件操作、目录管理 | File Agent |
| Shell 命令、系统操作 | System Agent |
| 网络搜索、资料查找 | Web Agent |
| 数据分析、统计计算 | Data Agent |
| 任务规划、项目分解 | Planning Agent |

**使用示例**:
```bash
uv run python main.py --multi-agent

> Write a Python function to sort a list
# Router → Code Agent

> Create a backup of my project
# Router → File Agent

> Check running processes
# Router → System Agent
```

---

### 💻 Code Agent

**文件**: `agents/code.py`

**功能**: 代码专家，专注于编程相关的任务。

**擅长领域**:
- 编写和调试各种编程语言的代码
- 代码审查和优化建议
- 解释技术概念和算法
- 架构设计决策

**可用工具**: `run_command`, `write_file`

**使用示例**:
```bash
> Implement a binary search tree in Python

> Debug this function: def add(a, b): return a - b

> Explain the difference between async and await in JavaScript
```

---

### 📁 File Agent

**文件**: `agents/file.py`

**功能**: 文件专家，专注于文件和目录操作。

**擅长领域**:
- 读取和写入文件
- 目录管理和组织
- 文件搜索和模式匹配
- 文本处理和转换

**可用工具**: `run_command`, `write_file`

**使用示例**:
```bash
> Read the config.yaml file and show me the database settings

> Create a new directory structure for my project: src/, tests/, docs/

> Find all Python files that contain "TODO" comments
```

---

### ⚙️ System Agent

**文件**: `agents/system.py`

**功能**: 系统专家，专注于系统命令和操作。

**擅长领域**:
- 执行 Shell 命令
- 进程管理
- 系统信息获取
- 环境配置

**可用工具**: `run_command`

**使用示例**:
```bash
> Check what Python processes are running

> Show me the disk usage of current directory

> List all environment variables
```

---

### 🔍 Web Agent

**文件**: `agents/web.py`

**功能**: 网络搜索专家，专注于信息收集和资料查找。

**擅长领域**:
- 搜索最新信息
- 查找技术文档
- 提取和总结网页内容
- 验证事实和说法

**可用工具**: `run_command` (可使用 curl, wget 等)

**使用示例**:
```bash
> Search for LangGraph multi-agent documentation

> Find the latest Python 3.13 features

> Look up the API documentation for OpenAI chat completions
```

---

### 📊 Data Agent

**文件**: `agents/data.py`

**功能**: 数据分析专家，专注于数据处理和可视化。

**擅长领域**:
- 分析结构化数据 (CSV, JSON, Excel)
- 统计分析
- 数据可视化
- 生成洞察报告

**可用工具**: `run_command`, `write_file`

**使用示例**:
```bash
> Analyze the sales.csv file and show me summary statistics

> Create a chart showing the trend of user growth

> Calculate the average score from this JSON data
```

---

### 📋 Planning Agent

**文件**: `agents/planning.py`

**功能**: 规划专家，专注于任务分解和执行计划。

**擅长领域**:
- 将复杂任务拆解为子任务
- 识别依赖关系和前置条件
- 估算工作量和资源需求
- 创建执行计划

**可用工具**: `run_command`, `write_file`

**使用示例**:
```bash
> Create a plan to migrate this codebase to use async/await

> Break down the steps to add unit tests to this project

> Design a roadmap for implementing a new authentication system
```

---

## 快速开始

### 启动多 Agent 系统

```bash
# 安装依赖
uv sync

# 启动多 Agent 模式
uv run python main.py --multi-agent
```

### 交互示例

```
🤖 Multi-Agent Mode (LangGraph)
Available agents: code, file, system, web, data, planning
--------------------------------------------------

You: Create a plan to refactor this codebase
🔄 Processing...
🔀 Router → planning agent

🤖 Assistant:
I'll create a comprehensive refactoring plan for your codebase:

## Phase 1: Assessment (Week 1)
1. Analyze current code structure
2. Identify code smells and technical debt
3. Document dependencies

## Phase 2: Design (Week 2)
1. Design new architecture
2. Define interfaces and contracts
3. Plan migration strategy

## Phase 3: Implementation (Weeks 3-4)
1. Refactor core modules
2. Update tests
3. Update documentation

Would you like me to elaborate on any phase?
```

---

## Agent 特性对比

| Agent | 主要任务 | 工具 | 适用场景 |
|-------|---------|------|---------|
| **Router** | 任务分发 | - | 所有请求的第一步 |
| **Code** | 编程开发 | run_command, write_file | 代码编写、调试、审查 |
| **File** | 文件操作 | run_command, write_file | 文件读写、目录管理 |
| **System** | 系统命令 | run_command | Shell 操作、进程管理 |
| **Web** | 信息搜索 | run_command | 文档查找、资料收集 |
| **Data** | 数据分析 | run_command, write_file | 数据处理、统计分析 |
| **Planning** | 任务规划 | run_command, write_file | 项目规划、任务分解 |

---

## 扩展新 Agent

要添加新的 Specialist Agent，按照以下步骤：

### 1. 创建 Agent 文件

在 `agents/` 目录下创建新文件，例如 `agents/research.py`:

```python
"""Research specialist agent."""

from agents.base import SpecialistAgent


class ResearchAgent(SpecialistAgent):
    """Specialist for academic research and literature review."""

    def __init__(self):
        super().__init__("research")

    def get_system_prompt(self) -> str:
        return """You are a Research Specialist. You excel at:
- Academic literature search
- Paper summarization
- Citation management
- Research methodology

Available tools: run_command, write_file

Guidelines:
1. Use credible academic sources
2. Provide proper citations
3. Summarize key findings
4. Identify research gaps"""


def research_node(state: dict) -> dict:
    """Research agent node."""
    agent = ResearchAgent()
    return agent(state)
```

### 2. 更新 Router

在 `agents/router.py` 的 `Route` 类中添加新选项：

```python
class Route(BaseModel):
    next: Literal[
        "code", "file", "system", "web", "data", "planning", "research"
    ] = Field(
        description="... Include research agent description ..."
    )
```

### 3. 更新 Graph

在 `multi_agent_graph.py` 中添加节点：

```python
from agents.research import research_node

workflow.add_node("research", research_node)
workflow.add_edge("research", END)

# Update conditional edges
workflow.add_conditional_edges(
    "router",
    lambda state: state["next"],
    {
        # ... existing agents ...
        "research": "research",
    }
)
```

### 4. 更新导出

在 `agents/__init__.py` 中导出新节点：

```python
from agents.research import research_node

__all__ = [..., "research_node"]
```

---

## 技术实现

### State 定义

所有 Agent 共享同一个状态定义 (`graph_config.py`):

```python
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add]
    next: str
```

### Agent 基类

所有 Specialist Agents 继承自 `SpecialistAgent` 基类 (`agents/base.py`):

```python
class SpecialistAgent(ABC):
    def __init__(self, name: str, model: str = None):
        # Auto-detect available model
        # Initialize LLM client
        # Load tool schemas

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    def __call__(self, state: dict) -> dict:
        # Build messages with system prompt
        # Invoke LLM
        # Return result
```

### Graph 编译

使用 LangGraph 的 `StateGraph` 构建执行图 (`multi_agent_graph.py`):

```python
workflow = StateGraph(AgentState)
workflow.add_node("router", route_node)
# ... add specialist nodes
workflow.add_conditional_edges("router", ...)
app = workflow.compile(checkpointer=MemorySaver())
```

---

## 相关文档

- [主 README](../README.md)
- [CLAUDE.md](../CLAUDE.md) - 项目开发指南
- [测试文档](../tests/README.md) - 测试套件说明

---

## 许可证

MIT License - 详见 [LICENSE](../LICENSE)
