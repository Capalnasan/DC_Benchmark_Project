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

        for label, module_path in BENCHMARKS:
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
