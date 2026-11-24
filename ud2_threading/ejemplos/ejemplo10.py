import threading
import time
import random

sem = threading.Semaphore(2)  # 2 "plazas"

def tarea(id_hilo):
    print(f"[{id_hilo}] Esperando plaza...")
    with sem:  # Semaphore soporta context manager desde Python 3.2
        print(f"[{id_hilo}] Ha entrado (ocupando plaza).")
        time.sleep(random.uniform(0.5, 1.5))
        print(f"[{id_hilo}] Sale (libera plaza).")

if __name__ == "__main__":
    hilos = [threading.Thread(target=tarea, args=(i,)) for i in range(6)]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print("Todos han pasado por la región crítica.")