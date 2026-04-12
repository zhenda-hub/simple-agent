"""LLM client abstraction over OpenAI SDK."""

from openai import OpenAI

from config import AgentConfig


class LLMClient:
    """Thin wrapper around openai.OpenAI for chat completions with tool support."""

    def __init__(self, config: AgentConfig):
        kwargs: dict = {
            "base_url": config.base_url,
            "api_key": config.api_key,
        }
        if config.provider == "openrouter":
            kwargs["default_headers"] = {
                "HTTP-Referer": "https://github.com/simple-agent",
                "X-Title": "simple-agent",
            }
        self.client = OpenAI(**kwargs)
        self.model = config.model

    def chat_stream(self, messages: list[dict], tools: list[dict] | None = None):
        """Stream a chat completion request. Yields chunks."""
        kwargs: dict = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        if tools:
            kwargs["tools"] = tools
        return self.client.chat.completions.create(**kwargs)
