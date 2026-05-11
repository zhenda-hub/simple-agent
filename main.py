"""CLI entry point for simple-agent."""

import sys
from config import _detect_provider, fetch_free_models, load_config
from formatter import (
    console,
    print_error,
    print_system_message,
    print_welcome,
    prompt_user,
)
from agent import Agent


def select_model() -> str:
    """Fetch free models and let the user pick one."""
    provider, base_url, api_key = _detect_provider()

    with console.status(f"Fetching available models from {provider}..."):
        models = fetch_free_models(provider, base_url, api_key)

    if not models:
        print_error(f"No free models found for {provider}.")
        raise SystemExit(1)

    console.print(f"\n[bold]Available models on {provider}:[/bold]\n")
    for i, m in enumerate(models, 1):
        console.print(f"  [cyan]{i:>3}[/cyan]. {m}")

    console.print()
    while True:
        try:
            choice = console.input("[bold]Select model (number or model ID): [/bold]").strip()
        except (EOFError, KeyboardInterrupt):
            raise SystemExit(0)
        if not choice:
            continue
        # Number selection
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                return models[idx]
            print_error(f"Invalid number. Choose 1-{len(models)}.")
            continue
        # Direct model ID
        if choice in models:
            return choice
        print_error(f"Unknown model: {choice}")


def run_multi_agent():
    """Run the multi-agent system with LangGraph."""
    try:
        from langchain_core.messages import HumanMessage
        from multi_agent_graph import multi_agent_app
    except ImportError as e:
        print_error(f"Multi-agent mode requires LangGraph. Run: uv sync")
        raise SystemExit(1)

    console.print("\n[bold cyan]🤖 Multi-Agent Mode (LangGraph)[/bold cyan]")
    console.print("Available agents: [bold]code[/bold], [bold]file[/bold], [bold]system[/bold]")
    console.print("-" * 50)

    thread_id = "default-session"
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = console.input("\n[bold]You:[/bold] ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("/exit", "/quit"):
                print_system_message("Goodbye!")
                break
            if user_input.lower() == "/help":
                print_system_message("Commands: /exit, /help")
                continue

            # Build initial state
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "next": ""
            }

            # Execute graph
            console.print("\n[dim]🔄 Processing...[/dim]")
            result = multi_agent_app.invoke(initial_state, config=config)

            # Display final response
            final_message = result["messages"][-1]
            console.print(f"\n[bold green]🤖 Assistant:[/bold green]\n{final_message.content}")

        except KeyboardInterrupt:
            print_system_message("Goodbye!")
            break
        except Exception as e:
            print_error(f"Error: {e}")


def main():
    # Check for multi-agent mode
    if len(sys.argv) > 1 and sys.argv[1] in ("--multi-agent", "-m"):
        run_multi_agent()
        return

    try:
        model = select_model()
        config = load_config(model)
    except ValueError as e:
        print_error(str(e))
        raise SystemExit(1)

    agent = Agent(config)
    print_welcome(config)
    print_system_message("Type your message and press Enter. /exit to quit, /clear to reset.\n")

    while True:
        user_input = prompt_user()
        if not user_input:
            continue

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

        agent.run(user_input)


if __name__ == "__main__":
    main()
