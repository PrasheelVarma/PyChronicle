import unittest
import sqlite3
import json
import os
import tempfile
from pychronicle.watch import WatchEngine, is_deletion_marker

class TestWatchEngine(unittest.TestCase):

    def setUp(self):
        # Create a temporary SQLite database
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                line_number INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                function_name TEXT NOT NULL,
                event TEXT NOT NULL,
                locals TEXT NOT NULL
            )
        """)

        # Insert sample timeline entries
        # Step 1: x = 10, y = "hello"
        # Step 2: y = "hello" (duplicate for y), z = 100
        # Step 3: x = 20 (x changed)
        # Step 4: del x (x deleted)
        # Step 5: x = 30 (x recreated)
        sample_logs = [
            (1.0, 10, "test.py", "main", "line", json.dumps({"x": 10, "y": "hello"})),
            (2.0, 11, "test.py", "main", "line", json.dumps({"y": "hello", "z": 100})),
            (3.0, 12, "test.py", "main", "line", json.dumps({"x": 20})),
            (4.0, 13, "test.py", "main", "line", json.dumps({"x": {"__pychronicle_deleted__": True}})),
            (5.0, 14, "test.py", "main", "line", json.dumps({"x": 30})),
        ]

        cursor.executemany("""
            INSERT INTO execution_log (timestamp, line_number, file_name, function_name, event, locals)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_logs)
        conn.commit()
        conn.close()

        self.engine = WatchEngine(db_name=self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_deletion_marker_check(self):
        self.assertTrue(is_deletion_marker("__DELETED__"))
        self.assertTrue(is_deletion_marker({"__pychronicle_deleted__": True}))
        self.assertFalse(is_deletion_marker("some_string"))
        self.assertFalse(is_deletion_marker(123))

    def test_watch_list_management(self):
        self.assertEqual(self.engine.get_watched_variables(), [])
        self.engine.add_watch("x")
        self.engine.add_watch("y")
        self.assertEqual(self.engine.get_watched_variables(), ["x", "y"])

        self.engine.remove_watch("x")
        self.assertEqual(self.engine.get_watched_variables(), ["y"])

        self.engine.clear_watches()
        self.assertEqual(self.engine.get_watched_variables(), [])

    def test_watch_history_and_duplicate_suppression(self):
        self.engine.add_watch("y")
        history_y = self.engine.get_watch_history("y")

        # Step 1 set y="hello", Step 2 also had y="hello" (consecutive duplicate).
        # history_y should contain only 1 entry.
        self.assertEqual(len(history_y), 1)
        self.assertEqual(history_y[0]["value"], "hello")
        self.assertEqual(history_y[0]["line_number"], 10)

    def test_watch_history_with_deletion_and_recreation(self):
        self.engine.add_watch("x")
        history_x = self.engine.get_watch_history("x")

        # Steps for x:
        # Step 1: x = 10
        # Step 3: x = 20
        # Step 4: del x (is_deleted=True, value=None)
        # Step 5: x = 30
        self.assertEqual(len(history_x), 4)

        self.assertEqual(history_x[0]["value"], 10)
        self.assertFalse(history_x[0]["is_deleted"])

        self.assertEqual(history_x[1]["value"], 20)
        self.assertFalse(history_x[1]["is_deleted"])

        self.assertIsNone(history_x[2]["value"])
        self.assertTrue(history_x[2]["is_deleted"])

        self.assertEqual(history_x[3]["value"], 30)
        self.assertFalse(history_x[3]["is_deleted"])

    def test_adding_watch_after_timeline_loaded(self):
        # Trigger timeline load by querying 'y'
        self.engine.add_watch("y")
        self.engine.get_watch_history("y")

        # Now add 'x' after timeline is already loaded
        self.engine.add_watch("x")
        history_x = self.engine.get_watch_history("x")
        self.assertEqual(len(history_x), 4)

    def test_load_timeline_entries_directly(self):
        engine = WatchEngine()
        entries = [
            {
                "id": 1,
                "timestamp": 1.0,
                "line_number": 5,
                "file_name": "app.py",
                "function_name": "foo",
                "event": "line",
                "delta": {"a": 42}
            },
            {
                "id": 2,
                "timestamp": 2.0,
                "line_number": 6,
                "file_name": "app.py",
                "function_name": "foo",
                "event": "line",
                "delta": {"a": 42}  # duplicate
            },
            {
                "id": 3,
                "timestamp": 3.0,
                "line_number": 7,
                "file_name": "app.py",
                "function_name": "foo",
                "event": "line",
                "delta": {"a": 99}
            }
        ]
        engine.add_watch("a")
        engine.load_timeline_entries(entries)
        history = engine.get_watch_history("a")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["value"], 42)
        self.assertEqual(history[1]["value"], 99)

if __name__ == "__main__":
    unittest.main()
