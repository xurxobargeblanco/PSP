import gzip
import time
import os
from multiprocessing import Process, Queue, cpu_count
from cryptography.fernet import Fernet
from pathlib import Path

# 104.21 s (1 productor / 4 consumidores)
# 100.05 s (1 productor / 4 consumidores) sin límite en la cola

INPUT_DIR = Path("data")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_QUEUE = 3
NUM_CONSUMERS = min(4, cpu_count())  # ajusta según núcleos disponibles

def producer(file_paths, queue):
    for path in file_paths:
        with open(path, "rb") as f:
            data = f.read()
        queue.put((path.name, data))
        print(f"[Producer] Enqueued {path.name}")
    for _ in range(NUM_CONSUMERS):
        queue.put(None)

def consumer(queue, key):
    fernet = Fernet(key)
    while True:
        item = queue.get()
        if item is None:
            break
        name, data = item
        print(f"[Consumer {os.getpid()}] Start {name}")
        for _ in range(10):
            data = fernet.encrypt(data)
        compressed = gzip.compress(data)
        out_path = OUTPUT_DIR / f"{name}.gz"
        with open(out_path, "wb") as f:
            f.write(compressed)
        print(f"[Consumer {os.getpid()}] Done {name}")

if __name__ == "__main__":
    files = list(INPUT_DIR.glob("*.txt"))
    key = Fernet.generate_key()
    queue = Queue(maxsize=MAX_QUEUE)
    
    t0 = time.perf_counter()
    producer_proc = Process(target=producer, args=(files, queue))
    consumers = [Process(target=consumer, args=(queue, key)) for _ in range(NUM_CONSUMERS)]
    
    producer_proc.start()
    for c in consumers:
        c.start()
    
    producer_proc.join()
    for c in consumers:
        c.join()
    
    t1 = time.perf_counter()
    print(f"Procesados {len(files)} ficheros en {t1 - t0:.2f} s (1 productor / {NUM_CONSUMERS} consumidores)")
