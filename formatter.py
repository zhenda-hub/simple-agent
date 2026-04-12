"""Rich-based terminal output formatting."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from config import AgentConfig

console = Console()


def print_welcome(config: AgentConfig):
    """Display startup banner."""
    console.print()
    console.print(
        Panel(
            f"[bold]Provider:[/bold] {config.provider}\n"
            f"[bold]Model:[/bold]    {config.model}",
            title="[bold cyan]Simple Agent[/bold cyan]",
            border_style="cyan",
        )
    )


def print_user_message(content: str):
    """Display user input."""
    console.print()
    console.print(f"[bold green]You>[/bold green] {content}")


def print_assistant_message(content: str):
    """Render assistant response as Markdown."""
    console.print()
    console.print(Markdown(content))


def print_tool_call(name: str, arguments: dict):
    """Display tool invocation."""
    args_str = str(arguments)
    console.print()
    console.print(
        Panel(
            Syntax(args_str, "python", theme="monokai", word_wrap=True),
            title=f"[bold yellow]Tool: {name}[/bold yellow]",
            border_style="yellow",
        )
    )


def print_tool_result(name: str, result: str, is_error: bool = False):
    """Display tool result."""
    style = "red" if is_error else "dim"
    # Truncate for display
    display = result if len(result) <= 2000 else result[:2000] + "\n... (truncated)"
    console.print(
        Panel(
            Text(display),
            title=f"[{style}]Result: {name}[/{style}]",
            border_style=style,
        )
    )


def print_system_message(content: str):
    """Dim system-level messages."""
    console.print(f"[dim]{content}[/dim]")


def print_error(content: str):
    """Bold red error messages."""
    console.print(f"[bold red]Error:[/bold red] {content}")


def prompt_user() -> str:
    """Prompt for user input. Raises SystemExit on Ctrl+C/EOF."""
    try:
        text = console.input("[bold green]You>[/bold green] ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit(0)
    return text
