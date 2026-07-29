import unittest
import os
import tempfile
import sqlite3
import pychronicle.storage as storage

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temp file path but don't open it yet, let initialize_database do it
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        self.orig_db_name = storage.DB_NAME
        storage.DB_NAME = self.db_path

    def tearDown(self):
        storage.stop_tracing_db(commit=False)
        storage.DB_NAME = self.orig_db_name
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_database_creation(self):
        # Database shouldn't exist initially
        self.assertFalse(os.path.exists(self.db_path))
        
        # Initialize
        conn = storage.initialize_database()
        self.assertIsNotNone(conn)
        conn.close()
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check tables exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify variable_history table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='variable_history'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Verify execution_log table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='execution_log'")
        self.assertIsNotNone(cursor.fetchone())
        
        # Verify index
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_execution_timestamp'")
        self.assertIsNotNone(cursor.fetchone())
        
        conn.close()

    def test_insert_variable_state(self):
        conn = storage.initialize_database()
        storage.insert_variable_state(conn, 10, "my_var", "my_value")
        
        cursor = conn.cursor()
        cursor.execute("SELECT line_number, variable_name, serialized_value FROM variable_history")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 10)
        self.assertEqual(row[1], "my_var")
        self.assertEqual(row[2], '"my_value"') # serialized as JSON
        
        conn.close()

    def test_save_execution_state(self):
        storage.save_execution_state({
            "timestamp": 12345.67,
            "line_number": 42,
            "file_name": "test.py",
            "function_name": "foo",
            "event": "line",
            "locals": {"a": 1}
        })
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, line_number, file_name, function_name, event, locals FROM execution_log")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 12345.67)
        self.assertEqual(row[1], 42)
        self.assertEqual(row[2], "test.py")
        self.assertEqual(row[3], "foo")
        self.assertEqual(row[4], "line")
        self.assertEqual(row[5], '{"a": 1}')
        conn.close()

    def test_reset_database(self):
        storage.save_execution_state({
            "timestamp": 12345.67,
            "line_number": 42,
            "file_name": "test.py",
            "function_name": "foo",
            "event": "line",
            "locals": {"a": 1}
        })
        
        # Reset database
        storage.reset_database()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM execution_log")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 0)
        conn.close()

    def test_empty_database_behavior(self):
        storage.reset_database()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM execution_log")
        self.assertEqual(cursor.fetchall(), [])
        conn.close()

if __name__ == "__main__":
    unittest.main()
