import cmd
import json
from core.storage.io import load_recording

class TimeWarpREPL(cmd.Cmd):
    intro = '\n=== TimeWarp Interactive Debugger ===\nType help or ? to list commands.\n'
    prompt = '(timewarp) '

    def __init__(self, events):
        super().__init__()
        self.events = events
        self.current_step = 0
        self.max_step = len(events) - 1

    def _print_state(self):
        if self.current_step < 0 or self.current_step > self.max_step:
            print("Out of bounds.")
            return
        e = self.events[self.current_step]
        print(f"\n[Step {self.current_step}/{self.max_step}] -> {e['function']}:{e['line']} ({e['event']}) [Depth: {e.get('depth', 0)}]")
        if e.get("source"):
            print(f"  Source: {e['source']}")
        
    def do_next(self, arg):
        """Step forward one event in time. (Shortcut: n)"""
        if self.current_step < self.max_step:
            self.current_step += 1
            self._print_state()
        else:
            print("Already at the end of the execution.")

    def do_prev(self, arg):
        """Step backward one event in time (Time Travel). (Shortcut: p)"""
        if self.current_step > 0:
            self.current_step -= 1
            self._print_state()
        else:
            print("Already at the beginning of the execution.")

    def do_vars(self, arg):
        """Print local variables at the current step. (Shortcut: v)"""
        e = self.events[self.current_step]
        locals_dict = e.get("locals", {})
        if not locals_dict:
            print("No local variables.")
        else:
            print(json.dumps(locals_dict, indent=2))

    def do_jump(self, arg):
        """Jump to a specific step. Usage: jump <step_number>"""
        try:
            target = int(arg)
            if 0 <= target <= self.max_step:
                self.current_step = target
                self._print_state()
            else:
                print(f"Step must be between 0 and {self.max_step}")
        except ValueError:
            print("Invalid step number.")

    def do_quit(self, arg):
        """Exit the debugger. (Shortcut: q)"""
        print("Exiting TimeWarp.")
        return True

    # Aliases
    do_n = do_next
    do_p = do_prev
    do_v = do_vars
    do_q = do_quit

def start_repl(filepath):
    try:
        events = load_recording(filepath)
    except Exception as err:
        print(f"Error reading {filepath}: {err}")
        return

    if not events:
        print("No events found in the recording.")
        return
    
    repl = TimeWarpREPL(events)
    repl._print_state()
    repl.cmdloop()
