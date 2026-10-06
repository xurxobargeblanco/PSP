import psutil


# 1. Mostrar todos los servicios:
#     - Para cada servicio se mostrará su nombre, PID asociado, estado y tipo de inicio

def mostrar_todos():
    for s in psutil.win_service_iter():
        info = s.info()
        print(f"{info['name']} | {str(info['pid'])} | {info['status']} | {info['start_type']}")

# 2. Mostrar servicios filtrados:
#    - El filtro será una cadena de texto formada por una o dos palabras separadas por un espacio. La primera de ellas hará referencia al estado del servicio: iniciado o   
#    parado; y la segunda al tipo de inicio: manual o automático

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

# 3. Mostrar descripción de un servicio:
#    - Se proporcionará el nombre del servicio y mostrará la descripción del mismo


def mostrar_descripcion():
    nombre = input("Nombre exacto del servicio: ").strip()
    servicio = psutil.win_service_get(nombre)
    info = servicio.as_dict()
    print(f"Servicio : {info['name']}")
    print(f"Descripcion: {info['descripcion']}")



# MENU DEL SISTEMA

def menu():
    while True:
        print("\n--- MENÚ DE SERVICIOS ---")
        print("a. Mostrar todos los servicios")
        print("b. Mostrar servicios filtrados")
        print("c. Mostrar descripción de un servicio")
        print("d. Salir")
        
        opcion = input("Selecciona una opción: ").strip().lower()
        if opcion == "a":
            mostrar_todos()
        elif opcion == "b":
            mostrar_filtrados()
        elif opcion == "c":
            mostrar_descripcion()
        elif opcion == "d":
            break


if __name__ == "__main__":
    menu()