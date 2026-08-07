# Runtime Tracer

## Overview

The Runtime Tracer is the core component of PyChronicle.

Its responsibility is to observe a Python program while it is executing, capture runtime events, record changes in local variables, and store the execution history for later analysis.

Unlike the Parser module, which performs static analysis without executing code, the Runtime Tracer works during program execution and records the actual behavior of the application.

The tracer is implemented using Python's built-in `sys.settrace()` function.

---

# Purpose

The Runtime Tracer provides the foundation for time-travel debugging.

Its primary responsibilities are to:

- Execute the target Python program.
- Monitor execution line by line.
- Capture runtime events.
- Record local variable changes.
- Store execution history in SQLite.
- Support historical replay through the Terminal User Interface.

Without the tracer, PyChronicle would have no runtime information to analyze.

---

# What is Runtime Tracing?

Runtime tracing is the process of monitoring a program while it executes.

Instead of only seeing the final output, the tracer records every important execution step.

For example:

```python
x = 10
y = 20
z = x + y
```

Normally, Python simply executes these statements.

With runtime tracing enabled, PyChronicle records:

```text
Line 1
x = 10

↓

Line 2
y = 20

↓

Line 3
z = 30
```

This recorded execution history can later be replayed inside the Terminal User Interface.

---

# Why sys.settrace()?

PyChronicle uses Python's built-in `sys.settrace()` function because it allows a custom tracing function to receive callbacks during program execution.

The tracing function is automatically invoked whenever Python executes certain runtime events.

This provides complete visibility into how the program behaves while it is running.

---

# Runtime Events

The tracing engine receives several types of execution events.

Common events include:

- Line execution
- Function calls
- Function returns
- Exceptions

Each event contains useful runtime information such as:

- Current file
- Line number
- Function name
- Local variables
- Event type

This information is stored for later analysis.

---

# Tracing Workflow

The runtime tracing process follows the workflow below.

```text
Python Program
        │
        ▼
Enable sys.settrace()
        │
        ▼
Program Executes
        │
        ▼
Runtime Event Generated
        │
        ▼
Capture Local Variables
        │
        ▼
Compare With Previous State
        │
        ▼
Store Delta in SQLite
        │
        ▼
Continue Execution
```

---

# Capturing Variable State

Whenever a traced event occurs, the tracer reads the current local variables from the executing frame.

Example:

```python
x = 10
y = 20
```

Captured state:

```text
{
    "x": 10,
    "y": 20
}
```

These values represent the current execution state at that point in time.

---

# Delta Compression

Rather than storing the complete execution state after every line, PyChronicle stores only variables that have changed.

Example:

Execution Step 1

```text
x = 10
```

Stored:

```text
x = 10
```

Execution Step 2

```text
x = 10
y = 20
```

Stored:

```text
y = 20
```

Execution Step 3

```text
x = 30
y = 20
```

Stored:

```text
x = 30
```

This significantly reduces storage requirements while preserving complete execution history.

---

# Variable Deletion

The tracer also detects when variables are removed.

Example:

```python
x = 10

del x
```

Instead of losing this information, the tracer records a deletion marker.

During replay, the reconstruction engine removes the variable at the correct point in history.

---

# Serialization

Python variables may contain many different data types.

Before storing them in SQLite, values are serialized into a consistent format.

Examples include:

- Numbers
- Strings
- Lists
- Dictionaries
- Objects (where supported)

Serialization ensures that execution history can be written safely to the database.

---

# Database Storage

Every runtime event produces a timeline entry.

Typical information stored includes:

- Timestamp
- Source filename
- Line number
- Function name
- Runtime event
- Delta-compressed local variables

These records form the execution history used by the replay engine.

---

# Error Handling

The tracer is designed to handle common runtime situations safely.

Examples include:

- Invalid Python files
- Missing files
- Runtime exceptions
- Unsupported values
- Empty execution history

This improves the reliability of the tracing process.

---

# Role in the Project

Within the overall architecture, the Runtime Tracer acts as the bridge between program execution and persistent storage.

```text
Python Program
        │
        ▼
Runtime Tracer
        │
        ▼
Delta Compression
        │
        ▼
SQLite Database
        │
        ▼
State Reconstruction
        │
        ▼
Terminal User Interface
```

Every component that follows depends on the execution history recorded by the tracer.

---

# Advantages

The Runtime Tracer provides several benefits:

- Captures actual program behavior.
- Records variable history automatically.
- Enables historical execution replay.
- Reduces storage using delta compression.
- Integrates directly with SQLite.
- Supports Watch Variables.
- Powers the Terminal User Interface.

These capabilities make runtime debugging significantly easier than repeatedly rerunning a program with traditional print statements.

---

# Limitations

The tracer focuses on recording execution history and is intentionally lightweight.

It does not currently provide features such as:

- Breakpoint management
- Remote debugging
- Multi-process tracing
- Multi-thread synchronization
- Graphical debugging interface

These features are considered possible future enhancements.

---

# Summary

The Runtime Tracer is the central component of PyChronicle.

Using Python's `sys.settrace()` function, it records runtime execution events, captures local variable changes, applies delta compression, and stores execution history in SQLite.

This recorded history forms the foundation for state reconstruction, Watch Variables, and the Terminal User Interface, enabling a lightweight time-travel debugging experience.
