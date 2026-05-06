from core.storage.io import load_recording

def replay(filepath, step=False, jump=None):
    events = load_recording(filepath)
    if not events:
        print("No events found.")
        return
        
    start_idx = jump if jump is not None else 0
    start_idx = max(0, min(start_idx, len(events) - 1))
    
    for i in range(start_idx, len(events)):
        event = events[i]
        if event.get("event") == "call":
            print(f"\nReplaying: {event['function']}")
            
        print(f"[{i}/{len(events)-1}] [{event['function']}:{event['line']}] {event.get('source', '')} | Locals: {event.get('locals', {})}")
        
        if step and i < len(events) - 1:
            input("Press Enter to continue to next step...")
