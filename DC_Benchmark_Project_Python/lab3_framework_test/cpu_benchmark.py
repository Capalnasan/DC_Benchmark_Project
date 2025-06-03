import time

def cpu_heavy(n):
    x = 0
    for i in range(n):
        x += (i * i) % 7
    return x

def run_benchmark(app=None):
    start = time.time()
    N = 50_000_000
    result = cpu_heavy(N)
    elapsed = time.time() - start
    if app:
        app.progress['value'] = 100
    return f"CPU test: {N} iterations in {elapsed:.3f}s"

def main(app=None):
    return run_benchmark(app)
