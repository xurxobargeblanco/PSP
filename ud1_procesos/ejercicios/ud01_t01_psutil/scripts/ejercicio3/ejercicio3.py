import psutil;

# Mostrar informacion de un proceso: 

def mostrar_informacion():
    
    [p for p in psutil.process_iter(attrs=['pid','name','username'])]

    for p in procesos:
        pid = p.get('pid', 'N/A')
        nombre = p.get('name') or 'Desconocido'
        usuario = p.get('username') or 'N/A'














# MENU DEL SISTEMA

def menu():
    while True:
        print("\n--- MENÚ DE SERVICIOS ---")
        print("a. Mostrar información de los procesos")
        print("b. Filtrar procesos por uso de memoria")
        print("c. Filtrar procesos por uso de CPU")
        print("d. Mostrar árbol de procesos")
        print("e. Salir")
        
        opcion = input("Selecciona una opción: ").strip().lower()

        match opcion:
            case "a":

            case "b":

            case "c":

            case "d":
                
            case "e":
                print("Saliendo del programa ...")
            case _:
                print("Opción no válida")
