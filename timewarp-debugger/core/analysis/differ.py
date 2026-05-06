import json
from core.storage.io import load_recording

def compare_runs(run1_path, run2_path):
    run1 = load_recording(run1_path)
    run2 = load_recording(run2_path)
        
    max_len = max(len(run1), len(run2))
    
    for i in range(max_len):
        if i >= len(run1):
            print(f"Difference at step {i}")
            print(f"Run1: <missing event>")
            print(f"Run2: {json.dumps(run2[i])}")
            return
        if i >= len(run2):
            print(f"Difference at step {i}")
            print(f"Run1: {json.dumps(run1[i])}")
            print(f"Run2: <missing event>")
            return
            
        e1 = run1[i]
        e2 = run2[i]
        
        # We ignore time differences and only compare function, line, and locals
        if e1['function'] != e2['function'] or e1['line'] != e2['line'] or e1['locals'] != e2['locals']:
            print(f"Difference at step {i}")
            # Format output to match expected Output
            print(f"Run1: {json.dumps(e1)}")
            print(f"Run2: {json.dumps(e2)}")
            return
            
    print("Runs are identical.")
