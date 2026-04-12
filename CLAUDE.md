# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                      # Install dependencies
uv run python main.py        # Run the agent
uv run python -c "..."       # Run one-off scripts
```

No test framework or linter configured yet.

## Architecture

ReAct-loop AI agent with streaming output. Single tool (`run_command`) for shell execution.

```
main.py          → CLI loop + interactive model selection
agent.py         → ReAct loop: stream LLM response → dispatch tool calls → repeat
llm.py           → OpenAI SDK wrapper, stream=True, supports SiliconFlow + OpenRouter
config.py        → _detect_provider() honors LLM_PROVIDER env var, falls back to auto-detect
                   fetch_free_models() queries /v1/models API for available models
formatter.py     → Rich console with force_terminal=True (Windows UTF-8 fix)
tools/__init__.py → @tool decorator registry + get_tool_schemas() + execute_tool()
tools/run_command.py → shell=True execution, dangerous commands need user confirmation
```

**ReAct flow**: User input → append to messages → stream LLM response (print text live, accumulate tool_call deltas) → if tool_calls: execute → append tool result → loop.

**Tool registration**: Add `@tool(name, description, parameters)` to a function in `tools/`, then import the module in `tools/__init__.py` bottom.

**Provider auto-detect**: Checks `LLM_PROVIDER` env var first, then scans for valid API keys. Both providers use OpenAI-compatible API (`base_url` + `api_key`).

**Windows**: `formatter.py` wraps stdout/stderr with UTF-8 to avoid GBK emoji crashes.
