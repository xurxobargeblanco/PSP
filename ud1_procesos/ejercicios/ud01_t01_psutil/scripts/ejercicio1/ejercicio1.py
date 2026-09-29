import psutil
import platform

# 1 Mostrar información del sistema: Deberán mostrarse por pantalla los siguientes datos:

# 1.1 Plataforma sobre la que se ejecuta el script: Windows o Linux

info_plataforma = platform.system

# 1.2 Información de CPUs

def info_cpu():

    # 1.2.1 Numero de CPUs
    cpus_físicas = psutil.cpu_count(logical=False)
    cpus_logicas = psutil.cpu_count(logical=False)

    # 1.2.2 Frecuencia de cada CPU - MHz
    frecuencias = psutil.cpu_freq(percpu=True)
    freq_lis = [f.current for f in frecuencias] if frecuencias else []

    # 1.2.3 % de memoria usado por cada CPU
    uso_por_cpu = psutil.cpu_percent(percpu=True, interval=1)

# 1.3 Información de memoria

    memoria = psutil.virtual_memory()

    def bytes_a_gb(bytes_val):
        return round(bytes_val / (1024 ** 3), 2)
    
    # 1.3.1 Memoria total
    memoria_total_gb = bytes_a_gb(memoria.total)

    # Memoria disponible 
    memoria_disponible_gb = bytes_a_gb(memoria.available)

    # Porcentaje de memoria usada
    Porcentaje_usado = memoria.percent

# 1.4 Informacion de discos

def obtener_info_discos():

    particiones = psutil.disk_partitions()
    lista_particiones = []
    
    # 1.4.1 Listado de particiones

    particiones = psutil.disk_partitions()

    for p in particiones:
        
        info_particion = {
            "dispositivo": p.device,
            "punto_montaje": p.mountpoint,
            "sistema_archivos": p.fstype
        }

    # 1.4.2 Uso de disco para cada unidad o partición

    # 1.4.3 Número de operaciones de lectura

    operaciones_lectura = psutil.disk_io_counters.read_count

    # 1.4.4 Número de operaciones de escritura

    operaciones_escritura = psutil.disk_io_counters.write_count

    # 1.4.5 Número de bytes leídos

    bytes_leidos = psutil.disk_io_counters.read_bytes

    # 1.4.6 Número de bytes escritos

    bytes_escritos = psutil.disk_io_counters.write_count


# 1.5 Estadísticas de red

    net_io = psutil.net_io_counters(pernic=False, nowrap=True)

    # 1.5.1 Bytes enviados
    # 1.5.2 Bytes recibidos
    # 1.5.3 Paquetes enviados
    # 1.5.4 Paquetes recibidos

    if net_io:
        bytes_enviados = net_io.bytes_sent  
        bytes_recibidos = net_io.bytes_recv  
        paquetes_enviados = net_io.packets_sent 
        paquetes_recibidos = net_io.packets_recv

    

# 2 Guardar información del sistema:

def menu():
    """Menú principal del programa."""
    while True:
        print("\n    MENÚ DE INFORMACIÓN DEL SISTEMA    ")
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
            #sys.exit()
        else:
            print("Opción inválida. Inténtalo de nuevo.")

def obtener_informacion_sistema():

    print()

def guardar_informacion():

    print()

def mostrar_informacion():

    print()


if __name__ == "__main__":
    menu()