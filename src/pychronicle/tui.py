import sqlite3
import json
import os
from typing import Any, Dict

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Label
from textual.containers import Horizontal, Vertical
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.console import Group

from pychronicle.watch import WatchEngine

DB_NAME = "pychronicle_history.db"

def is_internal_variable(var_name: str) -> bool:
    """Filter out Python dunder and internal execution variables."""
    if var_name.startswith("__") and var_name.endswith("__"):
        return True
    internal_names = {
        "__builtins__", "__loader__", "__package__", "__cached__",
        "__spec__", "__name__", "__doc__", "__file__", "__annotations__"
    }
    return var_name in internal_names

def format_variable_value(val: Any) -> str:
    """Format variable values cleanly for UI presentation."""
    if val is None:
        return "None"
    if isinstance(val, (dict, list, tuple)):
        try:
            return json.dumps(val, ensure_ascii=False)
        except Exception:
            return str(val)
    return str(val)

class PyChronicleApp(App):
    """A Textual app to visualize Python execution history with Watch Engine support."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state_cache = {}
        self.watch_engine = WatchEngine()
        self._current_target_id = None

    CSS = """
    #main_container {
        height: 100%;
        width: 100%;
    }

    #left_column {
        width: 50%;
        height: 100%;
        padding: 0 1;
        border-right: solid $accent;
    }

    #right_column {
        width: 50%;
        height: 100%;
        padding: 0 1;
    }

    .pane_title {
        background: $accent;
        color: $text;
        text-style: bold;
        padding: 0 1;
        margin-top: 0;
        margin-bottom: 0;
    }

    #timeline_table {
        height: 50%;
        border: solid $accent-darken-2;
    }

    #watch_table {
        height: 50%;
        border: solid $accent-darken-2;
    }

    #locals_table {
        height: 40%;
        border: solid $accent-darken-2;
    }

    #details_pane {
        height: 60%;
        background: $boost;
        padding: 1;
        overflow: auto;
        border: solid $accent-darken-2;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("w", "toggle_watch", "Toggle Watch (W)"),
        ("q", "quit", "Quit application")
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main_container"):
            with Vertical(id="left_column"):
                yield Label("⏱️ Execution Timeline", classes="pane_title")
                yield DataTable(id="timeline_table")
                yield Label("👁️ Watched Variables History", classes="pane_title")
                yield DataTable(id="watch_table")
            with Vertical(id="right_column"):
                yield Label("📦 Local Variables (Press 'W' to toggle watch)", classes="pane_title")
                yield DataTable(id="locals_table")
                yield Label("💻 Source Code & Snapshot", classes="pane_title")
                yield Static("Select a row in the timeline to see variable details here.", id="details_pane")
        yield Footer()

    def on_mount(self) -> None:
        timeline = self.query_one("#timeline_table", DataTable)
        timeline.add_columns("ID", "Line", "File", "Function", "Event")
        timeline.cursor_type = "row"
        timeline.zebra_stripes = True

        locals_tbl = self.query_one("#locals_table", DataTable)
        locals_tbl.add_columns("Watch", "Variable", "Value")
        locals_tbl.cursor_type = "row"
        locals_tbl.zebra_stripes = True

        watch_tbl = self.query_one("#watch_table", DataTable)
        watch_tbl.add_columns("Variable", "Line", "Function", "Value")
        watch_tbl.cursor_type = "row"
        watch_tbl.zebra_stripes = True

        self.load_database_data(timeline)
        self.update_watch_pane()

    def load_database_data(self, table: DataTable) -> None:
        """Loads lightweight timeline data into the UI without hoarding memory."""
        self._state_cache.clear()
        self.watch_engine.clear_cache()
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
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

    def reconstruct_state_dict_up_to(self, target_id: int) -> dict:
        """Dynamically reconstructs variables dictionary up to target_id."""
        if target_id in self._state_cache:
            return self._state_cache[target_id]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT locals FROM execution_log
            WHERE id <= ? ORDER BY timestamp ASC
        """, (target_id,))

        current_state = {}
        for row in cursor.fetchall():
            try:
                delta = json.loads(row[0])
            except Exception:
                delta = {}
            for k, v in delta.items():
                if v == "__DELETED__" or (isinstance(v, dict) and v.get("__pychronicle_deleted__") is True):
                    current_state.pop(k, None)
                else:
                    current_state[k] = v

        conn.close()
        self._state_cache[target_id] = current_state
        return current_state

    def reconstruct_state_up_to(self, target_id: int) -> str:
        """Backwards-compatible JSON string state reconstruction."""
        current_state = self.reconstruct_state_dict_up_to(target_id)
        user_vars = {k: v for k, v in current_state.items() if not is_internal_variable(k)}
        return json.dumps(user_vars, indent=2)

    def update_locals_table(self, locals_dict: dict) -> None:
        """Update Local Variables DataTable with user variables and watch status."""
        table = self.query_one("#locals_table", DataTable)
        table.clear()

        watched_set = set(self.watch_engine.get_watched_variables())
        user_vars = {k: v for k, v in locals_dict.items() if not is_internal_variable(k)}

        if not user_vars:
            table.add_row("-", "No user local variables", "-", key="empty")
            return

        for var_name, val in sorted(user_vars.items()):
            is_watched = var_name in watched_set
            watch_mark = "⭐ Watched" if is_watched else "  "
            val_str = format_variable_value(val)
            table.add_row(watch_mark, var_name, val_str, key=var_name)

    def update_watch_pane(self) -> None:
        """Update Watch Variables DataTable with chronological watch history."""
        table = self.query_one("#watch_table", DataTable)
        table.clear()

        watched_vars = self.watch_engine.get_watched_variables()
        if not watched_vars:
            table.add_row("-", "-", "-", "No watched variables. Select a local variable and press 'W'.", key="empty")
            return

        all_entries = []
        for var_name in watched_vars:
            history = self.watch_engine.get_watch_history(var_name)
            all_entries.extend(history)

        all_entries.sort(key=lambda x: (x.get("timestamp", 0), x.get("id", 0)))

        if not all_entries:
            table.add_row("-", "-", "-", "No changes recorded for watched variables.", key="empty_history")
            return

        for entry in all_entries:
            var_name = entry["variable"]
            line_str = f"L{entry['line_number']}"
            func_str = entry["function_name"]
            if entry["is_deleted"]:
                val_str = "❌ [DELETED]"
            else:
                val_str = format_variable_value(entry["value"])

            row_key = f"{var_name}_{entry['id']}"
            table.add_row(var_name, line_str, func_str, val_str, key=row_key)

    def action_toggle_watch(self) -> None:
        """Toggle watch status for the currently selected local variable."""
        locals_table = self.query_one("#locals_table", DataTable)
        if locals_table.row_count == 0:
            self.notify("No variables available in Local Variables table.", severity="warning")
            return

        try:
            row_index = locals_table.cursor_row
            row_data = locals_table.get_row_at(row_index)
            var_name = row_data[1]
        except Exception:
            var_name = None

        if not var_name or var_name in ("No user local variables", "-"):
            self.notify("Please select a valid local variable in Local Variables section.", severity="warning")
            return

        watched = self.watch_engine.get_watched_variables()
        if var_name in watched:
            self.watch_engine.remove_watch(var_name)
            self.notify(f"Unwatched variable '{var_name}'", severity="info")
        else:
            self.watch_engine.add_watch(var_name)
            self.notify(f"Watching variable '{var_name}' ⭐", severity="info")

        if self._current_target_id is not None:
            locals_dict = self.reconstruct_state_dict_up_to(self._current_target_id)
            self.update_locals_table(locals_dict)
        self.update_watch_pane()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlighting in timeline table."""
        if event.data_table.id != "timeline_table":
            return

        row_data = event.data_table.get_row(event.row_key)
        row_id = int(row_data[0])
        line_num = int(row_data[1])
        file_name = row_data[2]
        func_name = row_data[3]

        self._current_target_id = row_id

        locals_dict = self.reconstruct_state_dict_up_to(row_id)
        self.update_locals_table(locals_dict)
        self.update_watch_pane()

        locals_str = self.reconstruct_state_up_to(row_id)

        code_content = ""
        try:
            target_path = None
            if not hasattr(self, "_file_path_cache"):
                self._file_path_cache = {}

            if os.path.exists(file_name):
                target_path = file_name
            else:
                if file_name not in self._file_path_cache:
                    found_path = None
                    for root, dirs, files in os.walk("."):
                        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "venv", ".venv", "__pycache__", "site-packages")]
                        if file_name in files:
                            found_path = os.path.join(root, file_name)
                            break
                    self._file_path_cache[file_name] = found_path
                
                target_path = self._file_path_cache.get(file_name)

            if target_path:
                with open(target_path, "r", encoding="utf-8") as f:
                    code_content = f.read()
            else:
                code_content = f"# Could not locate source file '{file_name}'"
        except Exception as e:
            code_content = f"# Could not read source file: {e}"

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
            f"### 💻 Source Code:\n"
        )

        details_pane = self.query_one("#details_pane", Static)
        details_pane.update(Group(Markdown(details_text), syntax))

if __name__ == "__main__":
    app = PyChronicleApp()
    app.run()
