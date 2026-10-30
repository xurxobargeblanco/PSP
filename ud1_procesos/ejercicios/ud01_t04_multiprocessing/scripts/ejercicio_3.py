import multiprocessing
import random

def num_aleatorios(cola):
    for i in range(5):
        numero = random.randint(1,10)
        print(f"Numero generado: {numero}")
        cola.put(numero)
    
    cola.put(None)

def calcular_suma(cola):
    suma = 0

    while True:
        numero = cola.get()

        if numero is None:
            break

        suma += numero

    print(f"A suma total e : {suma}")

if __name__ == "__main__":
    cola = multiprocessing.Queue()

    proceso1 = multiprocessing.Process(
        target = num_aleatorios,
        args=(cola,)
    )

    proceso2 = multiprocessing.Process(
        target = calcular_suma,
        args=(cola,)
    )

    proceso1.start()
    proceso2.start()

    proceso1.join()
    proceso2.join()

    cola.close()

    
