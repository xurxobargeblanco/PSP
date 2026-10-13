import subprocess
import sys
import time

argumentos = sys.argv[1:]

if not argumentos:
    print("Uso: python3 measure_command.py <programa> [argumentos...]")
    sys.exit(1)

inicio = time.perf_counter()

resultado = subprocess.run(
    argumentos,
    capture_output=True,
    text=True
)

fin = time.perf_counter()

print(f"Ejecutando: {' '.join(argumentos)}")
print("Salida del proceso:")
print(resultado.stdout, end="")

if resultado.stderr:
    print(resultado.stderr, end="")

print(f"\nTiempo de ejecución: {fin - inicio:.2f} segundos")
print(f"Código de salida: {resultado.returncode}")

