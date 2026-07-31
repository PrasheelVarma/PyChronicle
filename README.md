# PyChronicle

> A Python runtime execution tracer, variable history analyzer, and lightweight time-travel debugging tool built using `sys.settrace`, SQLite, Textual, and Typer.

PyChronicle is a Python developer tool that records the execution of Python programs, captures runtime state changes, and stores execution history inside a SQLite database for later analysis.

Unlike traditional debugging, where developers often need to rerun a program after missing a bug, PyChronicle preserves the execution history so that previous execution states can be explored through an interactive terminal interface.

This project is being developed as part of the **Infotact Advanced Python Development Internship**.

---

# 🚀 Project Overview

Traditional Python debugging techniques such as print statements and debuggers only expose the **current execution state** of a program.

If a bug is missed or the program finishes execution, the developer generally has to execute the program again.

PyChronicle approaches debugging differently.

Instead of only showing the current state, it continuously records execution history while the program is running. After execution completes, the recorded history can be replayed to inspect how variables changed over time.

The complete workflow is:

```text
Python Script
      │
      ▼
AST Parser
      │
      ▼
Runtime Tracer (sys.settrace)
      │
      ▼
SQLite Storage
      │
      ▼
State Reconstruction
      │
      ▼
Interactive Terminal UI (Textual)
```

PyChronicle combines several advanced Python concepts including:

- Abstract Syntax Tree (AST) Parsing
- Runtime Execution Tracing
- SQLite Database Storage
- Delta State Compression
- Dynamic State Reconstruction
- Terminal User Interface Development
- Python CLI Packaging

---
<Features>

# 📂 Project Structure

```text
PyChronicle/
│
├── src/
│   └── pychronicle/
│       ├── __init__.py
│       ├── __main__.py
│       ├── parser.py
│       ├── tracer.py
│       ├── storage.py
│       ├── tui.py
│       └── watch.py
│
├── tests/
│   ├── test_cli.py
│   ├── test_database.py
│   ├── test_timeline.py
│   ├── test_tracing.py
│   ├── test_watch.py
│   └── test1.py
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

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/PrasheelVarma/PyChronicle.git
cd PyChronicle
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install the project:

```bash
pip install -e .
```

---

# ▶️ Execution Workflow

## Step 1 — Verify Installation

```bash
pychronicle --help
```

Displays the available command-line interface commands.

---

## Step 2 — Check Installed Version

```bash
pychronicle --version
```

Displays the installed PyChronicle version.

---

## Step 3 — Prepare the Python Program

Create or modify a Python file (for example `test_script.py`) that you want to analyze.

Example:

```python
def calculate_total(price, quantity):
    total = price * quantity
    return total

name = "Laptop"
price = 500
quantity = 2

total = calculate_total(price, quantity)

discount = 50
final_price = total - discount

for i in range(3):
    final_price += 10

status = "Expensive"

if final_price < 1000:
    status = "Affordable"

