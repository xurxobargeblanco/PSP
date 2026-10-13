import psutil

# 1. Mostrar información de todos los procesos
def mostrar_informacion():
    print(f"\n{'PID':<10} | {'NOMBRE':<30} | {'USUARIO':<20}")
    print("-" * 65)
    
    for p in psutil.process_iter(attrs=['pid', 'name', 'username']):
        info = p.info
        pid = info.get('pid', 'N/A')
        nombre = info.get('name') or 'Desconocido'
        usuario = info.get('username') or 'N/A'
        print(f"{str(pid):<10} | {nombre:<30} | {usuario:<20}")


# 2. Filtrar procesos por uso de memoria 
def filtrar_por_memoria():
    limite = float(input("\nIntroduce el porcentaje mínimo de memoria (%): ").strip())

    procesos = [p for p in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']) if p.info.get('memory_percent') and p.info.get('memory_percent') > limite]
    
    procesos.sort(key=lambda p: p.info.get('memory_percent', 0), reverse=True)

    print(f"\n{'PID':<10} | {'NOMBRE':<30} | {'MEMORIA (%)':<15}")
    print("-" * 60)
    
    for p in procesos:
        mem = p.info.get('memory_percent', 0)
        print(f"{str(p.info.get('pid')):<10} | {str(p.info.get('name')):<30} | {mem:.2f}%")


# 3. Filtrar procesos por uso de CPU 
def filtrar_por_cpu():
    limite = float(input("\nIntroduce el porcentaje mínimo de CPU (%): ").strip())

    procesos = [p for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']) if p.cpu_percent(interval=0.5) > limite]
    
    procesos.sort(key=lambda p: p.cpu_percent(interval=0.1))

    print(f"\n{'PID':<10} | {'NOMBRE':<30} | {'CPU (%)':<15}")
    print("-" * 60)
    
    for p in procesos:
        cpu = p.cpu_percent(interval=0.1)
        print(f"{str(p.info.get('pid')):<10} | {str(p.info.get('name')):<30} | {cpu:.2f}%")


# 4. Mostrar árbol de procesos 
def pintar_arbol(pid, indentacion=""):
    try:
        p = psutil.Process(pid)
        print(f"{indentacion}|____ PID: {pid}, Nombre: {p.name()}")
        
        for hijo in p.children():
            pintar_arbol(hijo.pid, indentacion + "  ")
            
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

def mostrar_arbol_menu():
    pid_usuario = int(input("\nIntroduce el PID del proceso raíz: ").strip())
    
    if psutil.pid_exists(pid_usuario):
        print(f"\n--- ÁRBOL DE PROCESOS DESDE PID {pid_usuario} ---")
        pintar_arbol(pid_usuario, "")
    else:
        print("El PID introducido no existe en el sistema.")


# --- MENÚ DEL SISTEMA ---
def menu():
    while True:
        print("\n--- MENÚ DE PROCESOS ---")
        print("1. Mostrar información de todos los procesos")
        print("2. Filtrar procesos por uso de memoria")
        print("3. Filtrar procesos por uso de CPU")
        print("4. Mostrar árbol de procesos")
        print("5. Salir")
        
        opcion = input("Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            mostrar_informacion()
        elif opcion == "2":
            filtrar_por_memoria()
        elif opcion == "3":
            filtrar_por_cpu()
        elif opcion == "4":
            mostrar_arbol_menu()
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    menu()
