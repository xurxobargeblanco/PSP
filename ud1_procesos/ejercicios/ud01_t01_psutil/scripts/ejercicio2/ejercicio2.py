import psutil


# 1. Mostrar todos los servicios:
#     - Para cada servicio se mostrará su nombre, PID asociado, estado y tipo de inicio


def mostrar_todos():
    for s in psutil.win_service_iter():
        info = s.info()
        print(f"{info['name']} | {str(info['pid'])} | {info['status']} | {info['start_type']}")

def mostrar_filtrados():
    filtro_input = input("Filtro (iniciado / parado) :").strip().lower().split()
    if not filtro_input:
        return
    estado_filtro = filtro_input[0]
    inicio_filtro = filtro_input[1] if len(filtro_input) > 1 else None

    for s in psutil.win_service_iter():
        info = s.info()
        cumple_estado = info['status'].lower() == estado_filtro
        cumple_inicio = (info['start_type'].lower() == inicio_filtro) if inicio_filtro else True

        if cumple_estado and cumple_inicio:
            print(f"{info['name']} | {str(info['pid'])} | {info['status']} | {info['start_type']}")





# MENU DEL SISTEMA

def menu():
    """Menú principal del programa."""
    while True:
        print("\n--- MENÚ DE INFORMACIÓN DEL LOS SERVICIOS ---")
        print("1. Mostrar todos los servicios (Iniciado/Parado - Manual/Automático)")
        print("2. Mostrar descripcion de servicio")
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