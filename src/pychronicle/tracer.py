import sys
import runpy
import time
import os
from pychronicle.storage import save_execution_state, start_tracing_db, stop_tracing_db

# Global state to track previous variables for delta compression
_previous_locals = {}

def sanitize_value(val, seen=None):
    """Recursively sanitize a value to make it fully JSON-serializable."""
    if seen is None:
        seen = set()

    val_id = id(val)
    if val_id in seen:
        return f"<CircularReference to {type(val).__name__}>"

    if isinstance(val, (int, float, str, bool, type(None))):
        return val
    elif isinstance(val, dict):
        seen.add(val_id)
        res = {str(k): sanitize_value(v, seen) for k, v in val.items()}
        seen.remove(val_id)
        return res
    elif isinstance(val, (list, tuple, set)):
        seen.add(val_id)
        res = [sanitize_value(item, seen) for item in val]
        seen.remove(val_id)
        return res
    else:
        return f"<{type(val).__name__}>"

def trace_callback(frame, event, arg):
    """
    Traces execution, filters out system calls, and performs Delta Compression.
    """
    global _previous_locals

    if event != "line":
        return trace_callback

    # FILTER: Only log lines from the specific file we are tracing
    filename = frame.f_code.co_filename
    if filename.startswith("<"):
        return trace_callback
    if "site-packages" in filename or "/lib/python" in filename or "/usr/lib" in filename:
        return trace_callback
    
    tracer_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(filename).startswith(tracer_dir):
        return trace_callback

    # SANITIZATION
    current_locals = {}
    for key, value in frame.f_locals.items():
        current_locals[key] = sanitize_value(value)

    # DELTA COMPRESSION: Only store what actually changed
    delta = {}
    for key, val in current_locals.items():
        if key not in _previous_locals or _previous_locals[key] != val:
            delta[key] = val

    for key in _previous_locals:
        if key not in current_locals:
            delta[key] = {"__pychronicle_deleted__": True}

    # Update global state for the next line execution
    _previous_locals = current_locals.copy()

    # Capture execution context (saving only the delta)
    execution_data = {
        "timestamp": time.time(),
        "line_number": frame.f_lineno,
        "file_name": os.path.basename(filename),
        "function_name": frame.f_code.co_name,
        "event": event,
        "locals": delta,
    }

    # Save to database
    save_execution_state(execution_data)

    return trace_callback

def start_tracing(target_script):
    """Enable tracing and execute the target Python file."""
    global _previous_locals
    _previous_locals = {}  # Reset state for a fresh trace

    start_tracing_db()

    sys.settrace(trace_callback)
    try:
        runpy.run_path(target_script, run_name="__main__")
    finally:
        stop_tracing()
        stop_tracing_db()

def stop_tracing():
    """Disable tracing."""
    sys.settrace(None)
