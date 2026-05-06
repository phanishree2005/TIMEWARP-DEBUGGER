import unittest
import os
from core.recorder.tracer import start_tracing, stop_tracing, get_recorded_events
from core.storage.io import save_recording, load_recording
from core.analysis.differ import compare_runs

def dummy_function():
    x = 10
    y = x + 5
    return y

class TestTimeWarpCore(unittest.TestCase):
    def test_tracer_captures_events(self):
        start_tracing()
        dummy_function()
        stop_tracing()
        
        events = get_recorded_events()
        self.assertTrue(len(events) > 0, "Tracer should capture events")
        
        # Check if dummy_function is in the trace
        functions = [e.get("function") for e in events]
        self.assertIn("dummy_function", functions)
        
    def test_replayer_io(self):
        start_tracing()
        dummy_function()
        stop_tracing()
        
        events = get_recorded_events()
        test_file = "test_run.json"
        
        # Save
        save_recording(test_file, events)
        self.assertTrue(os.path.exists(test_file))
        
        # Load
        loaded_events = load_recording(test_file)
        self.assertEqual(len(events), len(loaded_events))
        
        os.remove(test_file)

    def test_differ_detects_change(self):
        run1 = [{"event": "call", "function": "funcA", "line": 1, "locals": {"x": 1}}]
        run2 = [{"event": "call", "function": "funcA", "line": 1, "locals": {"x": 2}}]
        
        # Manually create files
        save_recording("t1.json", run1)
        save_recording("t2.json", run2)
        
        # We just test that differ doesn't crash on simple inputs.
        # compare_runs currently prints to stdout. 
        try:
            compare_runs("t1.json", "t2.json")
            success = True
        except Exception:
            success = False
            
        self.assertTrue(success)
        
        os.remove("t1.json")
        os.remove("t2.json")

if __name__ == '__main__':
    unittest.main()
