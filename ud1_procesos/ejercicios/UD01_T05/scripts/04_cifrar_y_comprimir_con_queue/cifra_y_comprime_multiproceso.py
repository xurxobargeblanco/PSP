# pipeline_queue.py
# Producer (cifra) → Queue → Consumer (comprime y escribe)
# 13.28 segs
# 218.11 segs fernet 10 vueltas

# 34.89 seg 100 vueltas siempre sobre data

import gzip
from pathlib import Path
import time
from multiprocessing import Process, Queue, cpu_count
from cryptography.fernet import Fernet

SENTINEL = None

def producer(file_queue: Queue, data_queue: Queue, key: bytes):
    fernet = Fernet(key)
    while True:
        try:
            p: Path = file_queue.get_nowait()
        except Exception:
            break
        data = p.read_bytes()
        enc = fernet.encrypt(data)            # rápido en comparación con compresión
        for _ in range(100):
            enc = fernet.encrypt(data)
        enc = fernet.encrypt(data)
        data_queue.put((p.name, enc))
        print("Encolado:", p.name)
    # indicar fin (tantos sentinels como consumidores)
    data_queue.put(SENTINEL)

def consumer(data_queue: Queue, outdir: Path):
    while True:
        item = data_queue.get()
        if item is SENTINEL:
            # reenviar sentinel para otros consumidores si existen
            data_queue.put(SENTINEL)
            break
        name, enc = item
        out = outdir / (name + ".gz")
        with gzip.open(out, 'wb') as f:
            f.write(enc)   # escribir comprimido
        print("Escrito:", out)

def main():
    key = Fernet.generate_key()
    files = list(Path("data").glob("*.txt"))
    Path("out").mkdir(exist_ok=True)
    file_q = Queue()
    data_q = Queue(maxsize=10)  # para experimentar backpressure
    for p in files:
        file_q.put(p)

    p_prod = Process(target=producer, args=(file_q, data_q, key))
    # Puedes lanzar más de un consumidor si la compresión puede paralelizarse sin conflicto
    p_cons = Process(target=consumer, args=(data_q, Path("out")))

    t0 = time.perf_counter()
    p_prod.start()
    p_cons.start()
    p_prod.join()
    p_cons.join()
    print("Tiempo total (pipeline Queue):", time.perf_counter() - t0)

if __name__ == "__main__":
    main()
