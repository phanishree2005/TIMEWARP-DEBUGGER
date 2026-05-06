# TimeWarp Debugger Architecture

## System Overview
TimeWarp is a multi-layer engineering system designed to trace, record, analyze, and replay Python program executions deterministically.

## Layer 1: The Core Recorder (`core/recorder`)
At the lowest level, TimeWarp uses `sys.settrace` and `threading.settrace` to hook into the Python VM.
- **Features:** Call stack tracking, deep object serialization, line context caching, and thread ID capturing.
- **Design Choice:** Filters are applied eagerly to prevent standard library code and internal debugger code from polluting the execution trace and eating memory.

## Layer 2: The Storage Interface (`core/storage`)
- **JSON Engine:** Standard output for small to medium scripts. Easy to diff and read.
- **SQLite Engine:** Used when the output file is `.db`. Allows scalable, out-of-core storage for executions that generate millions of events. This lays the foundation for analyzing huge enterprise applications without OOM errors.

## Layer 3: Playback & Interactive REPL (`core/playback`, `core/cli`)
- **Time-Travel Debugger:** Extends the standard `cmd` module to provide a REPL interface where developers can step forward, backward, or jump to any specific state in the execution history. 
- **Diff Engine:** `differ.py` performs differential analysis across two executions to quickly spot state mutations and divergence points.

## Layer 4: API & Extensibility (`core/server`)
- **REST API (`api.py`):** Exposes the recorded traces over HTTP (`/api/events`). This is the foundation required to attach a rich frontend (like a React or Vue GUI) or build VSCode plugins.

## Scalability & Performance
The overhead of line-level tracing in Python is inherently high. TimeWarp mitigates this by:
1. Stripping object references into clean structural representations.
2. Routing data to SQLite for big workloads.
3. Filtering irrelevant modules to reduce IO bottlenecking.
*(Run `timewarp benchmark` to observe the overhead costs.)*
