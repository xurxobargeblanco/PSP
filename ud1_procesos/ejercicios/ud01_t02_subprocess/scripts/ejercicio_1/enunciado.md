1. measure_command.py: medir el tiempo de ejecución de un proceso

    Cuando ejecutamos un programa desde una consola podemos observar cuánto tarda en finalizar, pero queremos crear una pequeña utilidad que permita medir automáticamente el tiempo empleado por otro programa.

    Por ejemplo, queremos poder ejecutar:

    python measure_command.py python tarea.py

    Y obtener información sobre cuánto tiempo ha tardado tarea.py.

    - Requisitos del programa

        El programa deberá:

        Recibir mediante la línea de comandos el programa que se quiere ejecutar.
        Recibir también los argumentos destinados a ese programa.
        Lanzar el proceso.
        Esperar a que termine.
        Medir el tiempo transcurrido.
        Mostrar la salida estándar producida por el proceso.
        Mostrar su código de salida.

        No es necesario implementar

        Ejecución de varios programas.
        Ejecución en segundo plano.
        Tuberías entre programas.
        Redirecciones.
        Interpretación de comandos de un shell.