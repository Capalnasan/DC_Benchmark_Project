import time
import random

def fixed_point_mult(a, b, frac_bits=16):
    return (a * b) >> frac_bits

def run_benchmark(app=None):
    NUM_ITER = 10_000_000
    frac_bits = 16
    a_vals = [random.randint(0, 1<<16) for _ in range(NUM_ITER)]
    b_vals = [random.randint(0, 1<<16) for _ in range(NUM_ITER)]
    start = time.time()
    for a, b in zip(a_vals, b_vals):
        c = fixed_point_mult(a, b, frac_bits)
    elapsed = time.time() - start
    if app:
        app.progress['value'] = 100
    return f"Fixed-point multiply {NUM_ITER} times in {elapsed:.3f}s"

def main(app=None):
    return run_benchmark(app)
