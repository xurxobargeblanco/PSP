
import threading
import time

saldo_actual = 2000

lock = threading.Lock()

def retirar(cantidad, nombre):
    global saldo_actual

    with lock:

        # Leer el saldo
        print(f"{nombre} consulta el saldo: {saldo_actual}€")

        # Simular la operación bancaria
        time.sleep(0.01)

        # Comprobar si hay dinero suficiente
        if saldo_actual >= cantidad:

            # Modificar el saldo
            saldo_actual -= cantidad

            print(f"{nombre} retira {cantidad}€. Saldo: {saldo_actual}€")

        else:
            print(f"{nombre}: Saldo insuficiente")


def persona(nombre, cantidad):
    for i in range(5):
        retirar(cantidad, nombre)


if __name__ == "__main__":

    hilo1 = threading.Thread(target=persona, args=("Persona A", 300))
    hilo2 = threading.Thread(target=persona, args=("Persona B", 100))

    hilo1.start()
    hilo2.start()

    hilo1.join()
    hilo2.join()

    print("Saldo final:", saldo_actual)
