# Parser Module

## Overview

The Parser module is responsible for performing static analysis of Python source code before runtime execution.

It uses Python's built-in **Abstract Syntax Tree (AST)** module to parse Python files and identify variable assignment statements without executing the program.

This module serves as the first stage of the PyChronicle workflow by analyzing the structure of Python source code.

---

# Purpose

The parser provides a lightweight method for inspecting Python programs before runtime tracing begins.

Its primary objectives are to:

- Parse Python source files.
- Detect variable assignment statements.
- Detect annotated assignments.
- Validate Python syntax.
- Demonstrate static code analysis using Python's AST module.

Unlike the runtime tracer, the parser does not execute the target program.

---

# What is an AST?

AST stands for **Abstract Syntax Tree**.

When Python reads a source file, it first converts the code into a tree-like structure that represents the program's syntax.

Instead of reading raw text, the parser works with this structured representation.

Example:

Python code:

```python
x = 10
y = x + 5
```

Simplified AST representation:

```text
Module
│
├── Assign
│     ├── Target: x
│     └── Value: 10
│
└── Assign
      ├── Target: y
      └── Value: x + 5
```

This allows PyChronicle to inspect the program without running it.

---

# Parser Workflow

The parser follows the workflow shown below.

```text
Python Source File
        │
        ▼
Read File
        │
        ▼
Parse using ast.parse()
        │
        ▼
Generate AST
        │
        ▼
Visit AST Nodes
        │
        ▼
Detect Assignments
        │
        ▼
Display Results
```

---

# Assignment Detection

The parser currently detects common assignment statements.

Example:

```python
x = 10
name = "PyChronicle"
total = price * quantity
```

Each assignment node is identified while traversing the Abstract Syntax Tree.

---

# Annotated Assignments

The parser also detects annotated assignments introduced in modern versions of Python.

Example:

```python
age: int = 20
```

These statements are represented by `AnnAssign` nodes inside the AST and are processed separately.

---

# Syntax Validation

Before generating the Abstract Syntax Tree, Python verifies that the source code follows valid syntax rules.

If invalid syntax is encountered, parsing stops and an appropriate error is reported.

This prevents invalid programs from entering later stages of the workflow.

---

# Why AST Instead of Reading Text?

Reading source code as plain text cannot reliably determine program structure.

Using the Abstract Syntax Tree provides several advantages:

- Ignores formatting differences.
- Understands Python syntax.
- Detects language constructs accurately.
- Supports structured program analysis.
- Avoids manual string parsing.

This makes the parser significantly more reliable.

---

# Role in the Project

The Parser module demonstrates static program analysis.

Within the complete PyChronicle architecture, it represents the first stage of the development pipeline.

```text
Python Program
      │
      ▼
Parser (AST)
      │
      ▼
Runtime Tracer
      │
      ▼
SQLite Storage
      │
      ▼
Timeline Reconstruction
      │
      ▼
Terminal User Interface
```

Although the runtime tracer performs the primary execution analysis, the parser provides the foundation for understanding Python source code structure.

---

# Current Capabilities

The parser currently supports:

- Python source parsing
- AST generation
- Assignment detection
- Annotated assignment detection
- Syntax validation

These capabilities demonstrate the use of Python's built-in parsing infrastructure for static analysis.

---

# Limitations

The current parser is intentionally lightweight.

It does not attempt to:

- Execute Python programs.
- Evaluate expressions.
- Perform control flow analysis.
- Build symbol tables.
- Infer variable types.
- Perform code optimization.

These responsibilities belong to later stages of the project or are outside the scope of PyChronicle.

---

# Summary

The Parser module provides the static analysis component of PyChronicle.

By using Python's Abstract Syntax Tree (AST), it can inspect Python source files, detect assignment statements, and validate syntax without executing the program.

This module introduces the project's use of compiler-inspired techniques and serves as the foundation for understanding Python program structure before runtime tracing begins.
