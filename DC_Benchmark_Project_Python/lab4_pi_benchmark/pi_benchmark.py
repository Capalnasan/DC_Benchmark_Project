import time

def compute_pi(n_digits):
    pi = 0
    for k in range(n_digits):
        pi += (1/(16**k))*(
            4/(8*k+1) -
            2/(8*k+4) -
            1/(8*k+5) -
            1/(8*k+6)
        )
    return pi

def run_benchmark(app=None):
    n = 500_000  # Number of terms
    start = time.time()
    pi_val = compute_pi(n)
    elapsed = time.time() - start
    if app:
        app.progress['value'] = 100
    return f"Calculated pi with {n} terms in {elapsed:.3f}s\nApprox value: {pi_val}"

def main(app=None):
    return run_benchmark(app)
