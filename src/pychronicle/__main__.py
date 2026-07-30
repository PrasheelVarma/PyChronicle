import os
from typing import Optional

import typer

from pychronicle.storage import reset_database
from pychronicle.tracer import start_tracing

VERSION = "0.1.0"


def version_callback(value: bool):
    """Display the current PyChronicle version."""
    if value:
        typer.echo(f"PyChronicle v{VERSION}")
        raise typer.Exit()


app = typer.Typer(
    help="PyChronicle: A Python execution tracing and visualization tool."
)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show the installed PyChronicle version and exit.",
    ),
):
    """
    PyChronicle CLI.
    """
    pass


@app.command()
def trace(script: str = typer.Argument(..., help="Path to the Python script.")):
    """Run the tracer on a target script and save the execution history."""

    if not os.path.exists(script):
        typer.secho(
            f"❌ Error: '{script}' does not exist.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(code=1)

    typer.secho("🧹 Cleaning previous trace data...", fg=typer.colors.YELLOW)
    reset_database()

    typer.secho(f"🚀 Starting trace for: {script}...", fg=typer.colors.GREEN)
    start_tracing(script)

    typer.secho(
        "✅ Tracing complete. Data logged to database.",
        fg=typer.colors.GREEN,
    )


@app.command()
def ui():
    """Launch the interactive Textual dashboard."""

    typer.secho(
        "🖥️ Launching the PyChronicle TUI...",
        fg=typer.colors.CYAN,
    )

    from pychronicle.tui import PyChronicleApp

    PyChronicleApp().run()


if __name__ == "__main__":
    app()
