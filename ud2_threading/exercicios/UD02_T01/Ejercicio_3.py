
import threading

contador = 0

class MiHilo(threading.Thread):

    def __init__(self, mensaje):
        super().__init__()
        self.mensaje = mensaje

    def run(self):
        global contador

        for i in range(10):
            contador += 1
            print(contador, self.mensaje)


if __name__ == "__main__":

    hilo1 = MiHilo("SI")
    hilo2 = MiHilo("NO")

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("Contador final:", contador)
