import argparse
import sys
import runpy
import os

# Adjust path so `core` can be imported when running as script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.recorder.tracer import start_tracing, stop_tracing, get_recorded_events
from core.playback.replayer import replay
from core.analysis.differ import compare_runs
from core.storage.io import save_recording

def main():
    parser = argparse.ArgumentParser(prog="timewarp")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Record
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("file", help="Python file to record")
    record_parser.add_argument("-o", "--output", default="recording.json", help="Output JSON file")
    
    # Replay
    replay_parser = subparsers.add_parser("replay", help="Replay a recorded execution")
    replay_parser.add_argument("file", help="Recording JSON/DB to replay")
    replay_parser.add_argument("--step", action="store_true", help="Pause after each step (interactive)")
    replay_parser.add_argument("--jump", type=int, help="Jump directly to a specific step number")
    
    # Analyze
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("run1", help="First recording JSON")
    analyze_parser.add_argument("run2", help="Second recording JSON")
    
    # Interactive Debug
    debug_parser = subparsers.add_parser("debug")
    debug_parser.add_argument("file", help="Recording JSON/DB to debug interactively")
    
    # API Server
    api_parser = subparsers.add_parser("api")
    api_parser.add_argument("file", help="Recording JSON/DB to serve")
    api_parser.add_argument("-p", "--port", type=int, default=8000, help="Port to run API on")
    
    # Benchmark
    benchmark_parser = subparsers.add_parser("benchmark")
    
    # Data Flow
    flow_parser = subparsers.add_parser("flow")
    flow_parser.add_argument("file", help="Recording JSON/DB")
    flow_parser.add_argument("var", help="Variable name to track")
    
    args = parser.parse_args()
    
    if args.command == "record":
        print(f"Recording execution of {args.file}...")
        
        target_dir = os.path.dirname(os.path.abspath(args.file))
        if target_dir not in sys.path:
            sys.path.insert(0, target_dir)
            
        start_tracing()
        try:
            runpy.run_path(args.file, run_name="__main__")
        except SystemExit:
            pass
        except Exception as e:
            print(f"Execution error: {e}")
        finally:
            stop_tracing()
            events = get_recorded_events()
            save_recording(args.output, events)
            print(f"Saved recording to {args.output}")
            
    elif args.command == "replay":
        print(f"Replaying from {args.file}...")
        replay(args.file, step=args.step, jump=args.jump)
        
    elif args.command == "analyze":
        print(f"Comparing {args.run1} and {args.run2}...")
        compare_runs(args.run1, args.run2)
        
    elif args.command == "debug":
        from core.cli.repl import start_repl
        start_repl(args.file)
        
    elif args.command == "api":
        from core.server.api import start_server
        start_server(args.file, args.port)
        
    elif args.command == "benchmark":
        from core.analysis.benchmark import run_benchmark
        run_benchmark()
        
    elif args.command == "flow":
        from core.analysis.flow import analyze_data_flow
        analyze_data_flow(args.file, args.var)

if __name__ == "__main__":
    main()
