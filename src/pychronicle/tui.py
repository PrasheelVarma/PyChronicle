import sqlite3
import json
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Horizontal
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.console import Group

DB_NAME = "pychronicle_history.db"

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history."""

    CSS = """
    Horizontal { height: 100%; }
    DataTable { width: 50%; height: 100%; border-right: vkey $accent; }
    #details_pane { width: 50%; height: 100%; padding: 1 2; background: $boost; overflow: auto; }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit application")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            yield DataTable(id="timeline_table")
            yield Static("Select a row in the timeline to see variable details here.", id="details_pane")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#timeline_table", DataTable)
        table.add_columns("ID", "Line", "File", "Function", "Event")
        table.cursor_type = "row"
        table.zebra_stripes = True
        self.load_database_data(table)

    def load_database_data(self, table: DataTable) -> None:
        """Loads lightweight timeline data into the UI without hoarding memory."""
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            # We fetch 'id' so we know exactly where we are in the timeline
            cursor.execute("""
                SELECT id, line_number, file_name, function_name, event
                FROM execution_log
                ORDER BY timestamp ASC
            """)

            for row in cursor.fetchall():
                row_id, line_num, file, func, event = row
                table.add_row(str(row_id), str(line_num), file, func, event, key=str(row_id))

            conn.close()
        except sqlite3.Error as e:
            self.notify(f"Database error: {e}", severity="error")

    def reconstruct_state_up_to(self, target_id: int) -> str:
        """Dynamically reconstructs variables up to the selected point in time."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Query all deltas up to the selected row, utilizing the WAL mode speeds
        cursor.execute("""
            SELECT locals FROM execution_log
            WHERE id <= ? ORDER BY timestamp ASC
        """, (target_id,))

        current_state = {}
        for row in cursor.fetchall():
            delta = json.loads(row[0])
            current_state.update(delta)

        conn.close()
        return json.dumps(current_state, indent=2)

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        row_data = event.data_table.get_row(event.row_key)
        row_id = int(row_data[0])
        line_num = int(row_data[1])
        file_name = row_data[2]
        func_name = row_data[3]

        # ON-DEMAND SCRUBBING: Fetch state only when highlighted
        locals_str = self.reconstruct_state_up_to(row_id)

        # Read the file for the code pane
        code_content = ""
        try:
            target_path = None
            if os.path.exists(file_name):
                target_path = file_name
            else:
                for root, dirs, files in os.walk("."):
                    if file_name in files:
                        target_path = os.path.join(root, file_name)
                        break

            if target_path:
                with open(target_path, "r", encoding="utf-8") as f:
                    code_content = f.read()
            else:
                code_content = f"# Could not locate source file '{file_name}'"
        except Exception as e:
            code_content = f"# Could not read source file: {e}"

        # Generate syntax highlighting
        syntax = Syntax(
            code_content,
            "python",
            theme="monokai",
            line_numbers=True,
            highlight_lines={line_num},
            word_wrap=True
        )

        details_text = (
            f"## ⏱️ Execution Snapshot\n\n"
            f"**File:** {file_name} | **Line:** {line_num}\n"
            f"**Function:** `{func_name}`\n\n"
            f"---\n\n"
            f"### 📦 Local Variables:\n```json\n{locals_str}\n```\n\n"
            f"---\n\n"
            f"### 💻 Source Code:\n"
        )

        details_pane = self.query_one("#details_pane", Static)
        details_pane.update(Group(Markdown(details_text), syntax))

if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
