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