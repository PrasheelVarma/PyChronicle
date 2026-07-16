import typer
from pychronicle.tracer import start_tracing

# Initialize the Typer application
app = typer.Typer(help="PyChronicle: A Python execution tracing and visualization tool.")

@app.command()
def trace(script: str = typer.Argument(..., help="The path to the Python script you want to trace.")):
    """
    Run the tracer on a target script and save the execution history to SQLite.
    """
    print(f"🚀 Starting trace for: {script}...")
    start_tracing(script)
    print("✅ Tracing complete. Data securely logged to the database.")

@app.command()
def ui():
    """
    Launch the interactive Textual dashboard.
    """
    print("🖥️ Launching the PyChronicle TUI...")

    # Import inside the command so it only loads if the user asks for the UI
    from pychronicle.tui import PyChronicleApp
    tui_app = PyChronicleApp()
    tui_app.run()

if __name__ == "__main__":
    app()
