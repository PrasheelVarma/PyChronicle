# Runtime Tracing Workflow

## Overview

This document explains the complete execution workflow of PyChronicle, from the moment a user starts tracing a Python program until the execution history is visualized in the Terminal User Interface (TUI).

The runtime tracing workflow is the core of the project. It combines Python's runtime tracing capabilities with efficient storage and execution replay to provide a lightweight time-travel debugging experience.

---

# Workflow Overview

```text
            User Python Script
                    │
                    ▼
      pychronicle trace script.py
                    │
                    ▼
         Runtime Tracer Starts
          (sys.settrace)
                    │
                    ▼
      Runtime Events Captured
                    │
                    ▼
       Local Variables Collected
                    │
                    ▼
     Delta Compression Applied
                    │
                    ▼
      Execution Stored in SQLite
                    │
                    ▼
         Program Execution Ends
                    │
                    ▼
        pychronicle ui
                    │
                    ▼
      Timeline Loaded from SQLite
                    │
                    ▼
    Execution State Reconstructed
                    │
                    ▼
      Interactive Terminal UI
```

---

# Step 1 – User Starts Tracing

The tracing process begins when the user executes a Python script through the PyChronicle command-line interface.

Example:

```bash
pychronicle trace test_script.py
```

or

```bash
python -m pychronicle trace test_script.py
```

The CLI validates the input file and initializes the runtime tracing engine.

---

# Step 2 – Runtime Tracer Initialization

PyChronicle enables Python's built-in runtime tracing mechanism using the `sys.settrace()` function.

The tracing callback is automatically invoked by the Python interpreter whenever significant execution events occur.

These events include:

- Function calls
- Line execution
- Function returns
- Exceptions

This allows PyChronicle to observe the execution of the target program in real time.

---

# Step 3 – Runtime Event Capture

As the target program executes, every traced event is intercepted.

For each execution event, PyChronicle records information such as:

- Source file
- Line number
- Function name
- Event type
- Current local variables

Each execution step represents a snapshot of the program at a specific point in time.

---

# Step 4 – Variable Collection

After receiving a runtime event, PyChronicle inspects the current local variables available within the executing frame.

Examples include:

```python
x = 10
y = 20
name = "PyChronicle"
```

These variables represent the current execution state of the program.

Since some Python objects cannot be directly serialized into JSON, PyChronicle sanitizes runtime values before storage.

---

# Step 5 – Delta Compression

Instead of storing every variable after every executed line, PyChronicle compares the current execution state with the previous one.

Only variables that have changed are recorded.

Example:

Previous state:

```text
x = 10
y = 20
```

Current state:

```text
x = 15
y = 20
```

Only the change is stored:

```text
x = 15
```

If a variable is deleted:

```python
del y
```

a deletion marker is stored so that historical reconstruction remains accurate.

This significantly reduces storage requirements while preserving execution history.

---

# Step 6 – SQLite Storage

The compressed execution record is written to the SQLite database.

Each execution record includes information such as:

- Timestamp
- File name
- Line number
- Function name
- Runtime event
- Delta-compressed variable state

PyChronicle uses SQLite because it is lightweight, serverless, and bundled with Python.

Additional optimizations include:

- Write-Ahead Logging (WAL)
- Database indexing
- Transaction batching

These optimizations improve write performance and replay speed.

---

# Step 7 – Program Completion

The tracing process continues until the target Python program finishes execution.

Once execution is complete, the database contains a complete timeline of recorded runtime events.

This timeline can later be replayed without executing the original program again.

---

# Step 8 – Launching the Terminal UI

The user starts the interactive interface using:

```bash
pychronicle ui
```

or

```bash
python -m pychronicle ui
```

The UI loads execution history from the SQLite database.

---

# Step 9 – Timeline Reconstruction

Since only changed variables were stored during execution, complete runtime states must be reconstructed before they can be displayed.

PyChronicle rebuilds the program state by replaying all previously recorded variable changes up to the selected execution step.

This process recreates the exact historical state of the program.

Example:

Stored deltas:

```text
Step 1:
x = 10

Step 2:
y = 20

Step 3:
x = 30
```

Reconstructed state at Step 3:

```text
x = 30
y = 20
```

---

# Step 10 – Interactive Debugging

The reconstructed execution history is displayed through the Terminal User Interface.

The interface allows the user to:

- Navigate the execution timeline
- Inspect local variables
- Monitor watched variables
- View execution snapshots
- Highlight the current source code line

Because the execution history has already been recorded, users can freely move backward and forward through the timeline without rerunning the program.

---

# Runtime Workflow Summary

The complete tracing pipeline can be summarized as:

```text
Python Program
      │
      ▼
sys.settrace()
      │
      ▼
Capture Runtime Events
      │
      ▼
Collect Local Variables
      │
      ▼
Apply Delta Compression
      │
      ▼
Store Execution History
      │
      ▼
SQLite Database
      │
      ▼
Load Timeline
      │
      ▼
Reconstruct Program State
      │
      ▼
Interactive Terminal UI
```

---

# Key Advantages of the Workflow

The runtime tracing workflow provides several advantages:

- Records execution history automatically.
- Stores only modified variables to reduce database size.
- Reconstructs historical program states accurately.
- Eliminates the need to rerun programs for missed debugging points.
- Enables efficient execution replay through a terminal-based interface.
- Maintains a modular pipeline where tracing, storage, reconstruction, and visualization are handled independently.

---

# Summary

PyChronicle's runtime tracing workflow combines Python's `sys.settrace()` functionality with delta-state compression, SQLite storage, state reconstruction, and a Textual-based Terminal User Interface.

This workflow enables developers to inspect historical execution states efficiently, providing a lightweight and practical time-travel debugging experience while keeping storage requirements low and replay performance fast.
