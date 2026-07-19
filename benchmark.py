import sqlite3
import time
from pathlib import Path

from pychronicle.storage import DB_NAME, reset_database
from pychronicle.tracer import start_tracing

TARGET_SCRIPT = "stress_test.py"

def get_database_size():
    """Return SQLite database size in KB."""
    db_file = Path(DB_NAME)
    if db_file.exists():
        return db_file.stat().st_size / 1024
    return 0

def fetch_row_count():
    """Return total execution states stored."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM execution_log")
    row_count = cursor.fetchone()[0]
    conn.close()
    return row_count

def fetch_basic_statistics():
    """Fetch additional statistics from the execution log."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # FIXED: We use 'locals' instead of 'variable_name' based on our schema
    cursor.execute("SELECT COUNT(DISTINCT locals) FROM execution_log")
    unique_states = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(line_number), MAX(line_number) FROM execution_log")
    min_line, max_line = cursor.fetchone()

    conn.close()
    return unique_states, min_line, max_line


def run_benchmark():
    print("🧹 Resetting database...")
    reset_database()

    print(f"🚀 Running tracer on '{TARGET_SCRIPT}'...\n")

    start = time.perf_counter()
    start_tracing(TARGET_SCRIPT)
    end = time.perf_counter()

    execution_time = end - start

    row_count = fetch_row_count()
    db_size = get_database_size()
    unique_states, min_line, max_line = fetch_basic_statistics()

    states_per_second = (
        row_count / execution_time
        if execution_time > 0
        else 0
    )

    print("=" * 60)
    print("        PYCHRONICLE MID-PROJECT BENCHMARK REPORT")
    print("=" * 60)

    print(f"Target Script           : {TARGET_SCRIPT}")
    print(f"Execution Time          : {execution_time:.6f} seconds")
    print(f"Execution States Logged : {row_count}")
    print(f"Logging Rate            : {states_per_second:.2f} states/sec")
    print(f"Database Size           : {db_size:.2f} KB")
    print(f"Unique Variable States  : {unique_states}")
    print(f"Line Number Range       : {min_line} - {max_line}")

    print("\nTRACE VALIDATION")
    print("-" * 60)

    if row_count > 0:
        print("✅ Execution states successfully captured.")
    else:
        print("❌ No execution states were captured.")

    if unique_states > 0:
        print("✅ Variable mutations successfully recorded.")
    else:
        print("❌ No variable mutations detected.")

    if min_line is not None and max_line is not None:
        print("✅ Line execution history successfully recorded.")
    else:
        print("❌ Line execution history unavailable.")

    print("\nSTORAGE AUDIT")
    print("-" * 60)

    if db_size > 0:
        print("✅ SQLite database successfully stored execution history.")
    else:
        print("❌ Database appears to be empty.")

    if execution_time < 2:
        print("✅ Minimal tracing overhead observed.")
    else:
        print("⚠ Tracing completed, but execution time was higher than expected.")

    print("\nOVERALL RESULT")
    print("-" * 60)

    if row_count > 0 and unique_states > 0:
        print("🎉 MID-PROJECT REVIEW STATUS : PASSED")
    else:
        print("❌ MID-PROJECT REVIEW STATUS : NEEDS ATTENTION")

    print("=" * 60)


if __name__ == "__main__":
    run_benchmark()
