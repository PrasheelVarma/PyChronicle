import sqlite3
import json

DB_NAME = "pychronicle_history.db"

def initialize_database():
    """Initializes the localized historical record tracking table."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS variable_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT NOT NULL
            )
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Database Initialization Failure: {e}")
        return None

def insert_variable_state(conn, line_number, var_name, var_value):
    """Safely serializes a Python variable and inserts it into the database."""
    try:
        cursor = conn.cursor()
        serialized_val = json.dumps(var_value)
        cursor.execute('''
            INSERT INTO variable_history (line_number, variable_name, serialized_value)
            VALUES (?, ?, ?)
        ''', (line_number, var_name, serialized_val))
        conn.commit()
        print(f"Logged: {var_name} at line {line_number}")
    except Exception as e:
        print(f"Failed to insert variable state: {e}")
