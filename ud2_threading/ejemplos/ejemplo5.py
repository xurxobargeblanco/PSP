import threading
import time

class TareaContador(threading.Thread):
    def __init__(self, nombre, limite, delay=1):
        super().__init__(name=nombre)
        self.limite = limite
        self.delay = delay

    def run(self):
        for i in range(1, self.limite + 1):
            print(f"Name: [{self.name}], Ident: [{self.ident}]  Valor: {i}")
            time.sleep(self.delay)

if __name__ == "__main__":
    hilo = TareaContador("ContadorHilo", limite=5, delay=0.5)

    print("[Principal] Iniciando hilo contador...")
    hilo.start()

    hilo.join()
    print("[Principal] El hilo contador ha terminado.")

