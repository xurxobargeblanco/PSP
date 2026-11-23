import threading
import time
import random

class MiHilo(threading.Thread):

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.tiempo = random.randint(0,10)

    def run(self):
        try:
            print(f"El {self.nombre} va a estar dormido durante {self.tiempo * 1000} milisegundos.")

            time.sleep(self.tiempo)

            print(f"{self.nombre} ha despertado")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":

    hilo1 = MiHilo("Hilo1")
    hilo2 = MiHilo("Hilo2")
    hilo3 = MiHilo("Hilo3")

    hilo1.start()
    hilo2.start()
    hilo3.start()

    hilo1.join()
    hilo2.join()
    hilo3.join()

    print("Todos los hilos han terminado")


