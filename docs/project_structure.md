# Project Structure

## Overview

PyChronicle follows a modular project structure where each component has a specific responsibility.

Instead of placing all logic inside a single file, the project separates parsing, runtime tracing, database management, user interface, and testing into independent modules.

This organization improves readability, maintainability, and future scalability.

---

# Repository Structure

```text
PyChronicle/
│
├── docs/
├── src/
│   └── pychronicle/
│
├── tests/
│
├── benchmark.py
├── stress_test.py
├── test_script.py
│
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore
```

Each directory serves a different purpose within the project.

---

# docs/

The **docs/** directory contains the project documentation.

It explains the internal architecture, workflows, implementation details, testing strategy, benchmarking, and future improvements.

Example documents include:

- Architecture
- Runtime Workflow
- Parser
- Runtime Tracer
- Storage
- Testing
- Benchmark
- Development Log

This folder is intended for developers who want to understand the project in depth.

---

# src/

The **src/** directory contains the actual source code of PyChronicle.

Using the `src` layout prevents accidental imports during development and follows modern Python packaging practices.

```text
src/
└── pychronicle/
```

---

# pychronicle/

This package contains all core modules of the project.

```text
pychronicle/
│
├── __init__.py
├── __main__.py
├── parser.py
├── tracer.py
├── storage.py
├── watch.py
└── tui.py
```

Each module has a dedicated responsibility.

---

# __init__.py

Marks the directory as a Python package.

It also allows PyChronicle to expose package-level metadata when required.

---

# __main__.py

Acts as the project's entry point.

This module initializes the command-line interface using **Typer** and dispatches commands such as:

- parser
- trace
- ui
- version
- help

Running

```bash
python -m pychronicle
```

starts execution from this file.

---

# parser.py

Responsible for static analysis.

Uses Python's **AST (Abstract Syntax Tree)** module to:

- Parse Python source code.
- Detect assignment statements.
- Detect annotated assignments.
- Validate syntax.

The parser does not execute the program.

---

# tracer.py

The Runtime Tracer is the core of PyChronicle.

Responsibilities include:

- Runtime tracing using `sys.settrace()`
- Capturing execution events
- Recording local variables
- Delta comparison
- Variable deletion detection
- Sending execution history to the storage layer

This module powers the time-travel debugging functionality.

---

# storage.py

Responsible for interacting with SQLite.

Main responsibilities include:

- Creating the database
- Writing execution history
- Reading timeline entries
- Delta storage
- State reconstruction support
- Database optimization

This module isolates database logic from the rest of the application.

---

# watch.py

Implements the Watch Variables engine.

Responsibilities include:

- Managing watched variables
- Recording variable history
- Duplicate suppression
- Deletion tracking
- Timeline synchronization

This module enables focused inspection of selected variables.

---

# tui.py

Implements the Terminal User Interface using the **Textual** framework.

The interface allows users to:

- Navigate execution history
- View source code
- Inspect variables
- Replay execution
- Monitor watched variables

This module provides the visual debugging experience.

---

# tests/

The **tests/** directory contains the automated unit test suite.

```text
tests/
│
├── test_cli.py
├── test_database.py
├── test_timeline.py
├── test_tracing.py
└── test_watch.py
```

Each file validates a different subsystem.

---

# test_cli.py

Tests the command-line interface.

Example checks include:

- Help command
- Version command
- Invalid commands
- Invalid files
- Trace command
- UI command

---

# test_database.py

Tests the SQLite storage layer.

Verifies:

- Database creation
- Data insertion
- Database reset
- Empty database handling

---

# test_tracing.py

Tests the runtime tracing engine.

Scenarios include:

- Variable assignments
- Loops
- Functions
- Recursion
- Exceptions
- Complex data types
- Variable deletion

---

# test_timeline.py

Validates timeline reconstruction.

Ensures delta-compressed execution history is reconstructed correctly.

---

# test_watch.py

Tests the Watch Variables engine.

Validates:

- Watch list management
- Variable history
- Duplicate suppression
- Variable recreation
- Timeline loading

---

# benchmark.py

Measures project performance.

It evaluates:

- Runtime tracing speed
- Replay speed
- Database size
- Delta compression efficiency
- Storage optimization

This script is intended for performance analysis.

---

# stress_test.py

Generates a large number of execution events.

Used to verify:

- Runtime tracing stability
- Timeline reconstruction
- SQLite performance
- Replay performance

This simulates larger workloads than normal test programs.

---

# test_script.py

A simple Python program used for manual testing.

It allows developers to:

- Trace execution
- Launch the Terminal UI
- Observe variable changes
- Verify Watch Variables

This script is useful during development and demonstrations.

---

# pyproject.toml

Defines the project configuration.

It includes:

- Project metadata
- Dependencies
- Package information
- Console entry point

This enables installation using modern Python packaging tools.

---

# requirements.txt

Lists project dependencies required for development and execution.

Examples include:

- Textual
- Typer

---

# README.md

Provides the primary project documentation.

It contains:

- Project overview
- Features
- Installation
- Usage
- Testing
- Development progress

This file serves as the project's main entry point for users.

---

# .gitignore

Specifies files and directories that should not be tracked by Git.

Examples include:

- Virtual environments
- Python cache files
- SQLite databases
- Temporary files

---

# Overall Architecture

The repository follows a layered architecture.

```text
Python Source File
        │
        ▼
Parser (AST)
        │
        ▼
Runtime Tracer
        │
        ▼
Storage Layer
        │
        ▼
SQLite Database
        │
        ▼
State Reconstruction
        │
        ▼
Watch Engine
        │
        ▼
Terminal User Interface
```

Each module performs a single responsibility while collaborating with the others to provide the complete time-travel debugging workflow.

---

# Summary

The PyChronicle project is organized into well-defined modules that separate parsing, runtime tracing, storage, visualization, and testing.

This modular architecture improves maintainability, simplifies development, and makes the project easier to extend as new debugging features are introduced.
