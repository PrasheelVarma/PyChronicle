import sqlite3
import time
import json
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

    cursor.execute("SELECT COUNT(DISTINCT locals) FROM execution_log")
    unique_deltas = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(line_number), MAX(line_number) FROM execution_log")
    min_line, max_line = cursor.fetchone()

    conn.close()
    return unique_deltas, min_line, max_line

def measure_replay_speed():
    """Simulates UI timeline scrubbing to measure state reconstruction speed."""
    start = time.perf_counter()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT locals FROM execution_log ORDER BY timestamp ASC")

    reconstructed_state = {}
    for row in cursor.fetchall():
        delta = json.loads(row[0])
        reconstructed_state.update(delta)

    conn.close()
    end = time.perf_counter()
    return end - start


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
    unique_deltas, min_line, max_line = fetch_basic_statistics()
    replay_time = measure_replay_speed()

    states_per_second = (
        row_count / execution_time
        if execution_time > 0
        else 0
    )

    print("=" * 60)
    print("        PYCHRONICLE PERFORMANCE BENCHMARK REPORT")
    print("=" * 60)

    print(f"Target Script           : {TARGET_SCRIPT}")
    print(f"Execution Write Time    : {execution_time:.6f} seconds")
    print(f"State Replay Fetch Time : {replay_time:.6f} seconds")
    print(f"Execution Deltas Logged : {row_count}")
    print(f"Tracing Throughput      : {states_per_second:.2f} states/sec")
    print(f"Compressed DB Size      : {db_size:.2f} KB")
    print(f"Unique Delta States     : {unique_deltas}")
    print(f"Line Number Range       : {min_line} - {max_line}")

    print("\nWEEK 3 DELTA-COMPRESSION AUDIT")
    print("-" * 60)

    if replay_time < 0.5:
        print("✅ Timeline state reconstruction is highly optimized (< 500ms).")
    else:
        print("⚠ Timeline reconstruction is slower than expected.")

    if unique_deltas > 0:
        print("✅ Variable delta mutations successfully recorded.")
    else:
        print("❌ No variable mutations detected. Check delta logic.")

    print("\nOVERALL RESULT")
    print("-" * 60)

    if row_count > 0 and replay_time < 1.0:
        print("🎉 SYSTEM BENCHMARK STATUS : SUCCESS")
    else:
        print("❌ SYSTEM BENCHMARK STATUS : FAILED")

    print("=" * 60)

if __name__ == "__main__":
    run_benchmark()
