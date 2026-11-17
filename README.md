# Cuaderno de aula del módulo de PSP

# PSP · Tema 1: Procesos

Resumo teórico do tema: que é un proceso, como se xestiona o seu ciclo de vida e como se comunican e sincronizan.

## Índice

1. [Conceptos básicos](#1-conceptos-básicos)
2. [Árbore de procesos](#2-árbore-de-procesos)
3. [Operacións básicas](#3-operacións-básicas)
4. [Estados dun proceso](#4-estados-dun-proceso)
5. [Comunicación e sincronización](#5-comunicación-e-sincronización)
6. [Mecanismos de exclusión mutua](#6-mecanismos-de-exclusión-mutua)
7. [Táboa comparativa](#7-táboa-comparativa)

---

## 1. Conceptos básicos

- **Programa**: arquivo no disco (estático).
- **Proceso**: programa **en execución**, con memoria, estado e PID propios. Un programa pode orixinar varios procesos.
- **Sistema operativo (SO)**: controla os procesos cargados en memoria, asigna a CPU a cada un e xestiona a súa comunicación e sincronización.
- **PID** (*Process Identifier*): identificador **único** de cada proceso; é como o SO se refire a el.

## 2. Árbore de procesos

- O SO é quen **executa** a creación de procesos, pero un proceso novo créase **sempre por petición doutro proceso** (o pai).
- Cada proceso depende de quen o creou: **pai → fillo**. Os fillos poden crear á súa vez máis fillos, formando a **árbore de procesos**.
- Ao arrancar o ordenador cárgase o kernel e créase o **proceso inicial**; de el descende todo o resto.

```
Proceso inicial
  └── Escritorio
        └── Word        (fillo do escritorio, pai da impresión)
              └── Impresión
```

## 3. Operacións básicas

| Operación | Descrición |
|---|---|
| `create` | Crear un proceso (creador = pai, creado = fillo) |
| `wait` | O pai espera a que o fillo remate |
| `exit` | O proceso avisa ao SO de que remata (pode informar ao pai) |

- Pai e fillo execútanse **concorrentemente**: comparten a CPU segundo a **política de planificación** do SO.
- Cada proceso ten a súa **imaxe de memoria** independente: o que un cambie **non o ve o outro**.
- **Windows** → `createProcess()`: crea un proceso a partir dun programa distinto.
- **UNIX/Linux** → `fork()`: o fillo é un duplicado do espazo de direccións do pai e continúa desde a mesma posición. Despois son independentes.
- **Memoria compartida**: rexión á que acceden varios procesos. O SO só a crea e establece permisos; os procesos definen o formato dos datos.
- **Terminación en cascada**: se o pai termina, nalgúns SO os fillos tamén. O pai tamén pode terminar un fillo (exceso de recursos, xa non é necesario...).

## 4. Estados dun proceso

```
Creado ──► Listo ◄────────────────┐
             │  ▲                 │ Fin E/S
   é o seu   │  │ fin de turno    │
   turno     ▼  │ ou abandono     │
          Execución ───────► Bloqueado
             │       espera suceso / E/S
             ▼ FIN
         Terminado
```

| Estado | Significado |
|---|---|
| **Creado** | O proceso acaba de nacer |
| **Listo** | Pode usar a CPU, agarda a que o planificador llela dea |
| **Execución** | Posúe a CPU |
| **Bloqueado** | Agarda un suceso (E/S, fin doutra tarefa, espera voluntaria) |
| **Terminado** | Rematou |

| Transición | Causa |
|---|---|
| Creado → Listo | Ao crearse |
| Listo → Execución | O **planificador (*scheduler*)** asigna a CPU |
| Execución → Listo | Fin da franxa de tempo ou abandono voluntario |
| Execución → Bloqueado | Espera un suceso |
| Bloqueado → Listo | Ocorre o suceso esperado (Fin E/S) |
| Execución → Terminado | Remata |

> Un proceso **bloqueado nunca pasa directamente a Execución**: primeiro vai a **Listo**.

- **Planificador (*scheduler*)**: parte do SO que decide que proceso usa a CPU. Un reparto xusto e habitual é por **franxas de tempo**: ao esgotarse, o proceso é desaloxado e pasa a Listo.
- **Cambio de contexto**: acto de cambiar un proceso de estado.
- **BCP** (*Bloque de Control de Proceso* ou *Descriptor de Proceso*): estrutura de datos coa información de control de cada proceso. O SO garda a colección de BCP nunha **cola estática, cola dinámica ou táboa (array)**.

## 5. Comunicación e sincronización

Os procesos que cooperan necesitan:

- **Comunicación**: intercambiar información.
- **Sincronización**: evitar accesos simultáneos descontrolados a datos comúns.

### Rexión crítica e exclusión mutua

- **Rexión crítica**: parte do programa que accede a un recurso compartido e require exclusión mutua.
- **Exclusión mutua**: se un proceso accede ao recurso compartido, os demais non poden ata que o libere.
- **Condición de carreira**: varios procesos modifican datos compartidos á vez e o resultado depende de como se alternen.

**Exemplo produtor–consumidor** (variable compartida `contador`, valor inicial 3):

| Proceso | Instrución | Valor |
|---|---|---|
| Produtor | le `contador` | 3 |
| Consumidor | le `contador` | 3 |
| Consumidor | escribe `contador - 1` | 2 |
| Produtor | escribe `contador + 1` | **4** |

Un elemento consumido perdeuse no contador.

### 6 condicións dunha boa solución

1. Dous procesos non poden estar á vez na mesma rexión crítica.
2. Non se fan suposicións sobre o hardware.
3. Non se fan suposicións sobre as velocidades relativas dos procesos.
4. Ningún proceso fóra da súa rexión crítica pode bloquear a outros.
5. Ningún proceso debe esperar eternamente para entrar.
6. Non se pospón indefinidamente a decisión de quen entra.

## 6. Mecanismos de exclusión mutua

### 6.1 Inhibición de interrupcións

- Antes da rexión crítica `DISABLE` (inhibir interrupcións); ao saír `ENABLE`. A rexión convértese nunha operación **atómica**.
- ✅ Simple.
- ❌ A rexión debe ser curta; bloquea tamén procesos que non compiten e o resto do sistema; é perigoso dar este control ao usuario.

### 6.2 Cerrollos (espera activa)

- Variable booleana que indica se a rexión está libre ou ocupada.
- ❌ Consultar o cerrollo e poñelo a ocupado **non é atómico**: dous procesos poden entrar á vez.
- Solucións por software: **Lamport** (panadaría), **Dekker** (2 procesos), **Dijkstra** (n procesos), **Knuth, Eisenberg e McGuire**, **Peterson**.
- Solución con hardware: instrución **TAS** (*Test And Set Lock*), que consulta e asigna nun só paso ininterrumpible.
- ❌ Consume CPU (**espera activa**).

### 6.3 Semáforos (Dijkstra, 1965)

- **Evitan a espera activa**: o proceso que espera queda bloqueado, sen consumir CPU.
- Impleméntanse cun contador e unha lista de procesos bloqueados.

| Operación | Efecto |
|---|---|
| `Init(n)` | Inicializa co número de procesos que poden entrar á vez |
| `Wait` (Bajar) | Se valor > 0, resta 1 e continúa; se vale 0, **bloquea** |
| `Signal` (Subir) | Suma 1 (e esperta un proceso bloqueado) |

```
Semáforo.Init(1)
P0: Wait()  → rexión crítica → Signal()
P1: Wait()  → rexión crítica → Signal()
```

- ✅ Sinxelos e sen espera activa.
- ❌ O programador debe seguir o protocolo; son de baixo nivel.

### 6.4 Monitores

- Módulo con **procedementos e datos**; os datos só son accesibles polos procedementos do monitor.
- **Só un proceso pode estar activo á vez dentro do monitor**; os demais esperan.
- É unha construción da linguaxe: a exclusión mutua implementa o **compilador**.
- ✅ Máis seguro (menos erros do programador).
- ❌ Dispoñible en poucas linguaxes.

### 6.5 Paso de mensaxes

- Necesario en **sistemas distribuídos** (cada procesador con memoria propia): non hai variables compartidas, polo que semáforos e monitores non serven.
- Permite que dous procesos se comuniquen **sen variables compartidas**.
- Primitivas: **Send** (enviar a un destino) e **Receive** (recibir de unha orixe; pode bloquear se non hai mensaxe).
- Son **chamadas ao sistema**, non construcións da linguaxe.

## 7. Táboa comparativa

| Mecanismo | Espera activa | Responsable | Vantaxe | Inconveniente |
|---|---|---|---|---|
| Inhibición de interrupcións | Non | Programador/SO | Simple | Perigoso, bloquea todo |
| Cerrollos | **Si** | Programador | Idea sinxela | Non atómico, consome CPU |
| Semáforos | No | Programador | Sen espera activa | Baixo nivel |
| Monitores | Non | **Compilador** | Máis seguro | Poucas linguaxes |
| Paso de mensaxes | Non | SO | Serve en sistemas distribuídos | — |