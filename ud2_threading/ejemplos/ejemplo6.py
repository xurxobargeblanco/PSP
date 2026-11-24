import threading
import time

contador = 0
lock = threading.Lock()

def incrementar(n):
    global contador
    for _ in range(n):
        lock.acquire()
        try:
            temp = contador
            temp += 1
            time.sleep(0.001)
            contador = temp
        finally:
            lock.release()

if __name__ == "__main__":
    hilos = [threading.Thread(target=incrementar, args=(100,)) for _ in range(5)]
    for h in hilos: h.start()
    for h in hilos: h.join()
    print("Valor final (acquire/release):", contador)