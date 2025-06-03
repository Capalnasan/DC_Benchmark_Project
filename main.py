import os

files_content = {
    "README.md": '''
# DC Benchmark Project (Python GUI Version)

This project is a modern, easy-to-use benchmarking suite for CPU, RAM, Storage, and more, with a graphical interface and real-time status/progress bar.

## How to use

1. Install Python 3.8+ and (optionally) `numpy` for some RAM/Cache tests:
   pip install numpy

2. Run the app:
   python main.py

3. Click any benchmark button to run the test and see real-time progress and results.

## Structure

Each lab is in its own folder with its main Python script.
No external dependencies except standard Python and `numpy`.

## Benchmarks included

- CPU Benchmark
- RAM/Cache Benchmark
- Pi Calculation
- Fixed Point Arithmetic
- Storage Write
- Random HDD Access
- Virtual Memory
- Composite Score

Results are displayed in the GUI.
''',

    "main.py": '''
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import importlib

BENCHMARKS = [
    ("CPU Benchmark", "lab3_framework_test.cpu_benchmark"),
    ("RAM/Cache Benchmark", "lab6_cache_test.cache_test"),
    ("Pi Calculation", "lab4_pi_benchmark.pi_benchmark"),
    ("Fixed Point Arithmetic", "lab5_fixed_point.fixed_point_benchmark"),
    ("Storage Write Test", "file_write_benchmark.file_write_benchmark"),
    ("Random HDD Access", "lab11_hdd_random.hdd_random_access"),
    ("Virtual Memory Test", "lab12_virtual_memory.virtual_memory_benchmark"),
    ("Composite Score", "composite_score.composite_score")
]

class BenchmarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DC Benchmark Suite")
        self.geometry("500x430")
        self.resizable(False, False)
        self.configure(bg="#191c24")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="DC Benchmark Suite", font=("Segoe UI", 22, "bold"), bg="#191c24", fg="#fafbfc").pack(pady=(20, 10))
        frm = ttk.Frame(self)
        frm.pack(padx=20, pady=10, fill='x', expand=True)

        for i, (label, module_path) in enumerate(BENCHMARKS):
            b = ttk.Button(frm, text=label, command=lambda m=module_path, l=label: self.run_benchmark(m, l))
            b.pack(fill='x', pady=6)

        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate", maximum=100, length=460)
        self.progress.pack(side='bottom', pady=(20, 2), padx=20)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(self, textvariable=self.status_var, bg="#191c24", fg="#00dc6a", anchor='w')
        self.status_label.pack(side='bottom', fill='x', padx=22, pady=(0, 10))

    def run_benchmark(self, module_path, label):
        self.progress['value'] = 0
        self.status_var.set(f"Running: {label}")
        self.update_idletasks()
        t = threading.Thread(target=self._run_benchmark_thread, args=(module_path, label), daemon=True)
        t.start()

    def _run_benchmark_thread(self, module_path, label):
        try:
            self.set_progress_indeterminate(True)
            mod = importlib.import_module(module_path)
            if hasattr(mod, "run_benchmark"):
                result = mod.run_benchmark(self)
            elif hasattr(mod, "main"):
                result = mod.main(self)
            else:
                result = mod.__doc__ or "(No output)"
            self.set_progress_indeterminate(False)
            self.progress['value'] = 100
            self.status_var.set(f"{label} completed!")
            messagebox.showinfo("Result", f"{label}:\n\n{result}")
        except Exception as e:
            self.set_progress_indeterminate(False)
            self.status_var.set("Error!")
            messagebox.showerror("Benchmark Error", f"{label} failed:\n{e}")

    def set_progress_indeterminate(self, enable=True):
        if enable:
            self.progress.config(mode="indeterminate")
            self.progress.start(10)
        else:
            self.progress.stop()
            self.progress.config(mode="determinate")

if __name__ == "__main__":
    app = BenchmarkApp()
    app.mainloop()
''',

    "lab2_project_setup/__init__.py": '''# Lab 2 - Project Setup\n# No benchmark, just project folder structure.\n''',

    "lab3_framework_test/cpu_benchmark.py": '''
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
''',

    "lab4_pi_benchmark/pi_benchmark.py": '''
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
    return f"Calculated pi with {n} terms in {elapsed:.3f}s\\nApprox value: {pi_val}"

def main(app=None):
    return run_benchmark(app)
''',

    "lab5_fixed_point/fixed_point_benchmark.py": '''
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
''',

    "lab6_cache_test/cache_test.py": '''
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
    return "\\n".join(output)

def main(app=None):
    return run_benchmark(app)
''',

    "file_write_benchmark/file_write_benchmark.py": '''
import os
import time
import tempfile

def write_test_file(filename, file_size_bytes, buffer_size_bytes, app=None):
    data = b'A' * buffer_size_bytes
    total_written = 0
    start_time = time.time()
    percent_last = 0
    with open(filename, "wb") as f:
        while total_written < file_size_bytes:
            to_write = min(buffer_size_bytes, file_size_bytes - total_written)
            f.write(data[:to_write])
            total_written += to_write
            if app and file_size_bytes > 0:
                percent = int(100 * total_written / file_size_bytes)
                if percent != percent_last:
                    app.progress['value'] = percent
                    percent_last = percent
    elapsed = time.time() - start_time
    speed = (file_size_bytes / 1024**2) / elapsed  # MB/s
    return speed, elapsed

def run_benchmark(app=None):
    TEMP_FOLDER = os.path.join(tempfile.gettempdir(), "bench")
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    file_sizes_mb = [1, 8, 32]
    speeds = []
    for i, size_mb in enumerate(file_sizes_mb):
        file_size = int(size_mb * 1024**2)
        filename = os.path.join(TEMP_FOLDER, f"write_size_{size_mb}MB_{i}.dat")
        speed, elapsed = write_test_file(filename, file_size, 1024, app)
        speeds.append(speed)
        os.remove(filename)
    avg_speed = sum(speeds) / len(speeds)
    if app:
        app.progress['value'] = 100
    return "Write Speeds (MB/s): " + ", ".join(f"{s:.2f}" for s in speeds) + f"\\nAverage: {avg_speed:.2f}"

def main(app=None):
    return run_benchmark(app)
''',

    "composite_score/composite_score.py": '''
def composite_score(cpu, ram, storage, weights=(0.4, 0.3, 0.3)):
    return cpu * weights[0] + ram * weights[1] + storage * weights[2]

def run_benchmark(app=None):
    cpu_score = float(input("CPU score: "))
    ram_score = float(input("RAM score: "))
    storage_score = float(input("Storage score: "))
    score = composite_score(cpu_score, ram_score, storage_score)
    if app:
        app.progress['value'] = 100
    return f"Composite Score: {score:.2f}"

def main(app=None):
    return run_benchmark(app)
''',

    "lab11_hdd_random/hdd_random_access.py": '''
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
''',

    "lab12_virtual_memory/virtual_memory_benchmark.py": '''
import mmap
import time
import tempfile
import os

def run_benchmark(app=None):
    FILE_SIZE = 32 * 1024 * 1024  # 32MB
    filename = os.path.join(tempfile.gettempdir(), "virtmem.dat")
    with open(filename, "wb") as f:
        f.write(b'\\0' * FILE_SIZE)

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
'''
}

structure = [
    "lab2_project_setup/__init__.py",
    "lab3_framework_test/cpu_benchmark.py",
    "lab4_pi_benchmark/pi_benchmark.py",
    "lab5_fixed_point/fixed_point_benchmark.py",
    "lab6_cache_test/cache_test.py",
    "file_write_benchmark/file_write_benchmark.py",
    "composite_score/composite_score.py",
    "lab11_hdd_random/hdd_random_access.py",
    "lab12_virtual_memory/virtual_memory_benchmark.py"
]

root = "DC_Benchmark_Project_Python"
os.makedirs(root, exist_ok=True)

# Root files
for root_file in ["main.py", "README.md"]:
    with open(os.path.join(root, root_file), "w", encoding="utf-8") as f:
        f.write(files_content[root_file].strip() + "\n")

# Subfolder files
for file_path in structure:
    folder = os.path.join(root, os.path.dirname(file_path))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(root, file_path), "w", encoding="utf-8") as f:
        f.write(files_content[file_path].strip() + "\n")

print("Project created successfully!")
