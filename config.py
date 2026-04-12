"""Configuration loading for the agent."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDERS = {
    "siliconflow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "api_key_env": "SILICONFLOW_API_KEY",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
    },
}

# Keywords to exclude when listing SiliconFlow chat models
_NON_CHAT_KEYWORDS = (
    "embedding", "reranker", "vl", "ocr", "tts", "asr", "image",
    "edit", "kolors", "lora", "i2v", "t2v", "speech", "voice",
    "captioner", "bge",
)


@dataclass
class AgentConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    max_iterations: int = 15
    code_timeout: int = 30


def _detect_provider() -> tuple[str, str, str]:
    """Detect which provider has a valid API key. Returns (name, base_url, api_key)."""
    # 1. Honor explicit LLM_PROVIDER setting
    explicit = os.getenv("LLM_PROVIDER", "").lower()
    if explicit in PROVIDERS:
        key = os.getenv(PROVIDERS[explicit]["api_key_env"], "")
        if key and not key.startswith("sk-your"):
            return explicit, PROVIDERS[explicit]["base_url"], key

    # 2. Auto-detect from available keys
    for name, cfg in PROVIDERS.items():
        key = os.getenv(cfg["api_key_env"], "")
        if key and not key.startswith("sk-your"):
            return name, cfg["base_url"], key

    raise ValueError(
        "No API key found. Set SILICONFLOW_API_KEY or OPENROUTER_API_KEY in .env or environment."
    )


def fetch_free_models(provider: str, base_url: str, api_key: str) -> list[str]:
    """Fetch free/available model IDs from provider's /v1/models endpoint."""
    client = OpenAI(base_url=base_url, api_key=api_key)
    models = client.models.list()

    if provider == "openrouter":
        # OpenRouter: free models have ":free" suffix
        return sorted(m.id for m in models.data if ":free" in m.id)

    # SiliconFlow: filter out Pro/ prefix and non-chat models
    result = []
    for m in models.data:
        mid = m.id
        if mid.startswith("Pro/"):
            continue
        if any(kw in mid.lower() for kw in _NON_CHAT_KEYWORDS):
            continue
        result.append(mid)
    return sorted(result)


def load_config(model: str) -> AgentConfig:
    """Load configuration with the selected model."""
    provider, base_url, api_key = _detect_provider()
    return AgentConfig(
        provider=provider,
        api_key=api_key,
        base_url=base_url,
        model=model,
        max_iterations=int(os.getenv("MAX_ITERATIONS", "15")),
        code_timeout=int(os.getenv("CODE_EXECUTION_TIMEOUT", "30")),
    )
