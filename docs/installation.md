# Installation Guide

## Overview

This document explains how to install and configure the PyChronicle development environment.

The installation process includes:

- Cloning the repository
- Creating a Python virtual environment
- Installing project dependencies
- Installing PyChronicle as a local package
- Verifying the installation

Following these steps ensures that PyChronicle is correctly configured for development and testing.

---

# System Requirements

Before installing PyChronicle, ensure that the following software is available.

## Operating System

PyChronicle can be developed and executed on:

- Linux
- Windows
- macOS

---

## Python

Python 3.10 or later is recommended.

Verify the installed version:

```bash
python --version
```

---

## Git

Git is required to clone the project repository.

Verify Git installation:

```bash
git --version
```

---

# Clone the Repository

Clone the project from GitHub.

```bash
git clone https://github.com/PrasheelVarma/PyChronicle.git
```

Move into the project directory.

```bash
cd PyChronicle
```

---

# Create a Virtual Environment

Creating a virtual environment keeps project dependencies isolated from the system Python installation.

Create the environment:

```bash
python -m venv venv
```

---

# Activate the Virtual Environment

## Linux / macOS

```bash
source venv/bin/activate
```

---

## Windows

```powershell
venv\Scripts\activate
```

Once activated, the terminal prompt should display the virtual environment name.

Example:

```text
(venv)
```

---

# Install Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

This installs all libraries required by PyChronicle.

Typical dependencies include:

- Textual
- Typer

---

# Install the Project

Install PyChronicle in editable mode.

```bash
pip install -e .
```

Editable installation allows changes made to the source code to be reflected immediately without reinstalling the package.

---

# Verify Installation

Verify that the package has been installed successfully.

Display the available commands:

```bash
python -m pychronicle --help
```

or

```bash
pychronicle --help
```

A successful installation displays the available command-line interface.

---

# Running the Parser

Parse a Python source file.

```bash
python -m pychronicle parser tests/test1.py
```

This performs static analysis using Python's Abstract Syntax Tree (AST).

---

# Runtime Tracing

Execute runtime tracing on a Python program.

```bash
python -m pychronicle trace test_script.py
```

The tracer records runtime execution history and stores it inside the SQLite database.

---

# Launch the Terminal User Interface

Once execution history has been recorded, start the interactive Terminal User Interface.

```bash
python -m pychronicle ui
```

The interface allows developers to:

- Navigate execution history
- Inspect variables
- Replay execution
- Monitor Watch Variables

---

# Running Automated Tests

Execute the complete automated unit test suite.

```bash
python -m unittest discover -s tests -p "test*.py" -v
```

All tests should complete successfully.

---

# Running the Stress Test

Execute the stress testing program.

```bash
python stress_test.py
```

This generates a large execution history for validating runtime tracing and replay performance.

---

# Running the Benchmark

Measure the performance of PyChronicle.

```bash
python benchmark.py
```

The benchmark reports:

- Runtime tracing speed
- Replay performance
- Database size
- Delta compression efficiency

---

# Project Setup Checklist

Before beginning development, verify that the following steps have been completed.

- Repository cloned
- Virtual environment created
- Virtual environment activated
- Dependencies installed
- Project installed in editable mode
- Parser verified
- Runtime tracing verified
- Terminal UI verified
- Automated tests executed
- Benchmark executed

---

# Troubleshooting

## Command Not Found

If the `pychronicle` command is unavailable, ensure that:

- The virtual environment is activated.
- The project has been installed using:

```bash
pip install -e .
```

---

## Missing Dependencies

If import errors occur, reinstall the required packages.

```bash
pip install -r requirements.txt
```

---

## Module Import Errors

Verify that commands are executed from the project root directory.

Example:

```text
PyChronicle/
```

Running commands from another directory may prevent Python from locating the package.

---

# Summary

PyChronicle can be installed using standard Python development tools.

The recommended workflow consists of cloning the repository, creating a virtual environment, installing dependencies, installing the project in editable mode, and verifying the installation using the parser, runtime tracer, Terminal User Interface, automated tests, stress test, and benchmark.

Following this process ensures that the development environment is correctly configured and ready for further development or experimentation.
