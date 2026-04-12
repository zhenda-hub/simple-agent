"""Configuration loading for the agent."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = {
    "siliconflow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "api_key_env": "SILICONFLOW_API_KEY",
        "model_env": "SILICONFLOW_MODEL",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "api_key_env": "OPENROUTER_API_KEY",
        "model_env": "OPENROUTER_MODEL",
    },
}


@dataclass
class AgentConfig:
    provider: str
    api_key: str
    base_url: str
    model: str
    max_iterations: int = 15
    code_timeout: int = 30


def _auto_detect_provider() -> str:
    """Auto-detect provider based on which API key is set."""
    for name, cfg in PROVIDERS.items():
        key = os.getenv(cfg["api_key_env"], "")
        if key and not key.startswith("sk-your"):
            return name
    raise ValueError(
        "No API key found. Set SILICONFLOW_API_KEY or OPENROUTER_API_KEY in .env or environment."
    )


def load_config() -> AgentConfig:
    """Load configuration from environment variables."""
    provider_env = os.getenv("LLM_PROVIDER", "").lower()
    provider = provider_env if provider_env in PROVIDERS else _auto_detect_provider()

    provider_cfg = PROVIDERS[provider]
    api_key = os.getenv(provider_cfg["api_key_env"], "")
    if not api_key or api_key.startswith("sk-your"):
        raise ValueError(
            f"Missing API key. Set {provider_cfg['api_key_env']} in .env or environment."
        )

    model = os.getenv(provider_cfg["model_env"], "")
    if not model:
        raise ValueError(
            f"Missing model. Set {provider_cfg['model_env']} in .env or environment."
        )

    return AgentConfig(
        provider=provider,
        api_key=api_key,
        base_url=provider_cfg["base_url"],
        model=model,
        max_iterations=int(os.getenv("MAX_ITERATIONS", "15")),
        code_timeout=int(os.getenv("CODE_EXECUTION_TIMEOUT", "30")),
    )
