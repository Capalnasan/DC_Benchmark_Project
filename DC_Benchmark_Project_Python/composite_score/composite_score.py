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
