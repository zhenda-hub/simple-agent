"""Base class for specialist agents."""

from abc import ABC, abstractmethod
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
from tools import get_tool_schemas
from config import load_config


class SpecialistAgent(ABC):
    """Base class for all specialist agents."""

    def __init__(self, name: str, model: str = None):
        self.name = name

        # Use available model if not specified
        if model is None:
            from config import _detect_provider, fetch_free_models
            provider, base_url, api_key = _detect_provider()
            models = fetch_free_models(provider, base_url, api_key)
            if models:
                model = models[0]  # Use first available model
            else:
                model = "Qwen/Qwen2.5-7B-Instruct"  # Fallback

        config = load_config(model)
        self.llm = ChatOpenAI(
            base_url=config.base_url,
            api_key=config.api_key,
            model=config.model,
            temperature=0.7
        )
        self.tools = get_tool_schemas()

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this specialist."""
        pass

    def __call__(self, state: dict) -> dict:
        """Execute the specialist agent logic."""
        from langchain_core.messages import SystemMessage

        messages = state["messages"]

        # Build message list with system prompt at the beginning
        all_messages = [SystemMessage(content=self.get_system_prompt())] + list(messages)

        # Call LLM with tool support
        try:
            response = self.llm.invoke(all_messages, tools=self.tools)
            # Return new message
            return {"messages": [response]}
        except Exception as e:
            # Return error message
            return {"messages": [AIMessage(content=f"Error: {e}")]}
