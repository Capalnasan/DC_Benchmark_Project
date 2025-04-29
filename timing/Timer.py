import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.total_time = 0
        self.running = False

    def start(self):
        self.start_time = time.perf_counter_ns()
        self.total_time = 0
        self.running = True

    def stop(self):
        if self.running:
            self.total_time += time.perf_counter_ns() - self.start_time
            self.running = False
        return self.total_time

    def pause(self):
        if self.running:
            self.total_time += time.perf_counter_ns() - self.start_time
            self.running = False
        return self.total_time

    def resume(self):
        if not self.running:
            self.start_time = time.perf_counter_ns()
            self.running = True
