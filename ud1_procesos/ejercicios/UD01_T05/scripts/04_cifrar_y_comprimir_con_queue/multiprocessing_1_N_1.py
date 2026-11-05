# pipeline_multiproceso_3_etapas.py
import gzip
import time
from pathlib import Path
from multiprocessing import Process, Queue, cpu_count
import hashlib


# 50 vueltas 2 cifradores 11.33 segundos

# 5000000 vueltas 2 cifradores 55.46 segundos

# --- Configuración ---
SENTINEL = None
VUELTAS_CPU = 5000000  # Carga de CPU ajustable (cuello de botella)
NUM_CIPHERS = min(2, cpu_count()) # Número de procesos CPU-Bound
INPUT_DIR = Path("data")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True) # Asegurar el directorio de datos

def cpu_intensive_work(data: bytes) -> bytes:
    """Simula una tarea CPU-Bound intensiva con hashing."""
    enc = data
    for _ in range(VUELTAS_CPU):
        enc = hashlib.sha256(enc).digest() 
    return enc

def reader_process(file_paths, q_read: Queue):
    """Proceso 1: Lee ficheros (I/O-Bound) y encola."""
    for p in file_paths:
        data = p.read_bytes()
        q_read.put((p.name, data))
        # print(f"[Lector] Encolado: {p.name}")
        
    # Enviar un centinela para cada proceso cifrador
    for _ in range(NUM_CIPHERS):
        q_read.put(SENTINEL)

def cipher_process(q_read: Queue, q_cipher: Queue):
    """Proceso 2: Cifra (CPU-Bound) y encola. Puede haber N procesos."""
    while True:
        item = q_read.get()
        if item is SENTINEL:
            # Reenviar centinela al compresor y terminar
            q_cipher.put(SENTINEL)
            break
            
        name, data = item
        enc = cpu_intensive_work(data) # Tarea CPU-Bound
        q_cipher.put((name, enc))
        # print(f"[Cifrador-{Process.pid}] Procesado: {name}")

def compressor_process(q_cipher: Queue):
    """Proceso 3: Comprime y escribe (I/O-Bound)."""
    while True:
        item = q_cipher.get()
        if item is SENTINEL:
            break
            
        name, data = item
        out = OUTPUT_DIR / (name + ".gz")
        
        # Tarea I/O-Bound (compresión y escritura)
        compressed = gzip.compress(data)
        out.write_bytes(compressed)
        # print(f"[Compresor] Escrito: {out.name}")

def main_multiproceso():
    files = list(INPUT_DIR.glob("*.txt"))
    if not files:
        print("¡Advertencia! No hay ficheros .txt en el directorio 'data'.")
        return

    # Colas de comunicación entre procesos
    q_read = Queue()   # Lector -> Cifradores
    q_cipher = Queue() # Cifradores -> Compresor

    t0 = time.perf_counter()
    
    # 1. Lector (Proceso)
    p_reader = Process(target=reader_process, args=(files, q_read))
    
    # 2. Cifradores (N Procesos CPU-Bound)
    p_ciphers = [
        Process(target=cipher_process, args=(q_read, q_cipher))
        for _ in range(NUM_CIPHERS)
    ]
    
    # 3. Compresor (Proceso)
    p_compressor = Process(target=compressor_process, args=(q_cipher,))

    # Iniciar procesos
    p_reader.start()
    for p in p_ciphers:
        p.start()
    p_compressor.start()

    # Esperar finalización
    p_reader.join()
    for p in p_ciphers:
        p.join()
    p_compressor.join()

    tiempo_total = time.perf_counter() - t0
    print("-" * 60)
    print(f"TIEMPO TOTAL (Multiproceso 3 Etapas con {NUM_CIPHERS} Cifradores): {tiempo_total:.2f} segundos")
    print("-" * 60)

if __name__ == "__main__":
    main_multiproceso()