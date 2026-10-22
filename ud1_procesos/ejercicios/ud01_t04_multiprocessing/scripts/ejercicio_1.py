import multiprocessing
import time
import random

def llenar_lista(lista):
    print('Llenar lista con numeros del 1 al 100')
    for i in range(100):
        lista[i] = i + 1
        time.sleep(random.random() * 0.1)

    print(f"\n[Proceso 1 - Finalizado] : {list(lista)}\n")

def producto_lista(lista):
    print("Lista multiplicada por 2")
    for i in range(100):
        lista[i] *= 2
        time.sleep(random.random() * 0.1)

    print(f"\n[Proceso 2 - Finalizado] : {list(lista)}\n")


if __name__ == "__main__":
    mylist = multiprocessing.Array('i', 100)
    
    proceso1 = multiprocessing.Process(target=llenar_lista, args=(mylist,))
    proceso2 = multiprocessing.Process(target=producto_lista, args=(mylist,))

    proceso1.start()
    proceso1.join() 

    proceso2.start()
    proceso2.join()

    print(f"Lista final desde main : {mylist[:]}")
    