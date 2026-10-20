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

while acabar != True :
    respuesta = input("")
    if respuesta == 'exit': acabar = True
    
          
