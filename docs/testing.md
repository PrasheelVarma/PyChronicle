# Testing

## Overview

Testing is an essential part of the PyChronicle project. It ensures that the runtime tracing engine, database layer, execution replay, command-line interface, and Terminal User Interface operate correctly under different scenarios.

The project combines automated unit testing, stress testing, performance benchmarking, and manual verification to validate both correctness and reliability.

---

# Testing Objectives

The testing process aims to verify that:

- Runtime tracing records execution correctly.
- Variable state changes are captured accurately.
- SQLite storage functions reliably.
- Delta-state reconstruction reproduces historical program states.
- Watch Variables behave as expected.
- The command-line interface accepts valid commands.
- Invalid inputs are handled safely.
- The Terminal User Interface displays execution history correctly.

---

# Testing Strategy

PyChronicle uses multiple testing approaches.

```text
                Testing Strategy

                     │
     ┌───────────────┼────────────────┐
     │               │                │
     ▼               ▼                ▼
 Unit Tests     Stress Testing   Manual Testing
     │               │                │
     └───────────────┼────────────────┘
                     ▼
             Performance Benchmark
```

Each testing method focuses on a different aspect of the project.

---

# Automated Unit Tests

The project includes automated unit tests for the core modules.

These tests verify that individual components behave correctly under normal and edge-case conditions.

The automated test suite covers:

- Command-line interface
- Database operations
- Runtime tracing
- Timeline reconstruction
- Watch Variables

Run all tests using:

```bash
python -m unittest discover -s tests -p "test*.py" -v
```

---

# Test Modules

The `tests/` directory contains dedicated test files for different components.

## test_cli.py

Validates the command-line interface.

Tests include:

- Help command
- Version command
- Invalid commands
- Missing files
- Invalid Python files
- UI command
- Trace command

---

## test_database.py

Validates the SQLite storage layer.

Tests include:

- Database creation
- Execution state insertion
- Database reset
- Empty database handling
- Execution state storage

---

## test_tracing.py

Tests the runtime tracing engine.

Scenarios include:

- Variable assignments
- Variable updates
- Variable deletion
- Loops
- Functions
- Nested functions
- Recursion
- Exception handling
- Classes and objects
- Complex Python data types

---

## test_timeline.py

Verifies execution state reconstruction.

Tests ensure that:

- Delta-compressed execution history can be reconstructed accurately.
- Historical variable states are reproduced correctly.
- Timeline replay behaves consistently.

---

## test_watch.py

Validates the Watch Variables engine.

Tests include:

- Watch list management
- Adding watched variables
- Removing watched variables
- Duplicate suppression
- Variable history
- Variable deletion
- Variable recreation
- Timeline loading

---

# Stress Testing

The project includes a dedicated stress testing program.

Run:

```bash
python stress_test.py
```

The stress test generates a large number of runtime events to simulate real-world execution.

Its purpose is to evaluate:

- Runtime tracing stability
- Database growth
- Delta compression
- Timeline reconstruction
- Replay performance

Stress testing helps identify issues that may not appear in small test programs.

---

# Performance Benchmark

Performance is evaluated separately using the benchmarking utility.

Run:

```bash
python benchmark.py
```

The benchmark measures:

- Runtime tracing speed
- Replay speed
- Database size
- Storage efficiency
- Delta compression effectiveness

Unlike unit tests, benchmarking focuses on performance rather than correctness.

---

# Manual Testing

Certain project features require manual verification.

These include:

- Terminal User Interface layout
- Timeline navigation
- Source code viewer
- Watch Variables panel
- Execution snapshot display
- Keyboard navigation
- Theme appearance

Manual testing ensures that the user experience matches the expected behavior.

---

# Example Manual Testing Workflow

A typical verification process is:

```text
Write Sample Python Program
            │
            ▼
Trace Program Execution
            │
            ▼
Launch Terminal UI
            │
            ▼
Navigate Timeline
            │
            ▼
Inspect Variable Changes
            │
            ▼
Verify Watch Variables
            │
            ▼
Validate Execution History
```

This workflow confirms that all major project components work together correctly.

---

# Edge Cases Tested

Several edge cases were considered during testing.

Examples include:

- Empty execution history
- Missing Python files
- Invalid file extensions
- Variable deletion
- Recursive functions
- Nested function calls
- Exception handling
- Large execution timelines
- Complex runtime objects
- Watch variable recreation

Testing these cases improves the robustness of the project.

---

# Expected Results

A successful test run should confirm that:

- All automated tests pass.
- Runtime tracing completes successfully.
- Execution history is stored correctly.
- Timeline reconstruction is accurate.
- Watch Variables behave consistently.
- Benchmark completes successfully.
- Stress test executes without errors.
- The Terminal User Interface remains responsive.

---

# Benefits of Testing

Testing provides several important benefits:

- Detects regressions during development.
- Verifies runtime correctness.
- Improves project reliability.
- Validates database consistency.
- Confirms replay accuracy.
- Ensures stable command-line behavior.
- Supports future maintenance and enhancements.

---

# Summary

PyChronicle combines automated unit testing, stress testing, benchmarking, and manual verification to validate both correctness and performance.

This multi-layered testing strategy helps ensure that runtime tracing, execution storage, timeline reconstruction, and the Terminal User Interface operate reliably across a variety of execution scenarios, resulting in a stable and maintainable debugging tool.
