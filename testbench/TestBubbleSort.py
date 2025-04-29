import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from benchmark.BubbleSortBenchmark import BubbleSortBenchmark
from timing.Timer import Timer
from mylogging.ConsoleLogger import ConsoleLogger

if __name__ == "__main__":
    logger = ConsoleLogger()
    benchmark = BubbleSortBenchmark()
    timer = Timer()

    benchmark.initialize(500)  # Initialize array with 500 random numbers

    timer.start()
    benchmark.run()
    elapsed_time_ns = timer.stop()

    logger.write("Execution time:", elapsed_time_ns, "nanoseconds")

    benchmark.clean()
    logger.close()
