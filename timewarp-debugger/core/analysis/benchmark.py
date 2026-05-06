import time
from core.recorder.tracer import start_tracing, stop_tracing

def compute_heavy():
    x = 0
    for i in range(50000):
        x += i
    return x

def run_benchmark():
    print("Running base benchmark without tracing...")
    start = time.time()
    compute_heavy()
    base_time = time.time() - start
    
    print("Running benchmark WITH TimeWarp tracing...")
    start_tracing()
    start = time.time()
    compute_heavy()
    traced_time = time.time() - start
    stop_tracing()
    
    print("\n--- Benchmark Results ---")
    print(f"Base Execution:   {base_time:.5f}s")
    print(f"Traced Execution: {traced_time:.5f}s")
    
    if base_time > 0:
        overhead = traced_time / base_time
        print(f"Overhead Ratio:   {overhead:.2f}x slower")
    else:
        print("Base time was too fast to measure overhead reliably.")
        
if __name__ == '__main__':
    run_benchmark()
