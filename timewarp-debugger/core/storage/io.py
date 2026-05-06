import json
import os

def save_recording(filepath, events):
    if filepath.endswith('.db'):
        from core.storage.db import StorageEngine
        db = StorageEngine(filepath)
        db.save_events(events)
    else:
        with open(filepath, "w") as f:
            json.dump(events, f, indent=2)

def load_recording(filepath):
    if not os.path.exists(filepath):
        print(f"Error: Could not find recording at '{filepath}'. Please check the path and try again.")
        return []
        
    if filepath.endswith('.db'):
        from core.storage.db import StorageEngine
        db = StorageEngine(filepath)
        return db.get_all_events()
    else:
        with open(filepath, "r") as f:
            return json.load(f)
