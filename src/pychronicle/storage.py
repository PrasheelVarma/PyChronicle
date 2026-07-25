import sqlite3
import json
import sys

DB_NAME = "pychronicle_history.db"

_active_conn = None

def start_tracing_db():
    global _active_conn
    if _active_conn is None:
        _active_conn = initialize_database()

def stop_tracing_db(commit: bool | None = None):
    global _active_conn
    if _active_conn:
        try:
            if commit is None:
                commit = (sys.exc_info()[0] is None)
            if commit:
                _active_conn.commit()
            else:
                _active_conn.rollback()
        except sqlite3.Error as e:
            print(f"Database transaction commit/rollback failed: {e}")
        finally:
            _active_conn.close()
            _active_conn = None

def get_connection():
    """Returns a SQLite connection configured with WAL mode for high performance."""
    conn = sqlite3.connect(DB_NAME)
    # Enable Write-Ahead Logging (WAL) for faster concurrent writes and reads
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def initialize_database() -> sqlite3.Connection | None:
    """Initialize SQLite tables and performance indexes for Week 3 storage."""
    try:
        conn = get_connection()
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

        # Week 2 & 3: Execution Tracing with Delta Storage
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

        # Performance Index: Speeds up chronological querying in the TUI
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_execution_timestamp
            ON execution_log (timestamp ASC);
        """)

        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Database initialization failed: {e}")
        return None

def insert_variable_state(conn: sqlite3.Connection, line_number: int, variable_name: str, variable_value) -> None:
    """Stores variable assignment state (Week 1)."""
    try:
        cursor = conn.cursor()
        serialized_value = json.dumps(variable_value, default=str)
        cursor.execute("""
            INSERT INTO variable_history (line_number, variable_name, serialized_value)
            VALUES (?, ?, ?)
        """, (line_number, variable_name, serialized_value))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Variable insertion failed: {e}")

def save_execution_state(data: dict) -> None:
    """Stores tracer execution data (Week 2/3)."""
    global _active_conn
    conn = _active_conn if _active_conn else initialize_database()
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
            json.dumps(data['locals'], default=str)
        ))
        if not _active_conn:
            conn.commit()
    except sqlite3.Error as e:
        print(f"Execution log insertion failed: {e}")
    finally:
        if not _active_conn:
            conn.close()

def init_db():
    """Initializes the database schema."""
    initialize_database()

def log_execution(timestamp, line_number, file_name, function_name, event, locals_dict):
    """Saves a single execution frame to the database."""
    save_execution_state({
        "timestamp": timestamp,
        "line_number": line_number,
        "file_name": file_name,
        "function_name": function_name,
        "event": event,
        "locals": locals_dict
    })

def reset_database():
    """Wipes the execution_log table clean before a new trace starts."""
    conn = get_connection()
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
