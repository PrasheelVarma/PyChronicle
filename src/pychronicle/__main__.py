import os
import typer
from pychronicle.tracer import start_tracing
from pychronicle.storage import reset_database

app = typer.Typer(help="PyChronicle: A Python execution tracing and visualization tool.")

@app.command()
def trace(script: str = typer.Argument(..., help="Path to the Python script.")):
    """Run the tracer on a target script and save the execution history."""
    if not os.path.exists(script):
        typer.secho(f"❌ Error: '{script}' does not exist.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    if not script.endswith(".py"):
        typer.secho(f"❌ Error: '{script}' is not a Python file.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    typer.secho("🧹 Cleaning previous trace data...", fg=typer.colors.YELLOW)
    reset_database()

    typer.secho(f"🚀 Starting trace for: {script}...", fg=typer.colors.GREEN)
    start_tracing(script)
    typer.secho("✅ Tracing complete. Data logged to database.", fg=typer.colors.GREEN)

@app.command()
def ui():
    """Launch the interactive Textual dashboard."""
    typer.secho("🖥️ Launching the PyChronicle TUI...", fg=typer.colors.CYAN)

    from pychronicle.tui import PyChronicleApp
    tui_app = PyChronicleApp()
    tui_app.run()

if __name__ == "__main__":
    app()
