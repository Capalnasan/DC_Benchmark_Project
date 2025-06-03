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
    return "Write Speeds (MB/s): " + ", ".join(f"{s:.2f}" for s in speeds) + f"\nAverage: {avg_speed:.2f}"

def main(app=None):
    return run_benchmark(app)
