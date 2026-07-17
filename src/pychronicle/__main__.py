import os
import typer
from pychronicle.tracer import start_tracing

# Initialize the Typer application
app = typer.Typer(help="PyChronicle: A Python execution tracing and visualization tool.")

@app.command()
def trace(script: str = typer.Argument(..., help="The path to the Python script you want to trace.")):
    """
    Run the tracer on a target script and save the execution history to SQLite.
    """
    # PRE-FLIGHT CHECKS
    if not os.path.exists(script):
        typer.secho(f"❌ Error: The file '{script}' does not exist.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    if not script.endswith(".py"):
        typer.secho(f"❌ Error: '{script}' is not a Python file.", fg=typer.colors.RED, bold=True)
        raise typer.Exit(code=1)

    typer.secho(f"🚀 Starting trace for: {script}...", fg=typer.colors.GREEN)
    start_tracing(script)
    typer.secho("✅ Tracing complete. Data securely logged to the database.", fg=typer.colors.GREEN)

@app.command()
def ui():
    """
    Launch the interactive Textual dashboard.
    """
    typer.secho("🖥️ Launching the PyChronicle TUI...", fg=typer.colors.CYAN)

    # Import inside the command so it only loads if the user asks for the UI
    from pychronicle.tui import PyChronicleApp
    tui_app = PyChronicleApp()
    tui_app.run()

if __name__ == "__main__":
    app()
