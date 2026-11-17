import sys
import time
import datetime
import json
import multiprocessing
import subprocess

def cargar_trabajos(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            trabajos = json.load(f)
    except FileNotFoundError:
        print(f"No existe el fichero '{ruta}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"El fichero no es un JSON valido: {e}")
        sys.exit(1)

    for t in trabajos:
        if not all(clave in t for clave in ("id","comando","intervlo")):
            print(f"Trabajo incompleto (claves) : {t}")
            sys.exit(1)
    return trabajos

def ejecutar_una_vez(id_trabajo, comando):
    print(f"Ejecutando trabajo '{id_trabajo}'")
    try:
        resultado = subprocess.run(comando, capture_output=True,text=True)
    except FileNotFoundError:
        print(f"Error en '{id_trabajo}': el programa {comando[0]!r} no existe.")
        return      
    
    marca = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_log = f"{id_trabajo}_{marca}.log"

    with open(nombre_log, "w", encoding="utf-8") as f:
        f.write(resultado.stdout)
        f.write(resultado.stderr)

    if resultado.returncode == 0:
        print("Trabajo finalizado correctamente.")
    else:
        print(f"Trabajo finalizado con error (código {resultado.returncode}).")

def bucle_trabajo(id_trabajo, comando, intervalo):
    while True:
        ejecutar_una_vez(id_trabajo, comando)
        time.sleep(intervalo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python json_cron.py trabajos.json")
        sys.exit(1)

    print("Cargando trabajos...")
    trabajos = cargar_trabajos(sys.argv[1])
    print(f"\n{len(trabajos)} trabajos cargados.\n")

    procesos = []
    for t in trabajos:
        p = multiprocessing.Process(
            target=bucle_trabajo,
            args=(t["id"], t["comando"], t["intervalo"]),
            daemon=True,
        )
        procesos.append(p)
        p.start()

    try:
        for p in procesos:
            p.join()
    except KeyboardInterrupt:
        print("\nDeteniendo trabajos...")
        for p in procesos:
            p.terminate()