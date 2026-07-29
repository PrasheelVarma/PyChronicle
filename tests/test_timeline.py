import unittest
import os
import tempfile
import sqlite3
import json
import pychronicle.tui as tui
import pychronicle.storage as storage
from pychronicle.tui import PyChronicleApp

class TestTimelineReconstruction(unittest.TestCase):
    def setUp(self):
        # Setup temporary database
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        
        self.orig_tui_db = tui.DB_NAME
        self.orig_storage_db = storage.DB_NAME
        
        tui.DB_NAME = self.db_path
        storage.DB_NAME = self.db_path
        
        # Initialize schema
        storage.initialize_database()
        
        # Populate mock timeline data
        # Row 1 (ID 1): x = 10, y = 20, __name__ = "main"
        # Row 2 (ID 2): y = 30, z = 40 (y updated, z added)
        # Row 3 (ID 3): x deleted
        # Row 4 (ID 4): x recreated with 50
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        sample_logs = [
            (1.0, 5, "app.py", "main", "line", json.dumps({"x": 10, "y": 20, "__name__": "main"})),
            (2.0, 6, "app.py", "main", "line", json.dumps({"y": 30, "z": 40})),
            (3.0, 7, "app.py", "main", "line", json.dumps({"x": {"__pychronicle_deleted__": True}})),
            (4.0, 8, "app.py", "main", "line", json.dumps({"x": 50})),
        ]
        
        cursor.executemany("""
            INSERT INTO execution_log (timestamp, line_number, file_name, function_name, event, locals)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_logs)
        self.conn.commit()
        
    def tearDown(self):
        self.conn.close()
        tui.DB_NAME = self.orig_tui_db
        storage.DB_NAME = self.orig_storage_db
        
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_state_reconstruction_dict(self):
        app = PyChronicleApp()
        
        # Reconstruct up to step 1
        state1 = app.reconstruct_state_dict_up_to(1)
        self.assertEqual(state1["x"], 10)
        self.assertEqual(state1["y"], 20)
        self.assertEqual(state1["__name__"], "main")
        self.assertNotIn("z", state1)
        
        # Reconstruct up to step 2 (y is updated, z is added)
        state2 = app.reconstruct_state_dict_up_to(2)
        self.assertEqual(state2["x"], 10)
        self.assertEqual(state2["y"], 30)
        self.assertEqual(state2["z"], 40)
        self.assertEqual(state2["__name__"], "main")
        
        # Reconstruct up to step 3 (x deleted)
        state3 = app.reconstruct_state_dict_up_to(3)
        self.assertNotIn("x", state3)
        self.assertEqual(state3["y"], 30)
        self.assertEqual(state3["z"], 40)
        
        # Reconstruct up to step 4 (x recreated with 50)
        state4 = app.reconstruct_state_dict_up_to(4)
        self.assertEqual(state4["x"], 50)
        self.assertEqual(state4["y"], 30)
        self.assertEqual(state4["z"], 40)

    def test_state_reconstruction_string(self):
        app = PyChronicleApp()
        
        # reconstruct_state_up_to filters out dunders/internal vars and returns formatted JSON
        state1_str = app.reconstruct_state_up_to(1)
        state1 = json.loads(state1_str)
        
        self.assertEqual(state1["x"], 10)
        self.assertEqual(state1["y"], 20)
        # Should not contain __name__ as it is internal
        self.assertNotIn("__name__", state1)
        
        state3_str = app.reconstruct_state_up_to(3)
        state3 = json.loads(state3_str)
        self.assertNotIn("x", state3)
        self.assertEqual(state3["y"], 30)
        self.assertEqual(state3["z"], 40)

if __name__ == "__main__":
    unittest.main()
