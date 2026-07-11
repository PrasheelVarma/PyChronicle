# PyChronicle

> A Python-based execution tracing and variable history analysis tool.

PyChronicle is a developer tool that helps visualize how Python programs execute by recording variable assignments and building a history of program execution. The project is being developed as part of the **Infotact Python Development Internship**.

> **Current Progress:** Week 1 Completed 🚧

---

## Project Overview

The goal of PyChronicle is to create a lightweight debugging and execution analysis tool capable of:

- Parsing Python source code using the Abstract Syntax Tree (AST)
- Detecting variable assignments
- Recording variable history into a SQLite database
- Tracing program execution (upcoming)
- Building a timeline of variable state changes (upcoming)

---

## Current Features (Week 1)

- Parse Python source files using Python's `ast` module.
- Detect variable assignments.
- Detect annotated assignments.
- Store assignment metadata in a SQLite database.
- Command-line support for analyzing Python files.
- Basic error handling for invalid input files.

---

## Project Structure

```text
PyChronicle/
│
├── src/
│   └── pychronicle/
│       ├── __init__.py
│       ├── parser.py
│       └── storage.py
│
├── tests/
│   └── test1.py
│
├── pyproject.toml
├── requirements.txt
├── README.md
└── pychronicle_history.db
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
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

## Usage

Analyze a Python source file

```bash
python -m pychronicle.parser tests/test1.py
```

The parser will:

- Parse the source file
- Detect variable assignments
- Store assignment information inside the SQLite database

---

## Database Schema

Current database table:

| Column | Description |
|---------|-------------|
| id | Primary Key |
| timestamp | Time of insertion |
| line_number | Line where assignment occurred |
| variable_name | Name of the assigned variable |
| serialized_value | Placeholder for future runtime value storage |

---

## Technologies Used

- Python 3
- Abstract Syntax Tree (AST)
- SQLite3
- JSON
- Git
- GitHub

---

## Development Roadmap

### ✅ Week 1
- [x] AST Parsing
- [x] Variable Assignment Detection
- [x] SQLite Integration
- [x] Command-line File Analysis

### ⏳ Week 2
- Runtime execution tracing
- Capture variable values
- Execution timeline

### ⏳ Week 3
- Function tracing
- Enhanced execution history
- Timeline improvements

### ⏳ Week 4
- Final integration
- Documentation
- Project refinement

---

## Author

**Prasheel Varma Datla**

GitHub: https://github.com/PrasheelVarma

---

## License

This project is currently developed for educational purposes as part of the Infotact Python Development Internship.
