#!/usr/bin/env python3
import sys, os, threading, random, time
from PyQt5 import QtCore, QtGui, QtWidgets

# ─── allow imports from your project packages ────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
from benchmark.BubbleSortBenchmark import BubbleSortBenchmark
from timing.Timer             import Timer
# ────────────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Benchmark GUI")
        self.resize(500, 300)
        self._build_ui()
        self._apply_light_theme()

    def _build_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        # Title
        title = QtWidgets.QLabel("Benchmark Dashboard")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        layout.addWidget(title)

        # Input row
        row = QtWidgets.QHBoxLayout()
        lbl = QtWidgets.QLabel("Array Size:")
        lbl.setFont(QtGui.QFont("Segoe UI", 11))
        row.addWidget(lbl)

        self.size_input = QtWidgets.QLineEdit("500")
        self.size_input.setFixedWidth(80)
        row.addWidget(self.size_input)

        self.run_btn = QtWidgets.QPushButton("Run")
        self.run_btn.setFixedWidth(80)
        self.run_btn.clicked.connect(self.start_benchmark)
        row.addWidget(self.run_btn)

        layout.addLayout(row)

        # Result display
        self.result_lbl = QtWidgets.QLabel("Execution Time: N/A")
        self.result_lbl.setFont(QtGui.QFont("Segoe UI", 11))
        self.result_lbl.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.result_lbl)

        # Theme switch
        self.theme_btn = QtWidgets.QPushButton("Switch to Dark Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)

        layout.addStretch()

    def start_benchmark(self):
        try:
            n = int(self.size_input.text())
            assert n>0
        except:
            QtWidgets.QMessageBox.critical(self, "Error", "Enter a positive integer!")
            return
        self.run_btn.setEnabled(False)
        threading.Thread(target=self._run_bench, args=(n,), daemon=True).start()

    def _run_bench(self, n):
        bench = BubbleSortBenchmark()
        timer = Timer()
        bench.initialize(n)
        timer.start()
        bench.run()
        elapsed = timer.stop()
        bench.clean()
        QtCore.QMetaObject.invokeMethod(self, "_finish",
            QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(int, elapsed))

    @QtCore.pyqtSlot(int)
    def _finish(self, elapsed):
        self.result_lbl.setText(f"Execution Time: {elapsed:,} ns")
        self.run_btn.setEnabled(True)

    def toggle_theme(self):
        if self._is_light:
            self._apply_dark_theme()
            self.theme_btn.setText("Switch to Light Mode")
        else:
            self._apply_light_theme()
            self.theme_btn.setText("Switch to Dark Mode")

    def _apply_light_theme(self):
        self._is_light = True
        QtWidgets.QApplication.setStyle("Fusion")
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window,        QtGui.QColor("#f5f5f5"))
        pal.setColor(QtGui.QPalette.Base,          QtGui.QColor("#ffffff"))
        pal.setColor(QtGui.QPalette.Button,        QtGui.QColor("#e0e0e0"))
        pal.setColor(QtGui.QPalette.ButtonText,    QtGui.QColor("#202020"))
        pal.setColor(QtGui.QPalette.WindowText,    QtGui.QColor("#202020"))
        pal.setColor(QtGui.QPalette.Text,          QtGui.QColor("#202020"))
        pal.setColor(QtGui.QPalette.Highlight,     QtGui.QColor("#3399ff"))
        pal.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
        QtWidgets.QApplication.setPalette(pal)

    def _apply_dark_theme(self):
        self._is_light = False
        QtWidgets.QApplication.setStyle("Fusion")
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Window,        QtGui.QColor("#2b2b2b"))
        pal.setColor(QtGui.QPalette.Base,          QtGui.QColor("#3c3f41"))
        pal.setColor(QtGui.QPalette.Button,        QtGui.QColor("#4b4b4b"))
        pal.setColor(QtGui.QPalette.ButtonText,    QtGui.QColor("#ffffff"))
        pal.setColor(QtGui.QPalette.WindowText,    QtGui.QColor("#ffffff"))
        pal.setColor(QtGui.QPalette.Text,          QtGui.QColor("#ffffff"))
        pal.setColor(QtGui.QPalette.Highlight,     QtGui.QColor("#3399ff"))
        pal.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
        QtWidgets.QApplication.setPalette(pal)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec_())
