2. mini_shell.py: un pequeño intérprete de comandos con alias

    Queremos construir una pequeña utilidad que permita ejecutar programas desde una consola propia.
    Además, queremos poder definir alias para aquellos comandos que utilizamos habitualmente.
    Los alias se almacenarán en un fichero de texto:
    aliases.txt

    Por ejemplo:
    py=python
    ip=ipconfig
    ping=ping -c1

    Nuestro programa deberá leer estos alias al iniciarse y, posteriormente, permitir introducir comandos.
    - Requisitos del programa

        El mini-shell deberá:

        Leer los alias al comenzar.
        Mostrar un indicador de entrada.
        Leer comandos introducidos por el usuario.
        Separar el nombre del comando de sus argumentos.
        Comprobar si el comando es un alias.
        Sustituirlo por el comando correspondiente cuando sea necesario.
        Ejecutar el proceso.
        Mostrar su salida estándar.
        Mostrar los errores producidos por el proceso.
        Continuar aceptando comandos hasta que el usuario introduzca:
        exit

        El mini-shell no deberá implementar:
        
        tuberías (|);
        redirecciones (>, >>);
        operadores && o ||;
        ejecución en segundo plano;
        comillas para agrupar argumentos;
        alias encadenados;
        comandos internos propios del shell.
        Los comandos se ejecutarán directamente mediante subprocess; no se utilizará shell=True.

