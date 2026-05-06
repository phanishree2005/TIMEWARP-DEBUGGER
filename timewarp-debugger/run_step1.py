from core.recorder.tracer import start_tracing, stop_tracing
import examples.target as target

if __name__ == "__main__":
    start_tracing()
    target.main()
    stop_tracing()
