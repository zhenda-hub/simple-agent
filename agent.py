"""Core ReAct loop agent."""

import json
from datetime import datetime

from config import AgentConfig
from formatter import (
    print_error,
    print_tool_call,
    print_tool_result,
    console,
)
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
            "You are a helpful AI assistant with access to the following tools:\n"
            "- run_command: Execute any shell command on the user's Windows system\n"
            "- write_file: Create or overwrite a file with given content (handles Unicode well)\n"
            "- Think step-by-step and use tools when needed\n\n"
            "Guidelines:\n"
            "1. When asked to perform computation or file operations, execute the appropriate command.\n"
            "2. When executing code, always consider error handling.\n"
            "3. After receiving tool results, analyze them before responding.\n"
            "4. If a tool fails, explain the error and suggest alternatives.\n"
            "5. Be concise but thorough.\n"
            "6. Always write files to the output/ directory. Create it if it doesn't exist.\n\n"
            f"Current date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Available tools: {tool_names}"
        )

    def _stream_response(self, tool_schemas):
        """Stream LLM response, printing text in real-time. Returns (content, tool_calls, finish_reason)."""
        request_messages = [{"role": "system", "content": self.system_prompt}] + self.messages

        try:
            stream = self.llm.chat_stream(request_messages, tools=tool_schemas)
        except Exception as e:
            error_msg = f"API error: {type(e).__name__}: {e}"
            print_error(error_msg)
            return error_msg, [], "stop"

        content_parts: list[str] = []
        tool_calls_map: dict[int, dict] = {}
        finish_reason = None

        for chunk in stream:
            delta = chunk.choices[0].delta

            # Print text immediately, char by char
            if delta.content:
                content_parts.append(delta.content)
                console.print(delta.content, end="", highlight=False)

            # Accumulate tool call deltas
            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    if idx not in tool_calls_map:
                        tool_calls_map[idx] = {"id": "", "name": "", "arguments": ""}
                    if tc_delta.id:
                        tool_calls_map[idx]["id"] += tc_delta.id
                    if tc_delta.function:
                        if tc_delta.function.name:
                            tool_calls_map[idx]["name"] += tc_delta.function.name
                        if tc_delta.function.arguments:
                            tool_calls_map[idx]["arguments"] += tc_delta.function.arguments

            if chunk.choices[0].finish_reason:
                finish_reason = chunk.choices[0].finish_reason

        # Final newline after streaming text
        if content_parts:
            console.print()

        content = "".join(content_parts)
        tool_calls = [tool_calls_map[i] for i in sorted(tool_calls_map)]
        return content, tool_calls, finish_reason or "stop"

    def run(self, user_input: str):
        """Run the ReAct loop for a single user input."""
        self.messages.append({"role": "user", "content": user_input})
        tool_schemas = get_tool_schemas()

        for _ in range(self.config.max_iterations):
            console.print()
            content, tool_calls, finish_reason = self._stream_response(tool_schemas)

            # Build assistant message for history
            msg_dict: dict = {"role": "assistant"}
            if content:
                msg_dict["content"] = content
            if tool_calls:
                msg_dict["tool_calls"] = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": tc["arguments"],
                        },
                    }
                    for tc in tool_calls
                ]
            self.messages.append(msg_dict)

            if finish_reason == "stop":
                return

            # Process tool calls
            for tc in tool_calls:
                tool_name = tc["name"]
                raw_args = tc["arguments"]
                try:
                    args = json.loads(raw_args)
                except json.JSONDecodeError as e:
                    result = f"Error: Invalid tool arguments JSON: {e}\nRaw arguments: {raw_args[:500]}"
                    print_tool_result(tool_name, result, is_error=True)
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": result,
                    })
                    continue
                print_tool_call(tool_name, args)
                result = execute_tool(tool_name, args)

                is_error = result.startswith("Error:")
                print_tool_result(tool_name, result, is_error=is_error)

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result,
                })

        print_error("Warning: Reached maximum number of iterations. The task may be incomplete.")

    def clear(self):
        """Clear conversation history."""
        self.messages.clear()
