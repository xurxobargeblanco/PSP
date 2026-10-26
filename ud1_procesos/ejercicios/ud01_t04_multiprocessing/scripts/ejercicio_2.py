import multiprocessing
import time
import random

def agregar_elemento(diccionario_compartido,id_proceso):
    time.sleep(random.random())

    time.sleep(random.random())
    
    clave = f"proceso_{id_proceso}"
    valor = random.randint(1, 100)
    
    diccionario_compartido[clave] = valor
    print(f"Proceso {id_proceso} engadiu: {clave} = {valor}")

if __name__ == '__main__':
    
    with multiprocessing.Manager() as manager:

        diccionario = manager.dict()

        procesos = []
        cantidad_procesos = 4

        for i in range(cantidad_procesos):
            p = multiprocessing.Process(target=agregar_elemento,args=(diccionario,i))
            procesos.append(p)
            p.start()
            p.join()

        print(f"Lista : {diccionario}")