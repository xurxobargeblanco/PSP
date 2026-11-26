import threading
import time
import random

capacidad_max = threading.Semaphore(3)

def cliente(cliente_id):

    print(f"El cliente {cliente_id} esta esperando para entrar al probador")

    with capacidad_max:

        print(f"El cliente {cliente_id} esta en el probador")
        time.sleep(random.uniform(2,5))
        print(f"El cliente {cliente_id} ha salido del probador")

if __name__ == "__main__":

    lista_hilos = [threading.Thread(target=cliente, args=(i,)) for i in range(1, 9)]

    for h in lista_hilos: h.start()
    for h in lista_hilos: h.join()

    print(f"Todos los clientes han acabado")