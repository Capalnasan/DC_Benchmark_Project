#!/usr/bin/env python3
import sys, os, threading, random, time
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

# ─ make sure imports see your packages ────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from benchmark.BubbleSortBenchmark import BubbleSortBenchmark
from timing.Timer             import Timer
# ──────────────────────────────────────────────────────────────────

class ModernApp(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")      # try "arc", "plastik", "equilux", "black"
        self.title("Benchmark Dashboard")
        self.geometry("500x320")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        PAD = {"padx":20, "pady":10}
        frm = ttk.Frame(self, relief="flat")
        frm.pack(fill="both", expand=True, **PAD)

        # Title
        lbl = ttk.Label(frm, text="📊 Benchmark Dashboard", font=("Segoe UI", 18, "bold"))
        lbl.pack(**PAD)

        # Input + run
        row = ttk.Frame(frm)
        row.pack(**PAD)
        ttk.Label(row, text="Array Size:", font=("Segoe UI", 11)).pack(side="left")
        self.size = tk.StringVar(value="500")
        ttk.Entry(row, textvariable=self.size, width=8, font=("Segoe UI", 11)).pack(side="left", padx=10)
        self.btn = ttk.Button(row, text="Run ►", command=self._on_run)
        self.btn.pack(side="left")

        # Result “card”
        card = ttk.Frame(frm, relief="groove", borderwidth=2)
        card.pack(fill="x", **PAD)
        self.result = ttk.Label(card, text="Execution Time: N/A", font=("Segoe UI", 12))
        self.result.pack(pady=10)

        # Theme chooser
        throw = ttk.Frame(frm)
        throw.pack(**PAD)
        ttk.Label(throw, text="Theme:", font=("Segoe UI", 11)).pack(side="left")
        themes = self.get_themes()
        self.thvar = tk.StringVar(value=self.get_theme())
        cb = ttk.Combobox(throw, textvariable=self.thvar, values=themes, state="readonly", width=15)
        cb.pack(side="left", padx=10)
        cb.bind("<<ComboboxSelected>>", lambda e: self.set_theme(self.thvar.get()))

    def _on_run(self):
        try:
            n = int(self.size.get()); assert n>0
        except:
            messagebox.showerror("Error", "Enter a positive integer.")
            return
        self.btn.state(["disabled"])
        threading.Thread(target=self._run, args=(n,), daemon=True).start()

    def _run(self, n):
        b = BubbleSortBenchmark()
        t = Timer()
        b.initialize(n)
        t.start()
        b.run()
        elapsed = t.stop()
        b.clean()
        self.after(0, lambda: self._finish(elapsed))

    def _finish(self, elapsed):
        self.result.config(text=f"Execution Time: {elapsed:,} ns")
        self.btn.state(["!disabled"])

if __name__=="__main__":
    ModernApp().mainloop()
