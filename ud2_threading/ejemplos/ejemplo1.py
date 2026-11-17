import threading

def escribe_y():
    for i in range(1000):
        print("Y", end="")

if __name__ == "__main__":
    print("INICIO")

    t = threading.Thread(target=escribe_y)
    t.start()

    for i in range(1000):
        print("X", end="")

    t.join()
