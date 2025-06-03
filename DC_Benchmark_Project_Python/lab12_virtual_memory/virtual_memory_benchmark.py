import mmap
import time
import tempfile
import os

def run_benchmark(app=None):
    FILE_SIZE = 32 * 1024 * 1024  # 32MB
    filename = os.path.join(tempfile.gettempdir(), "virtmem.dat")
    with open(filename, "wb") as f:
        f.write(b'\0' * FILE_SIZE)

    with open(filename, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        start = time.time()
        for i in range(0, FILE_SIZE, 4096):
            mm[i] = 123
            if app and FILE_SIZE > 0:
                app.progress['value'] = int(100 * i / FILE_SIZE)
        elapsed = time.time() - start
        mm.close()
    return f"Wrote to every 4KB page in {elapsed:.2f} seconds"

def main(app=None):
    return run_benchmark(app)
