import threading
import time
import random

condition = threading.Condition()
libro_disponible = False

def estudiante(id_est):
    global libro_disponible
    with condition:
        while not libro_disponible:
            print(f"[Estudiante {id_est}] Libro no disponible, esperando...")
            condition.wait()  # Espera a que el bibliotecario reponga
        # Una vez despierta, adquiere el libro
        libro_disponible = False
        print(f"[Estudiante {id_est}] ¡He conseguido el libro!")

def bibliotecario():
    global libro_disponible
    for _ in range(3):  # Reponer el libro 3 veces
        time.sleep(random.uniform(1, 2))  # Tiempo para reponer
        with condition:
            libro_disponible = True
            print("[Bibliotecario] Libro repuesto, notificando...")
            condition.notify()  # Despierta a un estudiante notify_all() -> Para despertar todos a vez e compitir

if __name__ == "__main__":
    # Crear hilos de estudiantes
    estudiantes = [threading.Thread(target=estudiante, args=(i,)) for i in range(5)]

    # Crear hilo del bibliotecario
    hilo_bibliotecario = threading.Thread(target=bibliotecario)

    # Iniciar todos los hilos
    for est in estudiantes:
        est.start()
    hilo_bibliotecario.start()

    # Esperar a que todos los hilos terminen
    for est in estudiantes:
        est.join()
    hilo_bibliotecario.join()

    print("Todos los estudiantes han tenido su turno con el libro.")
