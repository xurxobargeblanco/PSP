import threading
import time

rlock = threading.RLock()

def operacion_A():
    with rlock:
        print("[A] Inicio")
        time.sleep(0.2)
        operacion_B()
        print("[A] Fin")

def operacion_B():
    with rlock:
        print("[B] Ejecutando")
        time.sleep(0.2)

if __name__ == "__main__":
    t = threading.Thread(target=operacion_A)
    t.start()
    t.join()