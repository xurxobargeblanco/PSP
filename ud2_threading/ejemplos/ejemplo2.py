import threading
import time

def procesar_datos(origen, destino, delay=1):
    """Función que simula un procesamiento de datos."""
    print(f"[Hilo] Procesando datos desde {origen} hacia {destino}...")
    time.sleep(delay)
    print("[Hilo] Procesamiento terminado.")

if __name__ == "__main__":
    # args debe ser siempre una tupla (aunque sea de un solo elemento)
    argumentos_posicionales = ("servidor_A", "servidor_B")
    
    # kwargs se pasa como diccionario
    argumentos_con_nombre = {"delay": 2}

    hilo = threading.Thread(
        target=procesar_datos,
        args=argumentos_posicionales,
        kwargs=argumentos_con_nombre,
        name="HiloProcesamiento"
    )

    print("[Principal] Lanzando hilo...")
    hilo.start()

    print("[Principal] Esperando a que termine...")
    hilo.join()

    print("[Principal] Hilo finalizado.")