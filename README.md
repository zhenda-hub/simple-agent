# simple-agent

A simple AI agent with shell command execution, powered by SiliconFlow and OpenRouter.

## Features

- ReAct loop (Think → Act → Observe) with streaming output
- Shell command execution with dangerous command confirmation
- Interactive model selection from provider's free model list
- CLI chat with Rich markdown rendering
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

Select a model from the list, then start chatting.

## Configuration

Edit `.env`:

```env
LLM_PROVIDER=siliconflow    # or "openrouter"
SILICONFLOW_API_KEY=sk-...
```

Only one API key is needed. Model selection is interactive at startup.

## CLI Commands

| Command | Description |
|---------|-------------|
| `/exit` | Exit the agent |
| `/clear` | Clear conversation history |
| `/help` | Show available commands |

## Architecture

```
main.py          → CLI entry + interactive model selection
agent.py         → ReAct loop with streaming response
llm.py           → LLM client (OpenAI SDK, stream=True)
config.py        → Config + provider auto-detect + free model discovery
formatter.py     → Rich terminal output (Windows UTF-8 compatible)
tools/
  __init__.py    → @tool decorator registry
  run_command.py → Shell execution with danger confirmation
```

## License

Apache License 2.0
