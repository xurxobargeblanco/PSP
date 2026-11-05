import gzip
import time
import os
from multiprocessing import Process, Queue
from cryptography.fernet import Fernet
from pathlib import Path

# 132.50 s backpressure cola 2
# 132.47 s sin backpressure cola 20, se ve que el cuello de botella está en la forma de procesar los ficheros leidos

INPUT_DIR = Path("data")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_QUEUE = 2  # fuerza back-pressure
NUM_CONSUMERS = 1

def producer(file_paths, queue):
    for path in file_paths:
        with open(path, "rb") as f:
            data = f.read()
        queue.put((path.name, data))  # bloquea si la cola está llena
        print(f"[Producer] Enqueued {path.name}")
    for _ in range(NUM_CONSUMERS):
        queue.put(None)  # fin de trabajo

def consumer(queue, key):
    fernet = Fernet(key)
    while True:
        item = queue.get()
        if item is None:
            break
        name, data = item
        print(f"[Consumer {os.getpid()}] Processing {name}")
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
    p_prod = Process(target=producer, args=(files, queue))
    p_cons = Process(target=consumer, args=(queue, key))
    p_prod.start()
    p_cons.start()
    p_prod.join()
    p_cons.join()
    t1 = time.perf_counter()
    
    print(f"Procesados {len(files)} ficheros en {t1 - t0:.2f} s (1 productor / 1 consumidor)")
