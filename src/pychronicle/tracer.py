import sys
import runpy
import time
import os

from pychronicle.storage import save_execution_state

def sanitize_value(val):
    """Recursively sanitize a value to make it fully JSON-serializable."""
    if isinstance(val, (int, float, str, bool, type(None))):
        return val
    elif isinstance(val, dict):
        return {str(k): sanitize_value(v) for k, v in val.items()}
    elif isinstance(val, (list, tuple, set)):
        return [sanitize_value(item) for item in val]
    else:
        return f"<{type(val).__name__}>"

def trace_callback(frame, event, arg):
    """
    Traces execution, filters out system calls, and sanitizes local variables.
    """
    if event != "line":
        return trace_callback

    # FILTER: Only log lines from the specific file we are tracing
    filename = frame.f_code.co_filename
    if (
        "site-packages" in filename
        or "pychronicle" in filename
        or "/lib/python" in filename
        or "/usr/lib" in filename
        or filename.startswith("<")
    ):
        return trace_callback

    # SANITIZATION: Strip out non-serializable objects (functions, modules, etc.)
    clean_locals = {}
    for key, value in frame.f_locals.items():
        clean_locals[key] = sanitize_value(value)

    # Capture execution context
    execution_data = {
        "timestamp": time.time(),
        "line_number": frame.f_lineno,
        "file_name": os.path.basename(filename),
        "function_name": frame.f_code.co_name,
        "event": event,
        "locals": clean_locals,
    }

    # Save to database
    save_execution_state(execution_data)

    return trace_callback

def start_tracing(target_script):
    """Enable tracing and execute the target Python file."""
    sys.settrace(trace_callback)
    try:
        runpy.run_path(target_script, run_name="__main__")
    finally:
        stop_tracing()

def stop_tracing():
    """Disable tracing."""
    sys.settrace(None)
