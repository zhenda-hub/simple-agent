"""CLI entry point for simple-agent."""

from config import load_config
from formatter import (
    console,
    print_assistant_message,
    print_error,
    print_system_message,
    print_user_message,
    print_welcome,
    prompt_user,
)
from agent import Agent


def main():
    try:
        config = load_config()
    except ValueError as e:
        print_error(str(e))
        raise SystemExit(1)

    agent = Agent(config)
    print_welcome(config)
    print_system_message("Type your message and press Enter. /exit to quit, /clear to reset.\n")

    while True:
        user_input = prompt_user()
        if not user_input:
            print_system_message("Goodbye!")
            break

        lower = user_input.lower()
        if lower in ("/exit", "/quit"):
            print_system_message("Goodbye!")
            break
        if lower == "/clear":
            agent.clear()
            print_system_message("Conversation cleared.")
            continue
        if lower == "/help":
            print_system_message("Commands: /exit, /clear, /help")
            continue

        print_user_message(user_input)
        response = agent.run(user_input)
        if response:
            print_assistant_message(response)


if __name__ == "__main__":
    main()
