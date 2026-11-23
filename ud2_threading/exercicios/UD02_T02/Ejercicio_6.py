
import threading

class Factorial(threading.Thread):

    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):

        print(f"Empieza el proceso ... cálculo del factorial de: {self.n}")

        resultado = 1

        for i in range(1, self.n + 1):
            resultado *= i

        print(f"Acabó el proceso ... el factorial de: {self.n} es {resultado}")


if __name__ == "__main__":

    lista_hilos = []

    for i in range(5, 10):
        hilo = Factorial(i)
        lista_hilos.append(hilo)

    for hilo in lista_hilos:
        hilo.start()

    for hilo in lista_hilos:
        hilo.join()

    print("Todos los factoriales han terminado")
