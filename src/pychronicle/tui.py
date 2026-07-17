from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Static("Welcome to PyChronicle Tracer Visualizer", id="message")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
