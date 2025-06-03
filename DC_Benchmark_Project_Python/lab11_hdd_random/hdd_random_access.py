import os
import random
import time
import tempfile

def run_benchmark(app=None):
    TEMP_FOLDER = os.path.join(tempfile.gettempdir(), "bench")
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    FILENAME = os.path.join(TEMP_FOLDER, "random_access.dat")
    FILE_SIZE = 64 * 1024 * 1024  # 64MB
    BLOCK_SIZE = 4096  # 4KB
    NUM_ACCESSES = 5000

    # Create file if it doesn't exist
    if not os.path.exists(FILENAME):
        with open(FILENAME, "wb") as f:
            f.write(os.urandom(FILE_SIZE))

    with open(FILENAME, "rb") as f:
        start = time.time()
        for i in range(NUM_ACCESSES):
            pos = random.randint(0, FILE_SIZE - BLOCK_SIZE)
            f.seek(pos)
            data = f.read(BLOCK_SIZE)
            if app and NUM_ACCESSES > 0:
                app.progress['value'] = int(100 * (i+1) / NUM_ACCESSES)
        elapsed = time.time() - start
    return f"Random read: {NUM_ACCESSES} accesses in {elapsed:.2f}s ({NUM_ACCESSES/elapsed:.1f} IOPS)"

def main(app=None):
    return run_benchmark(app)
