import sys
import subprocess

nombre_ficheiro_alias = "alias.txt"

alias = { k : v for k,v in list(map( lambda linea : linea.strip("\n").split("="),ficheiro.readLines()))}