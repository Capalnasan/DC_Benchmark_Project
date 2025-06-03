# DC Benchmark Suite (Python GUI Version)

The DC Benchmark Suite is a comprehensive performance measurement tool designed to evaluate system components such as CPU, memory, storage, and more. It features a dynamic graphical interface that displays real-time progress and detailed results for each test.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Usage](#usage)
4. [Project Architecture](#project-architecture)
5. [Benchmark Details](#benchmark-details)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

This project provides a range of benchmarks to help users identify performance characteristics and potential bottlenecks on their systems. Whether you are a developer needing to test your hardware or a system administrator monitoring performance, this tool offers clear insights through its advanced tests and graphical representation.

## Installation & Setup

### Prerequisites

- Python 3.8 or later.
- (Optional) NumPy for enhanced memory and cache tests:

  pip install numpy

### Installation Steps

1. Clone the repository:

   git clone https://github.com/yourusername/DC_Benchmark_Project.git

2. Change directory to the project folder:

   cd DC_Benchmark_Project/DC_Benchmark_Project_Python

3. Install the required packages if needed:

   pip install numpy

## Usage

1. Launch the application by executing:

   python main.py

2. Use the graphical interface to select any benchmark:
   - Click the respective test button.
   - Observe real-time progress updates.
   - View detailed results on completion.

## Project Architecture

Each benchmark is organized into its own folder, enhancing modularity and ease of maintenance.

### Directory Structure

```
DC_Benchmark_Project_Python/
├── main.py                   # Main application entry point
├── cpu_benchmark/
│   └── cpu_test.py           # CPU performance tests
├── memory_benchmark/
│   └── ram_cache_test.py     # Memory and cache evaluations
├── disk_benchmark/
│   ├── storage_write.py      # Sequential storage write tests
│   └── random_hdd_access.py  # Random HDD access performance
├── misc/
│   ├── pi_calculation.py     # Pi calculation benchmark
│   └── fixed_point.py        # Fixed point arithmetic tests
└── docs/
   └── README.md             # This documentation file
```

## Benchmark Details

- **CPU Benchmark:** Tests for evaluating processing speed and multi-threading performance.
- **Memory & Cache Benchmark:** Analyzes the efficiency of RAM and cache layers.
- **Storage Tests:** Conducts both sequential write operations and randomized HDD access tests.
- **Computational Challenges:**
  - Pi Calculation for numerical precision.
  - Fixed Point Arithmetic for simulating domain-specific calculations.
- **Virtual Memory:** Assesses system paging efficiency and virtual memory handling.
- **Composite Score:** Aggregates all benchmarks into an overall system performance score.

## Contributing

We welcome contributions to enhance and expand this suite. To contribute:

1. Fork the repository.
2. Create a feature branch for your modifications.
3. Submit a pull request with a clear description of your changes.
4. Ensure coding standards and documentation are maintained.

## License

This project is licensed under the MIT License. See the LICENSE file for further details.

For support or to report issues, please open a ticket in the GitHub repository.
