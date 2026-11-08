import sys
import subprocess

def executar_comprobar(resultado, titulo):
    if resultado.returncode != 0:
        print("Non se pudo completar a opracion git.")
        return False
    print(titulo)

    if resultado.stdout.strip() == "":
        print("repositorio limpio (sen cambios pendientes). \n")
    else:
        print(resultado.stdout)
    return True


resultado1 = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True
)

if executar_comprobar(resultado1, "Estado do repositorio:"):
    
    resultado2 = subprocess.run(
        ["git", "log", "-1", "--oneline"],
        capture_output=True,
        text=True
    )
    
    if executar_comprobar(resultado2, "Último commit:"):
        
        resultado3 = subprocess.run(
            ["git", "fetch", "origin", "main"],
            capture_output=True,
            text=True
        )
        
        executar_comprobar(resultado3, "Actualización do repositorio remoto:")