print(name)
print(final_price)
print(status)
```

---

## Step 4 — Trace Program Execution

```bash
pychronicle trace test_script.py
```

This command automatically:

- Clears any previous execution history
- Executes the target Python program
- Records runtime execution events
- Captures local variable changes
- Stores execution history inside SQLite

---

## Step 5 — Launch the Interactive Terminal UI

```bash
pychronicle ui
```

The Terminal UI allows you to:

- Browse the execution timeline
- Inspect reconstructed local variables
- View watched variables
- Navigate execution events
- View source code
- Highlight the currently executing line

---

## Step 6 — Performance Benchmark (Optional)

```bash
python benchmark.py
```

Measures:

- Tracing performance
- Replay performance
- Database size
- Storage efficiency
- Delta compression effectiveness

---

## Step 7 — Stress Testing (Optional)

```bash
python stress_test.py
```

Validates the tracer and storage system under larger execution workloads.

---

# 🗄️ Storage

PyChronicle stores execution history inside a SQLite database.

Each execution event records information such as:

- Timestamp
- Executed line number
- Source file name
- Function name
- Runtime event
- Delta-compressed local variable state

Instead of storing the complete runtime state after every executed line, PyChronicle stores **only the variables that changed** between execution steps.

When the user navigates through the execution timeline, the complete program state is reconstructed dynamically by replaying the recorded variable deltas.

This approach significantly reduces storage usage while maintaining accurate historical replay.

SQLite optimizations implemented include:

- WAL (Write-Ahead Logging)
- Database indexing
- Transaction batching
- Delta-state reconstruction cache

---

# 🧪 Testing

PyChronicle includes multiple ways to validate the correctness and performance of the project.

## Automated Tests

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

The automated tests validate the major components of the project, including:

- Command Line Interface
- Database operations
- Runtime tracing
- Timeline reconstruction
- Watch Variables engine

---

## Performance Benchmark

Run:

```bash
python benchmark.py
```

The benchmark measures:

- Runtime tracing speed
- Execution replay performance
- Database size
- Storage efficiency
- Delta compression effectiveness
- Timeline reconstruction performance

---

## Stress Testing

Run:

```bash
python stress_test.py
```

The stress test executes larger workloads to verify:

- Runtime tracing
- Database stability
- Replay correctness
- Storage performance
- Reconstruction accuracy

---

# 🛠️ Technologies Used

- Python 3
- AST (`ast`)
- Runtime Tracing (`sys.settrace`)
- SQLite3
- Textual
- Typer
- unittest
- JSON
- Git
- GitHub

---

# 📈 Development Progress

## ✅ Week 1

- AST Parsing
- Variable Assignment Detection
- SQLite Storage Layer
- Command Line Parser

---

## ✅ Week 2

- Runtime Tracing using `sys.settrace`
- Execution History Recording
- SQLite Logging
- Terminal User Interface
- Timeline Visualization
- Source Code Viewer
- Benchmark Utility
- Stress Testing

---

## ✅ Week 3

- Delta State Compression
- Dynamic State Reconstruction
- Timeline Replay Optimization
- SQLite WAL Optimization
- Database Indexing
- Transaction-based Storage
- Performance Improvements

---

## 🚧 Week 4 (In Progress)

Completed:

- CLI Packaging
- Watch Variables Engine
- Watch Variables Integration
- Professional Package Structure
- Automated Unit Tests

Currently Working On:

- Final Stability Verification
- End-to-End Testing
- Documentation Refinement
- Final Project Review

---

# 🎯 Current Status

## Project Status

- ✅ Week 1 Completed
- ✅ Week 2 Completed
- ⏳ Mid Review (Awaiting Evaluation)
- ✅ Week 3 Completed
- 🚧 Week 4 In Progress

---

## Current Focus

The current focus is completing the remaining Week 4 activities:

- Final stability verification
- End-to-end testing
- Documentation refinement
- Final project polishing

Once these activities are completed, PyChronicle will be ready for the internship's final review and project submission.

---

# 📚 Project Learning Outcomes

Through this project, the following concepts have been explored and implemented:

- Python Abstract Syntax Tree (AST)
- Python Runtime Tracing (`sys.settrace`)
- SQLite Database Design
- Delta-State Compression
- Dynamic State Reconstruction
- Terminal UI Development using Textual
- Python CLI Packaging using Typer
- Automated Software Testing
- Performance Benchmarking
- Stress Testing
- Software Project Organization

---

# 🚀 Future Improvements

Some enhancements that can be explored beyond the internship include:

- Search and filtering within execution history
- Exporting execution sessions
- Breakpoint support
- Multiple trace session management
- Enhanced timeline visualization
- Advanced debugging analytics

---

# 👨‍💻 Author

**Prasheel Varma Datla**

GitHub:

https://github.com/PrasheelVarma

---

# 📄 License

This project is being developed for educational purposes as part of the **Infotact Advanced Python Development Internship**.
