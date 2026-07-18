import sqlite3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Horizontal

# Point to your database
DB_NAME = "pychronicle_history.db"

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history."""

    # Inline CSS to create the split-screen layout
    CSS = """
    Horizontal {
        height: 100%;
    }
    DataTable {
        width: 65%;
        height: 100%;
        border-right: vkey $accent;
    }
    #details_pane {
        width: 35%;
        height: 100%;
        padding: 1 2;
        background: $boost;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit application")
    ]

    def compose(self) -> ComposeResult:
        """Create the split-screen layout."""
        yield Header(show_clock=True)
        # Use a Horizontal container to place the table and details side-by-side
        with Horizontal():
            yield DataTable(id="timeline_table")
            yield Static("Select a row in the timeline to see variable details here.", id="details_pane")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the table with headers and data when app mounts."""
        table = self.query_one("#timeline_table", DataTable)
        table.add_columns("Line", "File", "Function", "Event")
        table.cursor_type = "row"
        table.zebra_stripes = True

        self.load_database_data(table)

    def load_database_data(self, table: DataTable) -> None:
        """Fetch logs from the SQLite database."""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            # Fetch data including the locals, but we won't show locals in the table anymore
            cursor.execute("""
                SELECT line_number, file_name, function_name, event, locals
                FROM execution_log
                ORDER BY timestamp ASC
            """)

            for row in cursor.fetchall():
                line_num, file, func, event, locals_json = row
                # We store the locals string secretly in the row key/data so we can grab it later
                table.add_row(str(line_num), file, func, event, key=str(locals_json))

            conn.close()
        except sqlite3.Error as e:
            self.notify(f"Database error: {e}", severity="error")

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """This event fires every time you move the cursor up or down the table."""
        # Get the row data
        row_data = event.data_table.get_row(event.row_key)
        line_num = row_data[0]
        func_name = row_data[2]

        # The locals string was stored in the row_key value
        locals_str = event.row_key.value

        # Format the right-side panel text
        details_text = f"## ⏱️ Execution Snapshot\n\n**Line:** {line_num}\n**Function:** {func_name}\n\n---\n\n### 📦 Local Variables:\n{locals_str}"

        # Update the details pane
        details_pane = self.query_one("#details_pane", Static)
        details_pane.update(details_text)

if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
