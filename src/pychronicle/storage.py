import sqlite3
import json

DB_NAME = "pychronicle_history.db"

def init_db():
    """Initializes the database schema."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            line_number INTEGER,
            file_name TEXT,
            function_name TEXT,
            event TEXT,
            locals TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_execution(timestamp, line_number, file_name, function_name, event, locals_dict):
    """Saves a single execution frame to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Serialize the locals dictionary safely
    locals_json = json.dumps(locals_dict, default=str)

    cursor.execute("""
        INSERT INTO execution_log (timestamp, line_number, file_name, function_name, event, locals)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, line_number, file_name, function_name, event, locals_json))

    conn.commit()
    conn.close()

def reset_database():
    """Wipes the execution_log table clean before a new trace starts."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS execution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            line_number INTEGER,
            file_name TEXT,
            function_name TEXT,
            event TEXT,
            locals TEXT
        )
    """)
    cursor.execute("DELETE FROM execution_log")
    conn.commit()
    conn.close()
