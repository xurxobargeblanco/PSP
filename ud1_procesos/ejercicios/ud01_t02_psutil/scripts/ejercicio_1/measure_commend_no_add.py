import subprocess
import sys
import time

argumentos = sys.argv[1:]
inicio = time.perf_counter()
resultado = subprocess.run(argumentos,capture_output=True,text=True)
fin = time.perf_counter()

print(f"""
    Ejecutando : {"".join(argumentos)}
    Salida del proceso : 
    {resultado.stdout}
    {resultado.stderr}
    Tarea terminada 

    Tiempo de ejecución : {(fin-inicio):2.2f} segundos
    Codigo de salida {resultado.returncode}
      """)