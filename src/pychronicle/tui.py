import sqlite3
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Horizontal

DB_NAME = "pychronicle_history.db"

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history."""

    CSS = """
    Horizontal { height: 100%; }
    DataTable { width: 60%; height: 100%; border-right: vkey $accent; }
    #details_pane { width: 40%; height: 100%; padding: 1 2; background: $boost; }
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
        self.row_locals = {}
        table = self.query_one("#timeline_table", DataTable)
        table.add_columns("Line", "File", "Function", "Event")
        table.cursor_type = "row"
        table.zebra_stripes = True
        self.load_database_data(table)

    def load_database_data(self, table: DataTable) -> None:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT line_number, file_name, function_name, event, locals
                FROM execution_log
                ORDER BY timestamp ASC
            """)
            for row in cursor.fetchall():
                line_num, file, func, event, locals_json = row
                # Let Textual generate a unique RowKey automatically
                row_key = table.add_row(str(line_num), file, func, event)
                self.row_locals[row_key] = str(locals_json)
            conn.close()
        except sqlite3.Error as e:
            self.notify(f"Database error: {e}", severity="error")

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        row_data = event.data_table.get_row(event.row_key)
        line_num = int(row_data[0])
        file_name = row_data[1]
        func_name = row_data[2]
        locals_str = getattr(self, "row_locals", {}).get(event.row_key, "{}")

        code_snippet = "Code not available."
        try:
            import os
            target_path = None
            if os.path.exists(file_name):
                target_path = file_name
            else:
                # Recursively lookup the file in the current working directory
                for root, dirs, files in os.walk("."):
                    if file_name in files:
                        target_path = os.path.join(root, file_name)
                        break

            if target_path:
                with open(target_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if 0 <= line_num - 1 < len(lines):
                        code_snippet = lines[line_num - 1].strip()
            else:
                code_snippet = f"Could not locate source file '{file_name}' in workspace."
        except Exception as e:
            code_snippet = f"Could not read source file: {e}"

        details_text = (
            f"## ⏱️ Execution Snapshot\n\n"
            f"**File:** {file_name} | **Line:** {line_num}\n"
            f"**Function:** `{func_name}`\n\n"
            f"---\n\n"
            f"### 💻 Source Code:\n```python\n{code_snippet}\n```\n\n"
            f"---\n\n"
            f"### 📦 Local Variables:\n```json\n{locals_str}\n```"
        )

        details_pane = self.query_one("#details_pane", Static)
        details_pane.update(details_text)


if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
