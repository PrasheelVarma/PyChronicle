import sqlite3
import json
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable

# Point to your database
DB_NAME = "pychronicle_history.db"

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit application")
    ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the table with headers and data when app mounts."""
        table = self.query_one(DataTable)
        # Setup table columns
        table.add_columns("Line", "File", "Function", "Event", "Local Variables")
        table.cursor_type = "row"
        table.zebra_stripes = True

        # Load the data
        self.load_database_data(table)

    def load_database_data(self, table: DataTable) -> None:
        """Fetch fresh logs from the SQLite database."""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Select execution logs ordered by time
            cursor.execute("""
                SELECT line_number, file_name, function_name, event, locals
                FROM execution_log
                ORDER BY timestamp ASC
            """)

            for row in cursor.fetchall():
                line_num, file, func, event, locals_json = row

                # Sanitize the locals dictionary string for the UI display
                locals_str = str(locals_json)
                locals_display = locals_str[:50] + "..." if len(locals_str) > 50 else locals_str

                # Add the row to the table
                table.add_row(str(line_num), file, func, event, locals_display)

            conn.close()
        except sqlite3.Error as e:
            self.notify(f"Database error: {e}", severity="error")

if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
