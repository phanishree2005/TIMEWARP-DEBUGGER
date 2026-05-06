from core.recorder.tracer import start_tracing, stop_tracing, save_recording
import examples.target as target

if __name__ == "__main__":
    start_tracing()
    target.main()
    stop_tracing()
    
    save_recording("recording.json")
    print("Recording saved to recording.json\n")
    
    with open("recording.json", "r") as f:
        print(f.read())
