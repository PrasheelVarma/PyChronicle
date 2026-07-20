# PyChronicle

> A Python runtime execution tracer and variable history analyzer built using `sys.settrace`, SQLite, and Textual.

PyChronicle is a developer tool that records the execution of Python programs, captures runtime state changes, and stores execution history in a SQLite database for later analysis. It is being developed as part of the **Infotact Advanced Python Development Internship**.

---

## 🚀 Project Overview

Traditional Python debuggers execute programs one step at a time but require rerunning the program whenever a bug is missed.

PyChronicle aims to provide a lightweight **time-travel debugging** experience by:

- Parsing Python programs
- Tracing runtime execution
- Recording execution history
- Storing execution states in SQLite
- Visualizing execution through a Terminal UI

This project combines Python metaprogramming techniques such as **AST parsing**, **runtime tracing**, and **terminal-based visualization**.

---

# ✨ Features

## ✅ Week 1

- AST-based Python source parsing
- Variable assignment detection
- Annotated assignment detection
- SQLite storage layer
- Command-line parsing support

## ✅ Week 2

- Runtime execution tracing using `sys.settrace`
- Capture execution history
- Record local variable states
- Store execution events in SQLite
- Terminal User Interface (Textual)
- Timeline visualization
- Source code viewer
- Execution details panel
- Stress testing utilities
- Performance benchmarking
- Mid-project validation tools

---

# 📂 Project Structure

```text
PyChronicle/
│
├── src/
│   └── pychronicle/
│       ├── __init__.py
│       ├── parser.py
│       ├── tracer.py
│       ├── storage.py
│       ├── tui.py
│       └── __main__.py
│
├── tests/
│   ├── test1.py
│   └── ...
│
├── stress_test.py
├── benchmark.py
│
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/PrasheelVarma/PyChronicle.git
cd PyChronicle
```

Create a virtual environment

```bash
python -m venv .pc_env
```

Activate the environment

### Linux / macOS

```bash
source .pc_env/bin/activate
```

### Windows

```powershell
.pc_env\Scripts\activate
```

Install the project

```bash
pip install -e .
```

---

# ▶️ Usage

## Parse a Python file

```bash
python -m pychronicle.parser tests/test1.py
```

---

## Trace program execution

```bash
python stress_test.py
```

The tracer will:

- Execute the target program
- Capture runtime events
- Record local variable states
- Store execution history in SQLite

---

## Launch the Terminal UI

```bash
python -m pychronicle.tui
```

The TUI allows you to:

- Browse execution history
- Inspect recorded variable states
- Navigate execution events
- View source code alongside execution data

---

## Run the Benchmark

```bash
python benchmark.py
```

The benchmark performs:

- Database reset
- Runtime tracing
- Trace validation
- Storage audit
- Performance measurement

Example output:

```text
PYCHRONICLE PERFORMANCE BENCHMARK REPORT

Execution Time          : 0.08 seconds
Execution States Logged : 1850
Logging Rate            : 23000 states/sec
Database Size           : 85 KB

TRACE VALIDATION
✔ Execution states captured
✔ Variable states recorded
✔ Execution history verified

STORAGE AUDIT
✔ SQLite storage verified
✔ Minimal tracing overhead

SYSTEM BENCHMARK STATUS : SUCCESS
```

---

# 🗄️ Storage

PyChronicle stores execution history in SQLite.

Each execution event contains information such as:

- Timestamp
- Executed line number
- File name
- Local execution state
- Runtime metadata

This enables replaying and inspecting historical execution.

---

# 🧪 Testing

Example test programs are available inside the `tests/` directory.

Additional stress testing is provided by:

```text
stress_test.py
```

which generates a large number of execution events for validating the tracer and measuring performance.

---

# 🛠️ Technologies Used

- Python 3
- AST (`ast`)
- Runtime Tracing (`sys.settrace`)
- SQLite3
- Textual
- JSON
- Git
- GitHub

---

# 📈 Development Progress

## ✅ Week 1

- AST Parsing
- Variable Assignment Detection
- SQLite Storage
- Command-Line Parser

## ✅ Week 2

- Runtime Tracer
- Execution History Recording
- SQLite Logging
- Terminal UI
- Timeline Viewer
- Benchmarking
- Stress Testing
- Mid-Project Validation

## ⏳ Week 3

- Delta-state compression
- Optimized storage
- Timeline improvements
- Faster execution replay

## ⏳ Week 4

- CLI packaging
- Watch Variables
- Performance optimization
- Documentation refinement
- Final polishing

---

# 🎯 Current Status

**Project Milestone**

✅ Week 1 Completed

✅ Week 2 Completed

✅ Mid-Project Review Completed

🚧 Currently progressing toward Week 3.

---

# 👨‍💻 Author

**Prasheel Varma Datla**

GitHub:
https://github.com/PrasheelVarma

---

# 📄 License

This project is developed for educational and learning purposes as part of the **Infotact Advanced Python Development Internship**.
