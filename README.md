# simple-agent

A simple AI agent with tool use and code execution, powered by SiliconFlow and OpenRouter.

## Features

- ReAct loop (Think → Act → Observe)
- Tool calling: file read/write, directory listing, Python code execution
- Sandboxed code execution with timeout and output truncation
- CLI interactive chat with Rich markdown rendering
- Support for SiliconFlow and OpenRouter (OpenAI-compatible API)

## Quick Start

1. Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
uv sync
```

3. Run:

```bash
uv run python main.py
```

## Configuration

Edit `.env`:

```env
LLM_PROVIDER=siliconflow    # or "openrouter"
SILICONFLOW_API_KEY=sk-...
SILICONFLOW_MODEL=Qwen/Qwen2.5-72B-Instruct
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `/exit` | Exit the agent |
| `/clear` | Clear conversation history |
| `/help` | Show available commands |

## Architecture

```
main.py       → CLI entry point
agent.py      → ReAct loop orchestrator
llm.py        → LLM client (OpenAI SDK)
config.py     → Configuration loading
formatter.py  → Rich terminal output
tools/        → Tool registry + implementations
  execute_code.py  → Sandboxed Python execution
  read_file.py     → Read files
  write_file.py    → Write files
  list_directory.py → List directories
```

## License

Apache License 2.0
