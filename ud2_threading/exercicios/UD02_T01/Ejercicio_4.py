
import threading

class MiHilo(threading.Thread):

    def __init__(self, inicio, fin, nombre):
        super().__init__()
        self.inicio = inicio
        self.fin = fin
        self.nombre = nombre

    def run(self):
        print(f"{self.nombre}: Comienza")

        for i in range(self.inicio, self.fin + 1):
            print(f"{self.nombre}: {i}")

        print(f"{self.nombre}: Termina")


if __name__ == "__main__":

    hiloA = MiHilo(1, 10, "ThreadA")
    hiloB = MiHilo(20, 30, "ThreadB")

    print("Iniciar los dos threads")

    hiloA.start()
    hiloB.start()

    print("Los hilos se han inicializado")

    hiloA.join()
    hiloB.join()

    print("El programa principal ha terminado")
