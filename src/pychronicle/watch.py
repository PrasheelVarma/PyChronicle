import sqlite3
import json
from typing import Any, Dict, List, Set, Optional

DB_NAME = "pychronicle_history.db"

def is_deletion_marker(val: Any) -> bool:
    """Check if a value represents a deleted variable marker."""
    if val == "__DELETED__":
        return True
    if isinstance(val, dict) and val.get("__pychronicle_deleted__") is True:
        return True
    return False

class WatchEngine:
    """
    Engine to track and retrieve chronological history of watched variables
    across PyChronicle execution timelines.
    """

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._watched_vars: Set[str] = set()
        self._cached_timeline: List[Dict[str, Any]] = []
        self._watch_history: Dict[str, List[Dict[str, Any]]] = {}
        self._timeline_loaded: bool = False

    def add_watch(self, var_name: str) -> None:
        """Add a variable name to the watch list."""
        if var_name not in self._watched_vars:
            self._watched_vars.add(var_name)
            if self._timeline_loaded:
                self._build_history_for_variable(var_name)

    def remove_watch(self, var_name: str) -> None:
        """Remove a variable name from the watch list."""
        self._watched_vars.discard(var_name)
        self._watch_history.pop(var_name, None)

    def clear_watches(self) -> None:
        """Clear all watched variables and their history."""
        self._watched_vars.clear()
        self._watch_history.clear()

    def get_watched_variables(self) -> List[str]:
        """Return sorted list of currently watched variable names."""
        return sorted(list(self._watched_vars))

    def get_watch_history(self, var_name: str) -> List[Dict[str, Any]]:
        """
        Retrieve chronological history for a watched variable.
        Loads the timeline if not already cached.
        """
        if not self._timeline_loaded:
            self.load_from_db()

        if var_name not in self._watch_history:
            if var_name in self._watched_vars or self._timeline_loaded:
                self._build_history_for_variable(var_name)

        return self._watch_history.get(var_name, [])

    def clear_cache(self) -> None:
        """Invalidate all cached timeline and watch history data."""
        self._cached_timeline.clear()
        self._watch_history.clear()
        self._timeline_loaded = False

    def load_from_db(self, db_name: Optional[str] = None) -> None:
        """
        Load timeline data from SQLite database in a single pass
        and reconstruct watch histories for all currently watched variables.
        """
        target_db = db_name or self.db_name
        self.clear_cache()

        try:
            conn = sqlite3.connect(target_db)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, line_number, file_name, function_name, event, locals
                FROM execution_log
                ORDER BY timestamp ASC, id ASC
            """)

            timeline = []
            for row in cursor.fetchall():
                row_id, ts, line_num, file_name, func_name, event, locals_str = row
                try:
                    delta = json.loads(locals_str)
                except (json.JSONDecodeError, TypeError):
                    delta = {}

                timeline.append({
                    "id": row_id,
                    "timestamp": ts,
                    "line_number": line_num,
                    "file_name": file_name,
                    "function_name": func_name,
                    "event": event,
                    "delta": delta
                })

            conn.close()
            self._cached_timeline = timeline
            self._timeline_loaded = True

            for var in list(self._watched_vars):
                self._build_history_for_variable(var)

        except sqlite3.Error:
            self._cached_timeline = []
            self._timeline_loaded = False

    def load_timeline_entries(self, entries: List[Dict[str, Any]]) -> None:
        """
        Directly load pre-reconstructed timeline entries into the engine.
        Useful when avoiding DB calls if timeline entries are already in memory.
        """
        self.clear_cache()
        self._cached_timeline = entries
        self._timeline_loaded = True
        for var in list(self._watched_vars):
            self._build_history_for_variable(var)

    def _build_history_for_variable(self, var_name: str) -> None:
        """
        Build chronological change history for a single variable
        from the cached timeline entries.
        Only records entries when value changes or variable is deleted/recreated.
        """
        history = []
        last_state = None  # (value, is_deleted)

        for entry in self._cached_timeline:
            delta = entry.get("delta", {})
            if var_name not in delta:
                continue

            raw_val = delta[var_name]
            deleted = is_deletion_marker(raw_val)
            val = None if deleted else raw_val
            current_state = (val, deleted)

            if current_state != last_state:
                last_state = current_state
                history.append({
                    "id": entry["id"],
                    "timestamp": entry["timestamp"],
                    "line_number": entry["line_number"],
                    "file_name": entry["file_name"],
                    "function_name": entry["function_name"],
                    "event": entry["event"],
                    "variable": var_name,
                    "value": val,
                    "is_deleted": deleted
                })

        self._watch_history[var_name] = history
