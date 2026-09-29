import os
import sys
import platform
import json
import psutil
from datetime import datetime

# FUNCIONES AUXILIARES

def bytes_a_gb(bytes_val): return round(bytes_val / (1024 ** 3), 2)

# 1. RECOPILACIÓN DE DATOS DEL SISTEMA

def obtener_informacion_sistema():
    
    # 1.1 Plataforma

    info_plataforma = platform.system()  

    # 1.2 Información de CPUs

    frecuencias = psutil.cpu_freq(percpu=True)
    freq_list = [f.current for f in frecuencias] if frecuencias else []
    
    info_cpu = {
        "cpus_fisicas": psutil.cpu_count(logical=False),
        "cpus_logicas": psutil.cpu_count(logical=True),
        "frecuencias_mhz": freq_list,
        "porcentaje_uso": psutil.cpu_percent(percpu=True, interval=1)
    }

    # 1.3 Información de Memoria

    memoria = psutil.virtual_memory()

    info_memoria = {
        "memoria_total_gb": bytes_a_gb(memoria.total),
        "memoria_disponible_gb": bytes_a_gb(memoria.available),
        "porcentaje_usado": memoria.percent
    }

    # 1.4 Información de Discos

    particiones = psutil.disk_partitions()
    lista_particiones = []

    for p in particiones:
        
        uso = psutil.disk_usage(p.mountpoint)
        
        datos_part = {
            "dispositivo": p.device,
            "punto_montaje": p.mountpoint,
            "sistema_archivos": p.fstype,
            "total_gb": bytes_a_gb(uso.total),
            "libre_gb": bytes_a_gb(uso.free),
            "porcentaje_uso": uso.percent
        }
        lista_particiones.append(datos_part)

    disk_io = psutil.disk_io_counters()
    info_discos = {
        "particiones": lista_particiones,
        "operaciones_lectura": disk_io.read_count if disk_io else 0,
        "operaciones_escritura": disk_io.write_count if disk_io else 0,
        "bytes_leidos": disk_io.read_bytes if disk_io else 0,
        "bytes_escritos": disk_io.write_bytes if disk_io else 0
    }

    # 1.5 Estadísticas de Red

    net_io = psutil.net_io_counters()
    info_red = {
        "bytes_enviados": net_io.bytes_sent if net_io else 0,
        "bytes_recibidos": net_io.bytes_recv if net_io else 0,
        "paquetes_enviados": net_io.packets_sent if net_io else 0,
        "paquetes_recibidos": net_io.packets_recv if net_io else 0
    }

    # Diccionario global

    return {
        "plataforma": info_plataforma,
        "cpu": info_cpu,
        "memoria": info_memoria,
        "discos": info_discos,
        "red": info_red
    }

# 2. MOSTRAR INFORMACIÓN POR PANTALLA

def mostrar_informacion(datos):
    """Muestra los datos organizados en la consola."""
    print("\n" + "=" * 50)
    print("        INFORMACIÓN DEL SISTEMA")
    print("=" * 50)
    
    print(f"\n1. Plataforma: {datos['plataforma']}")

    print("\n2. Información de CPUs:")
    print(f"   - CPUs Físicas: {datos['cpu']['cpus_fisicas']}")
    print(f"   - CPUs Lógicas: {datos['cpu']['cpus_logicas']}")
    print(f"   - Frecuencia por CPU (MHz): {datos['cpu']['frecuencias_mhz']}")
    print(f"   - Uso por CPU (%): {datos['cpu']['porcentaje_uso']}")

    print("\n3. Información de Memoria:")
    print(f"   - Memoria Total: {datos['memoria']['memoria_total_gb']} GB")
    print(f"   - Memoria Disponible: {datos['memoria']['memoria_disponible_gb']} GB")
    print(f"   - Porcentaje Usado: {datos['memoria']['porcentaje_usado']}%")

    print("\n4. Información de Discos:")
    print("   Particiones:")
    for p in datos['discos']['particiones']:
        print(f"     * {p['dispositivo']} en '{p['punto_montaje']}' [{p['sistema_archivos']}]")
        print(f"       Total: {p['total_gb']} GB | Libre: {p['libre_gb']} GB | Uso: {p['porcentaje_uso']}%")
            
    print(f"   - Operaciones de lectura: {datos['discos']['operaciones_lectura']}")
    print(f"   - Operaciones de escritura: {datos['discos']['operaciones_escritura']}")
    print(f"   - Bytes leídos: {datos['discos']['bytes_leidos']}")
    print(f"   - Bytes escritos: {datos['discos']['bytes_escritos']}")

    print("\n5. Estadísticas de Red:")
    print(f"   - Bytes enviados: {datos['red']['bytes_enviados']}")
    print(f"   - Bytes recibidos: {datos['red']['bytes_recibidos']}")
    print(f"   - Paquetes enviados: {datos['red']['paquetes_enviados']}")
    print(f"   - Paquetes recibidos: {datos['red']['paquetes_recibidos']}")
    print("=" * 50)

# 3. GUARDAR INFORMACIÓN EN JSON

def guardar_informacion(datos):
    """Guarda el diccionario en un archivo JSON en la ruta indicada por el usuario."""
    ruta = input("\nIntroduce la ruta del directorio donde guardar el archivo JSON: ").strip()

    nombre_fichero = datetime.now().strftime("%Y%m%d%H%M%S") + "-system-info.json"
    ruta_completa = os.path.join(ruta, nombre_fichero)

    with open(ruta_completa, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
    print(f"\n[OK] Información guardada con éxito en:\n{ruta_completa}")

# 4. MENÚ PRINCIPAL

def menu():
    """Menú principal del programa."""
    while True:
        print("\n--- MENÚ DE INFORMACIÓN DEL SISTEMA ---")
        print("1. Mostrar información del sistema")
        print("2. Guardar información del sistema")
        print("3. Salir")
        
        opcion = input("Selecciona una opción (1-3): ").strip()
        
        if opcion == "1":
            print("\nObteniendo datos del sistema...")
            datos = obtener_informacion_sistema()
            mostrar_informacion(datos)
        elif opcion == "2":
            print("\nObteniendo datos del sistema...")
            datos = obtener_informacion_sistema()
            guardar_informacion(datos)
        elif opcion == "3":
            print("Saliendo del programa...")
            sys.exit()
        else:
            print("Opción inválida. Inténtalo de nuevo.")


if __name__ == "__main__":
    menu()