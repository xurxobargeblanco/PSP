import sys
import subprocess

nombre_ficheiro_alias = "aliases.txt"

try:
    with open(nombre_ficheiro_alias, "r") as ficheiro:
        alias = { k : v for k,v in list(map( lambda linea : linea.strip("\n").split("="),ficheiro.readlines()))}
except FileNotFoundError:
    print("No se encuentra el archivo deseado")
    alias = {}

acabar = False

while not acabar:
    linea = input("> ")
    
    if linea.strip():
        partes = linea.split()
        
        if partes[0] == 'exit':
            acabar = True
        else:
            pass           

