import threading
import time
import random

evento_inicio = threading.Event()

def trabajador(id_hilo):
    print(f"[Trabajador {id_hilo}] Preparado. Esperando señal para iniciar...")
    evento_inicio.wait()  # Bloqueo aquí hasta que alguien llame set()
    # Una vez set(), todos los wait() devuelven inmediatamente
    print(f"[Trabajador {id_hilo}] Señal recibida. Ejecutando tarea...")
    time.sleep(random.uniform(0.5, 1.2))
    print(f"[Trabajador {id_hilo}] Tarea finalizada.")

def supervisor():
    print("[Supervisor] Realizando comprobaciones previas...")
    time.sleep(2)
    print("[Supervisor] Todo OK. Lanzando la señal de inicio.")
    evento_inicio.set()  # Activa el evento (persistente)

if __name__ == "__main__":
    threads = [threading.Thread(target=trabajador, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()

    # Lanzamos el supervisor en el hilo principal
    supervisor()

    for t in threads:
        t.join()
    print("[Principal] Todos los trabajadores han terminado.")