
import subprocess

print("=" * 40)
print("COMPROBACIÓN DEL REPOSITORIO")
print("=" * 40)

resultado = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

if resultado.returncode != 0:
    print("Error: non te atopas nun repositorio Git.")
    print(resultado.stderr)
    exit()

estado = resultado.stdout.strip()

resultado = subprocess.run(
    ["git", "log", "-1", "--oneline"],
    capture_output=True,
    text=True
)

if resultado.returncode != 0:
    print("Error ao obter o último commit.")
    print(resultado.stderr)
    exit()

ultimo_commit = resultado.stdout.strip()

resultado = subprocess.run(
    ["git", "fetch", "origin", "main"],
    capture_output=True,
    text=True
)

if resultado.returncode != 0:
    print("Error ao actualizar o repositorio remoto.")
    print(resultado.stderr)
    exit()

print("\nEstado del repositorio:\n")

if estado == "":
    print("Repositorio limpio.")
else:
    print("Hay cambios pendientes.")
    print("\nArchivos afectados:")

    for linea in estado.splitlines():
        print(" ", linea[3:])

print("\nÚltimo commit:\n")
print(ultimo_commit)

print("\nActualización del repositorio remoto:\n")
print("Fetch realizado correctamente.")

print("\n" + "=" * 40)
print("RESUMEN")
print("=" * 40)

if estado == "":
    print("\nEl repositorio no tiene cambios pendientes.")
else:
    print("\nEl repositorio tiene cambios pendientes.")

print("La información del repositorio remoto se ha actualizado.")

        

