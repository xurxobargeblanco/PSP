import multiprocessing

def enviar_texto(conexion):
    texto = "Ola Mundo, ejercicio multiproces"
    conexion.send(texto)
    conexion.close()

def recibir_texto(conexion):
    texto = conexion.recv()
    texto = texto.upper()

    print(f"Texto recibido : {texto}")
    conexion.close()

if __name__ == "__main__":
    extremo1, extremo2 = multiprocessing.Pipe()

    proceso1 = multiprocessing.Process(
        target=enviar_texto,
        args=(extremo1,)
    )

    proceso2 = multiprocessing.Process(
        target=recibir_texto,
        args=(extremo2,)
    )

    proceso1.start()
    proceso2.start()

    proceso1.join()
    proceso2.join()