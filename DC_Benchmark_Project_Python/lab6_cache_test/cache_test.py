import time

try:
    import numpy as np
except ImportError:
    np = None

def memory_benchmark(arr_size, stride, app=None):
    if np is None:
        return "numpy not installed. Run `pip install numpy`!"
    arr = np.zeros(arr_size, dtype=np.int32)
    N = len(arr)
    accesses = N // stride
    start = time.time()
    for i in range(0, N, stride):
        arr[i] += 1
        if app and i % max(stride * 10000, 1) == 0:
            app.progress['value'] = min(100, int(100 * i / N))
    elapsed = time.time() - start
    return elapsed, accesses

def run_benchmark(app=None):
    arr_size = 8 * 1024 * 1024  # 8M ints ~32MB
    output = []
    for stride in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
        elapsed, accesses = memory_benchmark(arr_size, stride, app)
        output.append(f"Stride: {stride}, Time: {elapsed:.6f}s, Accesses: {accesses}")
    if app:
        app.progress['value'] = 100
    return "\n".join(output)

def main(app=None):
    return run_benchmark(app)
