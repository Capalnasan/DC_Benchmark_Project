import random
from benchmark.IBenchmark import IBenchmark

class BubbleSortBenchmark(IBenchmark):
    def __init__(self):
        self.array = []
        self.running = True

    def initialize(self, size=1000):
        self.array = [random.randint(0, 10000) for _ in range(size)]

    def run(self, *params):
        n = len(self.array)
        for i in range(n):
            if not self.running:
                break
            for j in range(0, n-i-1):
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]

    def clean(self):
        self.array.clear()

    def cancel(self):
        self.running = False
