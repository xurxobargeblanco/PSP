
import threading

def escribe_x():
    for i in range(30):
        print("NO", end="")

def escribe_y():
    for i in range(30):
        print("YES", end="")

if __name__ == "__main__":
    print("INICIO")

    t0 = threading.Thread(target=escribe_x)
    t1 = threading.Thread(target=escribe_y)

    print("Ejecución en HiloA")
    t0.start()

    print("Ejecución en HiloB")
    t1.start()

    print("Ejecución en main")

    t0.join()
    t1.join()


    


