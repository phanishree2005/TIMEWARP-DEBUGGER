# TimeWarp Debugger

**🚀 Live Demo:** [https://timewarp-debugger-h4x7.vercel.app/](https://timewarp-debugger-h4x7.vercel.app/)  
**⚙️ Backend API:** [https://timewarp-debugger.onrender.com](https://timewarp-debugger.onrender.com)

**TimeWarp** is a professional-grade time-travel debugger for Python. It traces execution step-by-step, captures exact memory snapshots, and lets you rewind code execution to find exactly where state mutations or bugs occurred.

---

### ✨ Key Features
- **Deterministic Recording:** Save the exact step-by-step trace of your Python program to an SQLite database.
- **Time-Travel REPL:** Step backward (`prev`) or forward (`next`) through execution in the terminal.
- **Memory Snapshots:** View local variables, stack depth, and source code context at every single execution step.
- **Diff Analysis Engine:** Automatically compare two execution runs to find exactly where logic diverged.
- **Live React Dashboard:** A premium dark-mode Web UI with a Live Editor and visual timeline.

---

### 🚀 Quick Start

1. **Record a script:**
   ```bash
   .\timewarp.bat record examples\bug_case.py -o bug_run.db
   ```
2. **Replay in the Interactive REPL:**
   ```bash
   .\timewarp.bat debug bug_run.db
   # Type 'next', 'prev', or 'vars' in the console!
   ```
3. **Analyze Data Flow:**
   ```bash
   .\timewarp.bat flow bug_run.db final_price
   ```
4. **Launch the Web Dashboard:**
   ```bash
   .\timewarp.bat api bug_run.db -p 8000
   cd ui && npm run dev
   ```

---

### 🏗️ Architecture

```text
[Python Script] -> (sys.settrace) -> [Recorder] -> [SQLite DB]
                                                          |
                                      +-------------------+-------------------+
                                      v                   v                   v
                               [CLI Replayer]      [Diff Engine]      [REST API] -> [React Dashboard]
```

---

### 📊 Performance Note
Line-level tracing in Python carries inherent overhead because the VM pauses to capture state on every operation. 
* **Benchmark:** Our standard heavy loop takes `~0.001s` natively, and `~0.320s` when traced.
* **Usage:** TimeWarp is designed for finding impossible bugs, root-cause analysis, and local debugging. It is **not** meant to run in 24/7 production environments due to the `sys.settrace` overhead.
