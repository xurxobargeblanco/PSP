import threading
import time
import random

# Objeto que almacenará datos específicos de cada hilo
datos_locales = threading.local()

def trabajador(id_hilo):
    # Cada hilo tendrá su "nombre" independiente aunque se use el mismo objeto
    datos_locales.nombre = f"Hilo-{id_hilo}"
    datos_locales.contador = 0

    for _ in range(5):
        time.sleep(random.uniform(0.1, 0.3))
        datos_locales.contador += 1
        print(f"[{datos_locales.nombre}] contador = {datos_locales.contador}")

if __name__ == "__main__":
    hilos = [threading.Thread(target=trabajador, args=(i,)) for i in range(3)]

    for h in hilos:
        h.start()

    for h in hilos:
        h.join()

    print("Finalizado.")