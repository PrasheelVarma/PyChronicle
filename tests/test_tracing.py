import unittest
import os
import tempfile
import sqlite3
import json
import pychronicle.storage as storage
import pychronicle.tracer as tracer

class TestTracing(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for the tests
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

        self.orig_db_name = storage.DB_NAME
        storage.DB_NAME = self.db_path
        
        # Initialize schema
        storage.initialize_database()

    def tearDown(self):
        tracer.stop_tracing()
        storage.stop_tracing_db(commit=False)
        storage.DB_NAME = self.orig_db_name
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def run_trace_script(self, code_content: str):
        # Write to a temporary file in current directory with a generic name
        # to ensure it is not filtered by the "pychronicle" check
        temp_filename = "temp_trace_target.py"
        with open(temp_filename, "w", encoding="utf-8") as f:
            f.write(code_content)
        
        try:
            storage.reset_database()
            tracer._previous_locals = {}
            
            # Start tracing (runpy will execute the file)
            tracer.start_tracing(temp_filename)
            
            # Fetch the execution logs
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT line_number, function_name, event, locals 
                FROM execution_log 
                ORDER BY timestamp ASC, id ASC
            """)
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    "line_number": row[0],
                    "function_name": row[1],
                    "event": row[2],
                    "locals": json.loads(row[3])
                })
            conn.close()
            return logs
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def test_variable_assignments_and_updates(self):
        code = """x = 10
y = 20
x = 30
"""
        logs = self.run_trace_script(code)
        
        # The tracer records line executions.
        # Line 1: x = 10 (before execution: locals = {})
        # Line 2: y = 20 (before execution: x is 10, y is not set. Delta: {"x": 10})
        # Line 3: x = 30 (before execution: x is 10, y is 20. Delta: {"y": 20})
        # After Line 3: script ends, so no subsequent line event is fired for final state in global scope.
        
        self.assertTrue(len(logs) >= 2)
        # Check first logged delta
        self.assertEqual(logs[1]["locals"], {"x": 10})
        # Check second logged delta
        self.assertEqual(logs[2]["locals"], {"y": 20})

    def test_variable_deletion(self):
        code = """x = 10
y = 20
del x
z = 30
"""
        logs = self.run_trace_script(code)
        
        # Line 1: x = 10
        # Line 2: y = 20 (delta has x=10)
        # Line 3: del x (delta has y=20)
        # Line 4: z = 30 (delta has x deleted: {"x": {"__pychronicle_deleted__": True}})
        
        # We look for the deletion marker in the logs
        deleted_markers = [log["locals"] for log in logs if "x" in log["locals"]]
        
        found_deletion = False
        for locs in deleted_markers:
            val = locs["x"]
            if isinstance(val, dict) and val.get("__pychronicle_deleted__") is True:
                found_deletion = True
                break
                
        self.assertTrue(found_deletion)

    def test_loops(self):
        code = """total = 0
for i in range(3):
    total += i
"""
        logs = self.run_trace_script(code)
        
        # Verify that we logged loop steps and variables total and i change over time
        loop_locals = [log["locals"] for log in logs]
        
        # Verify we captured updates to total and i
        updated_totals = [locs["total"] for locs in loop_locals if "total" in locs]
        updated_is = [locs["i"] for locs in loop_locals if "i" in locs]
        
        self.assertTrue(len(updated_totals) > 0)
        self.assertTrue(len(updated_is) > 0)

    def test_functions_and_nested_functions(self):
        code = """def outer(a):
    def inner(b):
        c = a + b
        return c
    val = inner(5)
    return val

outer(10)
"""
        logs = self.run_trace_script(code)
        
        # Verify functions and nested functions are traced
        func_names = [log["function_name"] for log in logs]
        self.assertIn("outer", func_names)
        self.assertIn("inner", func_names)

    def test_recursion(self):
        code = """def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

fact(3)
"""
        logs = self.run_trace_script(code)
        
        # Verify recursion is traced (multiple logs in "fact" function)
        fact_logs = [log for log in logs if log["function_name"] == "fact"]
        self.assertTrue(len(fact_logs) >= 3)

    def test_exceptions(self):
        # We need to handle exception propagation in start_tracing
        code = """
try:
    x = 1
    raise ValueError("test error")
except ValueError:
    y = 2
"""
        # Tracing should complete successfully since the target script catches its own exception
        logs = self.run_trace_script(code)
        
        # Verify both block parts are traced
        lines = [log["line_number"] for log in logs]
        self.assertTrue(len(lines) > 2)

    def test_complex_data_types(self):
        code = """d = {"a": 1, "b": [2, 3]}
lst = [1, (2, 3)]
tup = (4, 5)
unused = 0
"""
        logs = self.run_trace_script(code)
        
        # Look for serialized complex types in local variables
        found_d = False
        found_lst = False
        found_tup = False
        
        for log in logs:
            locs = log["locals"]
            if "d" in locs:
                self.assertEqual(locs["d"], {"a": 1, "b": [2, 3]})
                found_d = True
            if "lst" in locs:
                self.assertEqual(locs["lst"], [1, [2, 3]]) # tuple is sanitized to list
                found_lst = True
            if "tup" in locs:
                self.assertEqual(locs["tup"], [4, 5]) # tuple is sanitized to list
                found_tup = True
                
        self.assertTrue(found_d)
        self.assertTrue(found_lst)
        self.assertTrue(found_tup)

    def test_classes_and_objects(self):
        code = """class Dummy:
    pass

obj = Dummy()
unused = 0
"""
        logs = self.run_trace_script(code)
        
        found_obj = False
        for log in logs:
            locs = log["locals"]
            if "obj" in locs:
                self.assertEqual(locs["obj"], "<Dummy>")
                found_obj = True
                
        self.assertTrue(found_obj)

if __name__ == "__main__":
    unittest.main()
