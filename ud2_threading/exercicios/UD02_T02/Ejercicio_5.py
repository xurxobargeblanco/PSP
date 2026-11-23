
import threading

class Factorial(threading.Thread):

    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        resultado = 1

        for i in range(1, self.n + 1):
            resultado *= i

        print(f"Factorial de {self.n}: {resultado}")


class Fibonacci(threading.Thread):

    def __init__(self, n):
        super().__init__()
        self.n = n

    def run(self):
        a = 0
        b = 1

        for i in range(self.n):
            a, b = b, a + b

        print(f"Fibonacci de {self.n}: {a}")


if __name__ == "__main__":

    numero = 10

    hilo1 = Factorial(numero)
    hilo2 = Fibonacci(numero)

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("Los dos cálculos han terminado")
