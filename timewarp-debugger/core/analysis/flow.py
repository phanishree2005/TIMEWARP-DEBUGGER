from core.storage.io import load_recording

def analyze_data_flow(filepath, target_var):
    events = load_recording(filepath)
    print(f"--- Data Flow Analysis for '{target_var}' ---")
    
    last_value = None
    found = False
    
    for e in events:
        if "locals" in e and target_var in e["locals"]:
            current_value = e["locals"][target_var]
            if current_value != last_value:
                print(f"[{e['function']}:{e['line']}] {target_var} mutated -> {current_value}")
                last_value = current_value
                found = True
                
    if not found:
        print(f"Variable '{target_var}' was never observed in the trace.")
