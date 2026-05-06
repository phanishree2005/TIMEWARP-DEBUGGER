import sys
import time
import os
import re
import threading
import linecache

WORKSPACE_DIR = os.getcwd()
recorded_events = []
start_time = 0

def deep_serialize(obj, depth=0, max_depth=2, visited=None):
    if visited is None:
        visited = set()
        
    obj_id = id(obj)
    if obj_id in visited:
        return "<circular_reference>"
        
    if depth > max_depth:
        return "<max_depth_reached>"
        
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
        
    visited.add(obj_id)
    
    try:
        if isinstance(obj, dict):
            return {str(k): deep_serialize(v, depth+1, max_depth, visited) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple, set)):
            return [deep_serialize(v, depth+1, max_depth, visited) for v in obj]
        else:
            val_str = str(obj)
            val_str = re.sub(r' at 0x[0-9a-fA-F]+', '', val_str)
            return val_str
    except Exception:
        return "<unserializable>"
    finally:
        visited.remove(obj_id)

def safe_serialize(locals_dict):
    serialized = {}
    for k, v in locals_dict.items():
        if k in ['__builtins__', '__doc__', '__loader__', '__spec__', '__name__', '__package__', '__file__', '__cached__']:
            continue
        serialized[k] = deep_serialize(v)
    return serialized

def trace_calls(frame, event, arg):
    if event in ("call", "line", "return"):
        func_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        
        abs_filename = os.path.abspath(filename)
        if not abs_filename.startswith(WORKSPACE_DIR):
            return trace_calls
            
        ignore_keywords = ["<", "tracer.py", "main.py", "differ.py", "replayer.py", "repl.py", "db.py", "io.py", "api.py", "benchmark.py"]
        if any(kw in filename for kw in ignore_keywords):
            return trace_calls
            
        line_no = frame.f_lineno
        source_line = linecache.getline(filename, line_no).strip()
        thread_id = threading.get_ident()
        
        # Calculate stack depth
        stack_depth = 0
        f = frame
        while f:
            stack_depth += 1
            f = f.f_back
            
        event_data = {
            "time": round(time.time() - start_time, 4),
            "thread_id": thread_id,
            "event": event,
            "function": func_name,
            "line": line_no,
            "source": source_line,
            "depth": stack_depth,
            "locals": safe_serialize(frame.f_locals)
        }
        recorded_events.append(event_data)
    return trace_calls

def start_tracing():
    global recorded_events, start_time
    recorded_events = []
    start_time = time.time()
    sys.settrace(trace_calls)
    threading.settrace(trace_calls)

def stop_tracing():
    sys.settrace(None)
    threading.settrace(None)

def get_recorded_events():
    return recorded_events
