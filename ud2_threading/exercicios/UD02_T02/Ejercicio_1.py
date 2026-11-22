
import threading
import time

class MiHilo(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            time.sleep(2)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":

    hilo = MiHilo()

    print("Estado antes de executar:", hilo.is_alive())

    hilo.start()

    print("Estado durante a execución:", hilo.is_alive())

    hilo.join()

    print("Estado despois de finalizar:", hilo.is_alive())
