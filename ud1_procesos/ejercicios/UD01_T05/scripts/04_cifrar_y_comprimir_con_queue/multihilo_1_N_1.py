# pipeline_multihilo_3_etapas.py
import gzip
import time
from pathlib import Path
import threading
import queue # La cola para hilos
import hashlib

# 50 vueltas 1 cifradores 

# 5000000 vueltas 1 cifrador 92.82 segundos

# --- Configuración ---
SENTINEL = None
VUELTAS_CPU = 5000000  # Debe ser el mismo valor que en la versión multiproceso
NUM_CIPHERS = 2 # El mismo número de workers para la comparación
INPUT_DIR = Path("data")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True) 

def cpu_intensive_work(data: bytes) -> bytes:
    """Simula una tarea CPU-Bound intensiva con hashing."""
    enc = data
    for _ in range(VUELTAS_CPU):
        enc = hashlib.sha256(enc).digest() 
    return enc

# Las funciones son casi idénticas, pero usan threading.Thread y queue.Queue

def reader_thread(file_paths, q_read: queue.Queue):
    """Hilo 1: Lee ficheros (I/O-Bound) y encola."""
    # ... (lógica idéntica a reader_process)
    for p in file_paths:
        data = p.read_bytes()
        q_read.put((p.name, data))
    
    for _ in range(NUM_CIPHERS):
        q_read.put(SENTINEL)

def cipher_thread(q_read: queue.Queue, q_cipher: queue.Queue):
    """Hilo 2: Cifra (CPU-Bound) y encola. N hilos workers."""
    while True:
        item = q_read.get()
        q_read.task_done() # Necesario para join
        
        if item is SENTINEL:
            q_cipher.put(SENTINEL)
            break
            
        name, data = item
        # Tarea CPU-Bound. El GIL bloqueará el paralelismo real aquí.
        enc = cpu_intensive_work(data) 
        q_cipher.put((name, enc))

def compressor_thread(q_cipher: queue.Queue):
    """Hilo 3: Comprime y escribe (I/O-Bound)."""
    while True:
        item = q_cipher.get()
        q_cipher.task_done()
        
        if item is SENTINEL:
            break
            
        name, data = item
        out = OUTPUT_DIR / (name + ".gz")
        
        # Tarea I/O-Bound
        compressed = gzip.compress(data)
        out.write_bytes(compressed)

def main_multihilo():
    files = list(INPUT_DIR.glob("*.txt"))
    if not files:
        print("¡Advertencia! No hay ficheros .txt en el directorio 'data'.")
        return

    # Colas de comunicación entre hilos
    q_read = queue.Queue()   # Lector -> Cifradores
    q_cipher = queue.Queue() # Cifradores -> Compresor

    t0 = time.perf_counter()
    
    # 1. Lector (Hilo)
    t_reader = threading.Thread(target=reader_thread, args=(files, q_read))
    
    # 2. Cifradores (N Hilos CPU-Bound)
    t_ciphers = [
        threading.Thread(target=cipher_thread, args=(q_read, q_cipher))
        for _ in range(NUM_CIPHERS)
    ]
    
    # 3. Compresor (Hilo)
    t_compressor = threading.Thread(target=compressor_thread, args=(q_cipher,))

    # Iniciar
    t_reader.start()
    for t in t_ciphers:
        t.start()
    t_compressor.start()

    # Esperar finalización
    t_reader.join()
    for t in t_ciphers:
        t.join()
    t_compressor.join()

    tiempo_total = time.perf_counter() - t0
    print("-" * 60)
    print(f"TIEMPO TOTAL (Multihilo 3 Etapas con {NUM_CIPHERS} Cifradores): {tiempo_total:.2f} segundos")
    print("-" * 60)

if __name__ == "__main__":
    main_multihilo()