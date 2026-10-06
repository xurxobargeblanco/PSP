# 3. Elabora un programa en Python que recopile información de los procesos del sistema. El programa deberá mostrar el siguiente menú:
1. Mostrar información de todos los procesos:
    - Se mostrará por defecto PID, nombre y usuario.
2. Filtrar procesos por uso de memoria:
    - Se preguntará al usuario un porcentaje de uso de memoria y sólo se mostrarán los procesos que tengan un valor mayor. Los procesos se mostrarán de mayor a menor uso de memoria.
3. Filtrar procesos por uso de memoria:
    - Se preguntará al usuario un porcentaje de uso de CPU (se realizará un sondeo con intervalo de 0.5) y solo se mostrarán los procesos que tengan un valor mayor. Los procesos se mostrarán de menor a mayor uso de CPU.
4. Mostrar árbol de procesos
    - Se preguntará al usuario por un PID, se debe comprobar que el proceso existe, y a continuación se mostrará de manera recursiva el árbol de procesos. De estos procesos solo se mostrará PID y nombre. Gráficamente se representarán los hijos de un proceso imprimiendo estos con dos espacios de indentado respecto a su padre.
