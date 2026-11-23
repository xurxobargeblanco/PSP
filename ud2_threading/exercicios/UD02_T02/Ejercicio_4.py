
import threading
import time

class MiHilo(threading.Thread):

    def __init__(self, nombre, id):
        super().__init__()
        self.nombre = nombre
        self.id = id

    def run(self):
        try:
            for i in range(1, 101):
                print(f"Valor {i} - Hilo {self.id} - Nombre: {self.nombre}")
                time.sleep(0.1)

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":

    inicio = time.time()

    lista_hilos = []

    for i in range(1, 6):
        hilo = MiHilo(f"miHilo-{i}", i)
        lista_hilos.append(hilo)

    for hilo in lista_hilos:
        hilo.start()

    for hilo in lista_hilos:
        hilo.join()

    fin = time.time()

    print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")
