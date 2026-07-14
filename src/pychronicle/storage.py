import json
import sqlite3
from sqlite3 import Connection

DB_NAME = "pychronicle_history.db"

def initialize_database() -> Connection | None:
    """
    Initialize the SQLite database. Creates both the variable_history
    table (for Week 1) and the execution_log table (for Week 2).
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Week 1: Variable Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variable_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT NOT NULL
            )
        """)

        # Week 2: Execution Tracing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS execution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                line_number INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                function_name TEXT NOT NULL,
                event TEXT NOT NULL,
                locals TEXT NOT NULL
            )
        """)

        conn.commit()
        return conn

    except sqlite3.Error as e:
        print(f"Database initialization failed: {e}")
        return None

def insert_variable_state(
    conn: Connection,
    line_number: int,
    variable_name: str,
    variable_value
) -> None:
    """Stores variable assignment state (Week 1)."""
    try:
        cursor = conn.cursor()
        serialized_value = json.dumps(variable_value)
        cursor.execute("""
            INSERT INTO variable_history (line_number, variable_name, serialized_value)
            VALUES (?, ?, ?)
        """, (line_number, variable_name, serialized_value))
        conn.commit()
        print(f"✓ Logged variable '{variable_name}' at line {line_number}")
    except sqlite3.Error as e:
        print(f"Variable insertion failed: {e}")

def save_execution_state(data: dict) -> None:
    """Stores tracer execution data (Week 2)."""
    conn = initialize_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO execution_log (
                timestamp, line_number, file_name, function_name, event, locals
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['timestamp'],
            data['line_number'],
            data['file_name'],
            data['function_name'],
            data['event'],
            json.dumps(data['locals'])
        ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Execution log insertion failed: {e}")
    finally:
        conn.close()
