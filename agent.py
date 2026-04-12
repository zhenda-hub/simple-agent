"""Core ReAct loop agent."""

import json
from datetime import datetime

from config import AgentConfig
from formatter import print_assistant_message, print_error, print_tool_call, print_tool_result
from llm import LLMClient
from tools import execute_tool, get_tool_schemas


class Agent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = LLMClient(config)
        self.messages: list[dict] = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        tool_names = ", ".join(t["function"]["name"] for t in get_tool_schemas())
        return (
            "You are a helpful AI assistant with access to tools. You can:\n"
            "- Execute Python code in a sandboxed environment\n"
            "- Read, write, and list files on the user's filesystem\n"
            "- Think step-by-step and use tools when needed\n\n"
            "Guidelines:\n"
            "1. When asked to perform computation or file operations, use the appropriate tool.\n"
            "2. When executing code, always consider error handling.\n"
            "3. After receiving tool results, analyze them before responding.\n"
            "4. If a tool fails, explain the error and suggest alternatives.\n"
            "5. Be concise but thorough.\n\n"
            f"Current date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Available tools: {tool_names}"
        )

    def run(self, user_input: str) -> str:
        """Run the ReAct loop for a single user input. Returns final assistant response."""
        self.messages.append({"role": "user", "content": user_input})

        tool_schemas = get_tool_schemas()

        for _ in range(self.config.max_iterations):
            # Build request messages: system + full history
            request_messages = [{"role": "system", "content": self.system_prompt}] + self.messages

            try:
                response = self.llm.chat(request_messages, tools=tool_schemas)
            except Exception as e:
                error_msg = f"API error: {type(e).__name__}: {e}"
                print_error(error_msg)
                return error_msg

            choice = response.choices[0]
            assistant_msg = choice.message

            # Append assistant message to history (may include tool_calls)
            msg_dict: dict = {"role": "assistant"}
            if assistant_msg.content:
                msg_dict["content"] = assistant_msg.content
            if assistant_msg.tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in assistant_msg.tool_calls
                ]
            self.messages.append(msg_dict)

            # If LLM is done (no tool calls), return content
            if choice.finish_reason == "stop":
                return assistant_msg.content or ""

            # Process tool calls
            if assistant_msg.tool_calls:
                for tc in assistant_msg.tool_calls:
                    tool_name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError as e:
                        args = {}
                        result = f"Error: Failed to parse tool arguments: {e}"
                    else:
                        print_tool_call(tool_name, args)
                        result = execute_tool(tool_name, args)

                    is_error = result.startswith("Error:")
                    print_tool_result(tool_name, result, is_error=is_error)

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    })

        return "Warning: Reached maximum number of iterations. The task may be incomplete."

    def clear(self):
        """Clear conversation history."""
        self.messages.clear()
