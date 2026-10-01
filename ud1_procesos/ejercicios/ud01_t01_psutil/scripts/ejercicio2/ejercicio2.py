import psutil


# 1. Mostrar todos los servicios:
#     - Para cada servicio se mostrará su nombre, PID asociado, estado y tipo de inicio

def obtener_servicios():
    lista_servicios = []

    



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