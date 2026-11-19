import threading

def escribe_yes():
    for i in range(30):
        print("YES",end="")

if __name__ == "__main__":
    print("INICIO")

    t = threading.Thread(target=escribe_yes)
    t.start()

    for i in range(30):
        print("NO", end="")

    t.join()