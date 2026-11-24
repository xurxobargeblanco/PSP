
import threading
import time

class MiHilo(threading.Thread):

    def __init__(self, nombre):
        super().__init__(name = nombre)

    def run(self):
        try:
            for i in range(1, 101):
                print(f"Valor desde hilo con ident {self.ident} - Nombre: {self.nombre}")
                time.sleep(0.1)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":

    inicio = time.perf_counter()

    hilo = MiHilo("ThreadA", 1)

    hilo.start()

    hilo.join()

    fin = time.perf_counter()

    print(f"Tiempo total de ejecución: {fin - inicio:.2f} segundos")
