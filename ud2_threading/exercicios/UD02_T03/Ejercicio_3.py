import threading
import time

salida = threading.Event()

def corredor(nombre):

    print(f"Corredor esperando señal de salida")
    salida.wait()

    if salida == True : print(f"Corredor arranca carrera")
