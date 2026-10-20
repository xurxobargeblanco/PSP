import sys
import subprocess

nombre_ficheiro_alias = "aliases.txt"

ficheiro = open(nombre_ficheiro_alias, "r")

alias = { k : v for k,v in list(map( lambda linea : linea.strip("\n").split("="),ficheiro.readLines()))}