# PyChronicle Architecture

## Overview

PyChronicle is a lightweight Python runtime execution tracer and time-travel debugging tool. It records the execution of Python programs, stores runtime history in a SQLite database, and allows developers to replay and inspect historical program states through an interactive Terminal User Interface (TUI).

The architecture is modular, with each component responsible for a specific stage of the tracing pipeline. This separation of responsibilities makes the project easier to maintain, test, and extend.

---

# High-Level Architecture

```text
                     +----------------------+
                     |   Python Script      |
                     | (User Program)       |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Runtime Tracer       |
                     | (sys.settrace)       |
                     +----------+-----------+
                                |
                    Captures execution events
                                |
                                v
                     +----------------------+
                     | Delta Compression    |
                     | Detect Changed Vars  |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | SQLite Storage       |
                     | execution_log table  |
                     +----------+-----------+
                                |
                     Reads execution history
                                |
                                v
                     +----------------------+
                     | State Reconstruction |
                     | Replay Variable State|
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Watch Variables      |
                     | History Engine       |
                     +----------+-----------+
                                |
                                v
                     +----------------------+
                     | Terminal UI          |
                     | (Textual)            |
                     +----------------------+
```

---

# Architectural Components

The project is divided into several independent modules.

Each module performs a single responsibility while communicating with the others through well-defined interfaces.

---

## 1. Parser Module (`parser.py`)

### Purpose

The parser module performs static analysis of Python source code.

Instead of executing the program, it parses the source using Python's built-in Abstract Syntax Tree (AST) module.

### Responsibilities

- Parse Python source files
- Detect variable assignments
- Detect annotated assignments
- Validate Python syntax
- Display parsed information

### Technologies

- `ast`

---

## 2. Runtime Tracer (`tracer.py`)

### Purpose

This is the core engine of PyChronicle.

It uses Python's `sys.settrace()` function to observe the execution of a Python program while it is running.

### Responsibilities

- Monitor execution events
- Detect variable changes
- Capture runtime snapshots
- Filter internal frames
- Prepare execution records
- Perform delta compression

### Captured Events

- line
- call
- return
- exception

---

## 3. Storage Layer (`storage.py`)

### Purpose

The storage layer persists runtime execution history inside a SQLite database.

Rather than storing complete program state after every executed line, it stores only the variables that changed.

### Responsibilities

- Database initialization
- Execution log storage
- Delta-state persistence
- Database reset
- Timeline retrieval

### Optimizations

- SQLite WAL mode
- Database indexing
- Transaction batching

---

## 4. State Reconstruction

### Purpose

Because only variable changes are stored, complete runtime states must be reconstructed when replaying execution.

The reconstruction engine rebuilds the complete variable state by replaying recorded deltas in chronological order.

### Responsibilities

- Replay execution history
- Reconstruct full variable state
- Handle deleted variables
- Cache reconstructed states

---

## 5. Watch Variables Engine (`watch.py`)

### Purpose

The Watch Variables Engine allows users to monitor selected variables throughout the execution timeline.

Instead of viewing every recorded variable, users can focus on variables that are important for debugging.

### Responsibilities

- Add watched variables
- Remove watched variables
- Build variable history
- Detect updates
- Detect deletions
- Suppress duplicate values
- Cache watch history

---

## 6. Terminal User Interface (`tui.py`)

### Purpose

The Terminal User Interface provides an interactive visualization of the recorded execution history.

The interface is built using the Textual framework.

### Main Panels

### Execution Timeline

Displays every recorded execution event.

Users navigate through execution history using the keyboard.

---

### Local Variables

Displays the reconstructed variable state for the currently selected execution step.

---

### Watch Variables

Displays the chronological history of watched variables.

---

### Source Code Viewer

Displays the original Python source code and highlights the currently selected execution line.

---

## 7. Command Line Interface (`__main__.py`)

### Purpose

Provides a simple interface for interacting with PyChronicle from the terminal.

### Available Commands

- Parse Python files
- Trace program execution
- Launch Terminal UI

The CLI is implemented using the Typer framework.

---

# Execution Workflow

The complete execution workflow is illustrated below.

```text
User executes

pychronicle trace program.py

            │
            ▼

Python starts execution

            │
            ▼

sys.settrace() intercepts runtime events

            │
            ▼

Tracer captures local variables

            │
            ▼

Delta Compression detects changes

            │
            ▼

Execution history stored in SQLite

            │
            ▼

User launches

pychronicle ui

            │
            ▼

Execution history loaded

            │
            ▼

State Reconstruction rebuilds variables

            │
            ▼

Interactive Terminal UI displays history
```

---

# Design Principles

The architecture follows several important software engineering principles.

## Modular Design

Each module performs a single responsibility and can be developed independently.

---

## Separation of Concerns

Parsing, tracing, storage, reconstruction, and visualization are implemented as separate layers.

---

## Efficient Storage

Only modified variables are stored using delta-state compression.

This significantly reduces database size compared to storing complete execution snapshots.

---

## Runtime Reconstruction

Historical execution states are reconstructed dynamically rather than stored redundantly.

This balances storage efficiency with replay accuracy.

---

## Extensibility

The modular architecture makes it straightforward to extend the project with additional debugging capabilities in the future.

Examples include:

- Breakpoints
- Timeline filtering
- Exporting trace sessions
- Search functionality
- Multiple trace sessions
- Additional UI themes

---

# Summary

PyChronicle follows a layered architecture consisting of parsing, runtime tracing, storage, state reconstruction, watch variable management, and terminal visualization.

Each module has a clearly defined responsibility, enabling efficient execution tracing, compact storage through delta compression, accurate historical state reconstruction, and an interactive debugging experience within the terminal.
