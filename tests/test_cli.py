import unittest
import os
import tempfile
from unittest.mock import patch
from typer.testing import CliRunner

import pychronicle.storage as storage
from pychronicle.__main__ import app

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        # Set a temporary database path
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

    def test_help(self):
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("PyChronicle", result.stdout)
        self.assertIn("trace", result.stdout)
        self.assertIn("ui", result.stdout)

    def test_version(self):
        result = self.runner.invoke(app, ["--version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("PyChronicle v0.1.0", result.stdout)

    def test_trace_missing_file(self):
        result = self.runner.invoke(app, ["trace", "nonexistent_file.py"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("does not exist", result.stdout)

    def test_trace_invalid_extension(self):
        # Create a temp file without .py suffix
        fd, temp_file = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            result = self.runner.invoke(app, ["trace", temp_file])
            self.assertEqual(result.exit_code, 1)
            self.assertIn("is not a Python file", result.stdout)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_trace_success(self):
        # Create a simple python script in current directory
        # Named simply to avoid "pychronicle" filtering in tracer
        temp_script = "temp_cli_test_script.py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write("x = 10\n")
            
        try:
            result = self.runner.invoke(app, ["trace", temp_script])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Tracing complete", result.stdout)
        finally:
            if os.path.exists(temp_script):
                os.remove(temp_script)

    def test_ui_command(self):
        # Mock the textual app run method to avoid opening TUI
        with patch("pychronicle.tui.PyChronicleApp.run") as mock_run:
            result = self.runner.invoke(app, ["ui"])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Launching the PyChronicle TUI", result.stdout)
            mock_run.assert_called_once()

    def test_invalid_command(self):
        result = self.runner.invoke(app, ["invalidcmd"])
        self.assertNotEqual(result.exit_code, 0)

if __name__ == "__main__":
    unittest.main()
