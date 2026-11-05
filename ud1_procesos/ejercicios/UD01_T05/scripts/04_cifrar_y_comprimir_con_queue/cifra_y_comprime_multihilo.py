# pipeline_multihilo.py
# (NO mejora la velocidad, el GIL limita el cifrado CPU-Bound)
import gzip
import time
from pathlib import Path
import threading
import queue # ¡Importante! La cola Thread-Safe
from cryptography.fernet import Fernet

# 31.98   100 vueltas siempre sobre data

SENTINEL = None
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

# Las funciones de Productor y Consumidor usan la misma lógica,
# solo cambian los objetos de concurrencia.

def producer_thread(file_queue: queue.Queue, data_queue: queue.Queue, key: bytes):
    """Hilo 1: Lee y cifra (CPU-Bound)."""
    fernet = Fernet(key)
    while True:
        p = file_queue.get()
        file_queue.task_done() # Necesario si se usa join() en el main
        
        if p is SENTINEL:
            break
            
        data = p.read_bytes()
        # Tarea Pesada CPU-Bound (10 rondas de cifrado)
        enc = fernet.encrypt(data)
        for _ in range(100):
            enc = fernet.encrypt(data)
        enc = fernet.encrypt(data)    
        data_queue.put((p.name, enc))
        # print("P-Encolado:", p.name)
        
    # Envía el centinela
    data_queue.put(SENTINEL)

def consumer_thread(data_queue: queue.Queue):
    """Hilo 2: Comprime y escribe (I/O-Bound)."""
    while True:
        item = data_queue.get()
        data_queue.task_done() # Necesario si se usa join() en el main
        
        if item is SENTINEL:
            break
            
        name, enc = item
        out = OUTPUT_DIR / (name + ".gz")
        
        # Tarea I/O-Bound
        with gzip.open(out, 'wb') as f:
            f.write(enc)
            
        # print("C-Escrito:", out)

def main_multihilo():
    key = Fernet.generate_key()
    files = list(Path("data").glob("*.txt"))
    
    # Colas de threading
    file_q = queue.Queue() 
    data_q = queue.Queue(maxsize=10) 
    
    for p in files:
        file_q.put(p)
    file_q.put(SENTINEL)

    t_prod = threading.Thread(target=producer_thread, args=(file_q, data_q, key))
    t_cons = threading.Thread(target=consumer_thread, args=(data_q,))

    t0 = time.perf_counter()
    t_prod.start()
    t_cons.start()
    
    t_prod.join()
    t_cons.join()
    
    # También se podría usar data_q.join() si se manejan correctamente los task_done
    
    tiempo_total = time.perf_counter() - t0
    print("-" * 50)
    print(f"TIEMPO TOTAL (Multihilo Pipeline): {tiempo_total:.2f} segundos")
    print("-" * 50)

if __name__ == "__main__":
    main_multihilo()