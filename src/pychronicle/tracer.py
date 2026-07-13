import sys
import runpy
import time

from pychronicle.storage import save_execution_state


def trace_callback(frame, event, arg):
    """
    This function is automatically called by Python
    whenever a trace event occurs.
    """

    # For Week 2, record only line execution events.
    if event != "line":
        return trace_callback

    execution_data = {
        "timestamp": time.time(),
        "line_number": frame.f_lineno,
        "file_name": frame.f_code.co_filename,
        "function_name": frame.f_code.co_name,
        "event": event,
        "locals": dict(frame.f_locals),
    }

    save_execution_state(execution_data)

    return trace_callback


def start_tracing(target_script):
    """
    Enable tracing and execute the target Python file.
    """

    sys.settrace(trace_callback)

    try:
        runpy.run_path(target_script, run_name="__main__")
    finally:
        stop_tracing()


def stop_tracing():
    """
    Disable tracing.
    """

    sys.settrace(None)
