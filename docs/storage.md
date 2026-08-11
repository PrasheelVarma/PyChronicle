# Storage Layer

## Overview

PyChronicle uses SQLite as its persistent storage layer for execution history.

The storage layer is responsible for recording execution events, storing variable state changes, and providing the data required to reconstruct program state later.

The design focuses on:

- Persistent execution history
- Efficient writes
- Delta-based storage
- Indexed queries
- Reliable state retrieval
- Reduced storage overhead

---

## Storage Technology

PyChronicle uses:

- **SQLite** — Embedded relational database
- **WAL mode** — Write-Ahead Logging for improved write behavior
- **Transactions** — Atomic database operations
- **Indexes** — Faster timeline and execution queries

No external database server is required.

---

## Database Structure

The execution history is stored in the SQLite database.

The execution records contain information such as:

| Field | Description |
|---|---|
| `id` | Unique execution record identifier |
| `timestamp` | Time associated with the recorded event |
| `line_number` | Source-code line being executed |
| `variable_name` | Variable associated with the state change |
| `serialized_value` | Serialized representation of the value |

Additional execution metadata can be stored depending on the execution event.

---

## Execution History

During tracing, PyChronicle records execution events in chronological order.

A simplified representation is:

```text
Python Program
      │
      ▼
Runtime Tracer
      │
      ▼
State Change
      │
      ▼
Storage Layer
      │
      ▼
SQLite Database
