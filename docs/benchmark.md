# Benchmark

## Overview

PyChronicle includes a benchmarking utility to evaluate the performance of the runtime tracing engine and the efficiency of the storage layer.

The benchmark measures how efficiently execution history is recorded, how much storage is consumed, and how quickly historical execution states can be reconstructed.

Unlike unit tests, the benchmark focuses on performance characteristics rather than functional correctness.

---

# Purpose

The benchmark is designed to answer questions such as:

- How long does tracing take?
- How many execution events are recorded?
- How much storage is required?
- How effective is delta-state compression?
- How quickly can execution history be replayed?

These measurements help evaluate the scalability and efficiency of the project.

---

# Benchmark Workflow

The benchmark follows the execution flow shown below.

```text
Reset Database
       │
       ▼
Execute Stress Test
       │
       ▼
Trace Runtime Events
       │
       ▼
Store Execution History
       │
       ▼
Collect Database Statistics
       │
       ▼
Replay Timeline
       │
       ▼
Generate Performance Report
```

---

# Running the Benchmark

Execute the benchmark using:

```bash
python benchmark.py
```

The benchmark automatically performs every required step.

---

# Benchmark Operations

During execution, the benchmark performs the following operations:

## 1. Database Reset

The existing execution database is cleared to ensure that previous execution history does not influence the benchmark results.

This guarantees that every benchmark starts with a clean environment.

---

## 2. Runtime Tracing

The benchmark executes the stress testing program through the PyChronicle tracing engine.

During execution:

- Runtime events are captured.
- Variable changes are detected.
- Delta-compressed execution states are stored.
- SQLite transactions are committed.

---

## 3. Database Analysis

Once tracing has completed, the benchmark collects statistics from the SQLite database.

Typical measurements include:

- Total execution events
- Number of stored timeline entries
- Database size
- Storage efficiency

These values provide insight into the effectiveness of the storage system.

---

## 4. Timeline Replay

The benchmark reconstructs execution history from the stored delta states.

This measures how efficiently historical execution states can be rebuilt for the Terminal User Interface.

---

## 5. Report Generation

Finally, a summary report is displayed containing the collected performance metrics.

Example:

```text
============================================================
        PYCHRONICLE PERFORMANCE BENCHMARK REPORT
============================================================

Execution Write Time
Replay Fetch Time
Execution Deltas Logged
Tracing Throughput
Compressed Database Size

DELTA COMPRESSION AUDIT

Timeline Reconstruction
Variable Delta Recording

SYSTEM BENCHMARK STATUS : SUCCESS
```

The exact values depend on the executed program and system configuration.

---

# Metrics Measured

The benchmark evaluates several important performance metrics.

## Execution Write Time

Measures the time required to record execution history while the traced program is running.

A lower value indicates faster tracing performance.

---

## Replay Fetch Time

Measures the time required to reconstruct execution history from the stored delta states.

Efficient replay is important for smooth navigation inside the Terminal User Interface.

---

## Execution Events

Represents the total number of runtime events captured during tracing.

These events form the execution timeline displayed in the user interface.

---

## Database Size

Measures the amount of storage consumed by the SQLite database after tracing completes.

Because PyChronicle stores only variable changes, the database remains significantly smaller than storing complete execution states.

---

## Delta Compression Efficiency

Evaluates how effectively redundant execution state has been eliminated.

A successful benchmark demonstrates that only modified variables are written to storage.

---

# Relationship with Stress Testing

The benchmark is designed to work together with the stress testing program.

The stress test generates a large number of runtime events, allowing the benchmark to evaluate:

- Storage performance
- Runtime tracing overhead
- Replay speed
- Delta compression effectiveness
- Database growth

This provides a more realistic evaluation than tracing very small programs.

---

# Design Considerations

The benchmarking system is intentionally lightweight.

It uses the same tracing engine and storage layer as the main application, ensuring that benchmark results accurately reflect real-world project behavior.

No separate benchmarking framework is required.

---

# Limitations

Benchmark results depend on several external factors, including:

- Processor speed
- Available memory
- Operating system
- Python version
- Program complexity
- Storage device performance

Therefore, benchmark values should be interpreted as relative performance measurements rather than absolute performance guarantees.

---

# Summary

The benchmarking utility provides a practical method for evaluating the performance of PyChronicle.

By measuring runtime tracing speed, storage efficiency, replay performance, and database growth, the benchmark helps validate that the tracing engine remains efficient while maintaining accurate execution history.

It serves as an important tool for performance analysis throughout the development of the project.
