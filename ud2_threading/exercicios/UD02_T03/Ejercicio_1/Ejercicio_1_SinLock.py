
import threading
import time

saldo_actual = 2000

def retirar(cantidad, nombre):
    global saldo_actual

    # Leer el saldo
    saldo_leido = saldo_actual
    print(f"{nombre} consulta el saldo: {saldo_leido}€")

    # Simular el tiempo de operación
    time.sleep(0.01)

    # Modificar el saldo
    if saldo_leido >= cantidad:

        saldo_actual = saldo_leido - cantidad
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

