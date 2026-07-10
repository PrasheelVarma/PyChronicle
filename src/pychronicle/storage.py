import json
import sqlite3
from sqlite3 import Connection

DB_NAME = "pychronicle_history.db"


def initialize_database() -> Connection | None:
    """
    Initialize the SQLite database and create the variable_history table
    if it does not already exist.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variable_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT NOT NULL
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
    """
    Serialize the variable information and store it in the database.
    """
    try:
        cursor = conn.cursor()

        serialized_value = json.dumps(variable_value)

        cursor.execute("""
            INSERT INTO variable_history (
                line_number,
                variable_name,
                serialized_value
            )
            VALUES (?, ?, ?)
        """, (
            line_number,
            variable_name,
            serialized_value
        ))

        conn.commit()

        print(f"✓ Logged '{variable_name}' (Line {line_number})")

    except sqlite3.Error as e:
        print(f"Database insertion failed: {e}")

    except TypeError as e:
        print(f"Serialization failed: {e}")
