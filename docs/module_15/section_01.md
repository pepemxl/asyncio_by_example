# Introducción a estructuras de datos thread safe

Para entender este tema veremos que está por debajo de nuestras herramientas así que haremos un poco de código en C/C++, con lo que buscamos:

- Entender los fundamentos de las estructuras de datos concurrentes
- Implementar operaciones thread safe 
- Analizar y resolver problemas de performance
- Evaluar concurrent vs trade off de performance

Antes de profundizar en el ámbito de los bloqueos(del ingles Locks), es fundamental que comprendamos, cómo  se integrán los bloqueos a estructuras de datos comunes con el fin de lograr la seguridad de los subprocesos(**thread safe**). 

Las preguntas clave aquí son:

- **Cómo agregar bloqueos(Locks) de manera efectiva**: ¿Cuáles son las estrategias para agregar bloqueos a una estructura de datos para garantizar un acceso simultáneo correcto?
- **Consideraciones de rendimiento**: ¿Cómo se pueden aplicar los bloqueos de una manera que mantenga la velocidad y permita el acceso simultáneo de varios subprocesos?
- ¿Cuál es la función de una variable de condición?
- ¿Cómo una variable de condición difiere de una variable común?
- ¿Qué es un semaforo?
- ¿Cómo reemplazamos locks y variables de condición con semafaros?
- ¿Qué es un semaforo binario y como trabaja?


## Estructura de datos para un contador

Empecemos con el caso del la estructura de datos **El Contador**.

Creando un Contador no concurrente de la manera más simnple sería algo parecido al siguiente código ejemplo:

```cpp
typedef struct __counter_t {
    int value;
} counter_t;

void init(counter_t *c) {
    c->value = 0;
}

void increment(counter_t *c) {
    c->value++;
}

void decrement(counter_t *c) {
    c->value--;
}

int get(counter_t *c) {
    return c->value;
}
```

donde tenemos la estructura de datos `counter_t` que será nuestro almacen de datos y 4 metodos que nos ayudarán respectivamente a 

- inicializar la estructura
- incrementar el valor del contador
- decrementar el valor del contador
- obtener el valor del contador

lo primero a notar es que:

- Este contador es fácil de implementar, pero carece de seguridad para subprocesos.
- Este contador tiene problemas de escalabilidad, es decir no cuenta con sincronización, por lo cual este contador no es adecuado para entornos concurrentes.

## Hagamos el contador thread safe

Primero hagamos que este contador sea thread safe, para ello agregaremos un Bloqueo (Lock).

### Donde se agrega el bloqueo?

Para hacer el contador thread-safe vamos a agregar un lock cada vez que cualquier metodo intente manipular(incrementar/decrementar) la información de la estructura de datos y lo liberaremos al retornar desde la llamada.


Ejemplo de lock


```cpp
// Pseudo código para el contador thread-safe 
lock_t lock;

void increment(counter_t *c) {
    lock(&lock);
    c->value++;
    unlock(&lock);
}

void decrement(counter_t *c) {
    lock(&lock);
    c->value--;
    unlock(&lock);
}

```

## Patrón de Diseños


The output of code in `01_example.cpp`
 would be 

 ```bash
Incremented: 1
Incremented: 2
Incremented: 3
Incremented: 4
Incremented: 5
Decremented: 4
Decremented: 3
Decremented: 2
Final value in thread: 2
Incremented: 3
Incremented: 4
Incremented: 5
Incremented: 6
Incremented: 7
Decremented: 6
Decremented: 5
Decremented: 4
Final value in thread: 4
Final value in main: 4

 ```

## Explicación:

La estructura `counter_t` y sus funciones asociadas:

- `init`, 
- `increment`, 
- `decrement`, 
- `get`

están definidas para manejar un contador seguro para subprocesos.

`threadFunction` es una función que será ejecutada por cada subproceso, demostrando las operaciones de incremento y decremento en el contador compartido.

La función principal inicializa el contador, crea dos subprocesos (cada uno de los cuales ejecuta `threadFunction`) y luego espera a que estos subprocesos se completen. Finalmente, imprime el valor final del contador.

Las instrucciones `printf` dentro de las funciones increment, decrement y `threadFunction` proporcionan una salida para realizar un seguimiento de los cambios en el valor del contador.


En resumen el contador ahora es seguro para subprocesos, sin embargo

- Cuello de botella de un solo bloqueo: un solo bloqueo puede no ser suficiente para las necesidades de alto rendimiento. Es posible que se requieran más optimizaciones, que serán el foco del resto del capítulo.
- Suficiencia para las necesidades básicas: si el rendimiento no es un problema crítico, un simple bloqueo puede ser suficiente y no es necesaria ninguna complejidad adicional.



## Como evaluar un contador sincronizado

### Configuración de la prueba de rendimiento

Para evaluar la eficiencia de la implementación básica del contador sincronizado, realizamos una prueba en la que cada subproceso actualiza un contador compartido una cantidad fija de veces. El impacto en el rendimiento se mide variando la cantidad de subprocesos involucrados en la actualización.

### Parámetros de la prueba

- Actividad de la prueba: cada subproceso actualiza el contador un millón de veces.
- Objetivo: determinar cómo el tiempo total empleado se ve afectado por la cantidad de subprocesos.
- Observaciones de la prueba
    - Escalabilidad deficiente
        - Resultados de la prueba: el gráfico ilustra que el rendimiento del contador sincronizado se degrada significativamente con más subprocesos.
        - Tiempo empleado: mientras que un solo subproceso completa un millón de actualizaciones en aproximadamente 0,03 segundos, las actualizaciones simultáneas de varios subprocesos generan demoras considerables, que alcanzan casi los 5 segundos.
        - Empeoramiento con más subprocesos: la demora aumenta a medida que se agregan más subprocesos, lo que indica una escalabilidad deficiente.
-   Escenario ideal: escalamiento perfecto
    - Definición: el escalamiento perfecto se logra cuando el tiempo que tardan los subprocesos en completar tareas en varios procesadores es tan rápido como en un solo procesador, a pesar del aumento de la carga de trabajo.
    - Objetivo: modificar el contador sincronizado para que presente un escalamiento perfecto, donde el trabajo realizado en paralelo no aumente significativamente el tiempo total.


## La necesidad de contadores escalables

El desafío de desarrollar contadores escalables se ha vuelto cada vez más relevante con la llegada de los procesadores multinúcleo. La investigación sobre el rendimiento del sistema operativo ha demostrado que sin contadores escalables, muchas cargas de trabajo de Linux enfrentan problemas de escalabilidad significativos en plataformas multinúcleo.

### El enfoque del contador de aproximación

Una solución eficaz para este problema es el contador de aproximación, que utiliza una combinación de contadores locales y globales.

### Estructura del contador de aproximación

- **Contador lógico**: el contador lógico está representado por un contador global y varios contadores locales, uno para cada núcleo de CPU.

Ejemplo: en un sistema de cuatro CPU, habría cuatro contadores locales y un contador global.

- **Mecanismo de bloqueo**: cada contador local se sincroniza con su propio bloqueo local y se utiliza un bloqueo global para el contador global.

### Funcionamiento del contador de aproximación

- Incremento del contador: cuando un subproceso desea incrementar el contador, actualiza su contador local correspondiente, lo que es eficiente debido a la contención reducida entre las CPU.
- Actualización de local a global: periódicamente, el valor de un contador local se transfiere al contador global mediante la adquisición del bloqueo global. Este proceso implica incrementar el contador global en función del valor del contador local y luego restablecer el contador local a cero.
- Umbral `S`: la frecuencia de las actualizaciones de local a global está determinada por un umbral `S`. Un `S` más pequeño hace que el contador se comporte más como un contador no escalable, mientras que un `S` más grande mejora la escalabilidad a expensas de la precisión en el recuento global.

### Obtención de un valor preciso

- Precisión del valor global: para obtener un recuento exacto, se podrían adquirir todos los bloqueos locales y el bloqueo global. Sin embargo, este enfoque no es escalable debido a la sobrecarga que supone adquirir varios bloqueos.

El contador de aproximación representa un equilibrio entre la escalabilidad y la precisión del recuento global. Al permitir actualizaciones simultáneas de los contadores locales y la sincronización periódica con el contador global, este método mejora significativamente la escalabilidad en sistemas multinúcleo, aunque puede introducir un retraso en la precisión del recuento global.

Veamos un ejemplo para demostrarlo:

| Time | L1 | L2 | L3 | L4 | G |
| ---- | --- | ---- | --- | --- | ---|
|0|0|0|0|0|0|
|1|0|0|1|1|0|
|2|1|0|2|1|0|
|3|2|0|3|1|0|
|4|3|0|3|2|0|
|5|4|1|3|3|0|
|6|5->0|1|3|4|5 (de L1)|
|7|0|2|4|5->0|10 (de L4)|


El umbral `S` se establece en 5 en este ejemplo, y los subprocesos en cada una de las cuatro CPU están actualizando sus conteos locales L1 ... L4. A medida que el tiempo disminuye, el valor del contador global (G) también se indica en el seguimiento. Un contador local se puede incrementar en cada paso de tiempo, si el valor local alcanza el umbral S, se transfiere al contador global y el contador local se reinicia.

El rendimiento de los contadores de aproximación con un umbral `S` de 1024 muestra que el rendimiento es excelente. Actualizar el contador cuatro millones de veces en cuatro procesadores lleva aproximadamente la misma cantidad de tiempo que actualizarlo un millón de veces en una CPU.

El valor del umbral `S`, con cuatro subprocesos en cuatro CPU, cada uno incrementando el contador un millón de veces. Cuando `S` es bajo, el rendimiento es terrible (aunque el conteo global siempre es preciso). Cuando S es alto, el rendimiento es excelente, pero el recuento global se retrasa (como máximo, en la cantidad de CPU multiplicada por S). Los contadores aproximados permiten este equilibrio entre precisión y rendimiento.


## Operaciones concurrentes en una Linked List

En la programación concurrente, modificar estructuras de datos comunes como listas enlazadas para admitir operaciones seguras para subprocesos puede ser complicado. Nos centraremos en la implementación concurrente de la operación de inserción en una lista enlazada, dejando otras operaciones como la búsqueda y la eliminación para una exploración más profunda.

### La operación de inserción básica

#### Implementación inicial

- **Mecanismo de bloqueo**: en el método de inserción concurrente básico, se adquiere un bloqueo al principio y se libera al salir. Esto garantiza que la operación de inserción sea segura para subprocesos.
- **Manejo de fallas de malloc()**: si malloc() falla (algo poco frecuente), es crucial liberar el bloqueo antes de que falle la operación de inserción. Este requisito introduce complejidad y potencial de errores.

#### Desafío con flujo de control excepcional

- Propenso a errores: el manejo de flujo de control excepcional, como liberar el bloqueo en caso de falla de malloc(), puede ser propenso a errores. Los estudios han demostrado que esas rutas de código raramente utilizadas son una fuente común de errores.

### Optimización del método de inserción

#### Reestructuración para lograr eficiencia

- Región crítica: la clave es reestructurar el código de modo que el bloqueo solo se mantenga alrededor de la región crítica de la operación de inserción. Esto hace que la implementación sea más robusta.
- Malloc() seguro para subprocesos: suponiendo que malloc() es seguro para subprocesos, se puede llamar sin un bloqueo, lo que reduce la duración durante la cual se mantiene el bloqueo.

Ejemplo de código de 02_example demuestra estos cambios, centrándose en el bloqueo solo cuando se modifica la lista compartida.

Al ingresar el método de inserción simplemente se obtiene un bloqueo y se libera cuando sale. Sin embargo, si malloc() falla (lo cual es una ocurrencia rara), el código también debe liberar el bloqueo antes de que falle la inserción. En este caso, el código también debe fallar la inserción.

### Mejora de la rutina de búsqueda

#### Simplificación del código

- Ruta de salida única: la función de búsqueda se puede modificar para que tenga una única ruta de salida, lo que simplifica el flujo de control.
- Puntos de bloqueo reducidos: este cambio reduce la cantidad de veces que se adquiere y libera el bloqueo, lo que disminuye la probabilidad de errores como olvidar desbloquear antes de regresar.

El desafío en la programación concurrente para estructuras de datos como listas enlazadas radica en mantener la precisión y la eficiencia en medio de modificaciones concurrentes. Al estructurar cuidadosamente el código y minimizar las regiones bloqueadas, podemos lograr una implementación más eficiente y resistente a errores.



## Escalado de listas enlazadas e implementación de colas concurrentes

### Bloqueo de mano sobre mano en listas enlazadas

El desafío de la escalabilidad: 
- **Lista concurrente básica**: si bien una lista enlazada concurrente básica con un solo bloqueo para toda la lista es simple, no se escala bien con múltiples subprocesos.
- Enfoque de bloqueo de mano sobre mano: este enfoque implica agregar un bloqueo a cada nodo de la lista. A medida que uno recorre la lista, adquiere el bloqueo del siguiente nodo antes de liberar el actual, de ahí el término "mano sobre mano".
    - Pros y contras: conceptualmente, el bloqueo de mano sobre mano aumenta el paralelismo en las operaciones de lista. Sin embargo, en la práctica, la sobrecarga de bloquear cada nodo puede ser prohibitiva, lo que a menudo lo hace menos eficiente que un solo bloqueo, especialmente para listas extensas y numerosos subprocesos.

### Posibles alternativas

- Enfoques híbridos: investigar un método híbrido, donde se adquiere un bloqueo para cada pocos nodos, podría ser una solución más práctica. 
- Colas concurrentes: el enfoque de Michael y Scott

### Estructura de cola de dos bloqueos

- Implementación: a diferencia del método más simple de usar un solo bloqueo prominente, el diseño de Michael y Scott para una cola concurrente implica dos bloqueos separados: uno para la cabeza y otro para la cola.
- Mejora de la concurrencia: esta estructura permite que las operaciones de encolado utilicen principalmente el bloqueo de cola y las operaciones de desencolado utilicen el bloqueo de cabeza, lo que permite la ejecución concurrente de estas funciones.

### Técnica del nodo ficticio

- Propósito: un nodo ficticio, asignado durante la inicialización de la cola, separa las operaciones de cabeza y cola, lo que mejora aún más la concurrencia.

### Comprensión de la cola

- Interacción con el código: para comprender completamente cómo funciona la cola concurrente de Michael y Scott, es beneficioso leer, escribir y ejecutar el código usted mismo. Medir su rendimiento puede proporcionar información valiosa.

### Aplicación de colas en sistemas multiproceso

- Frecuencia de uso: las colas son comunes en aplicaciones multiproceso, pero a menudo requieren más que solo bloqueos para satisfacer las demandas de dichos sistemas.


### Usando Colas

- Inicialización de la cola: la función Queue_Init inicializa una cola vacía con un nodo ficticio.
- Operaciones de puesta en cola y desconexión de la cola: Queue_Enqueue agrega un elemento en la cola y Queue_Dequeue elimina un elemento de la cabecera de la cola. Ambas operaciones están protegidas por bloqueos separados (head_lock y tail_lock), lo que mejora la concurrencia.
- Funciones de subproceso: EnqueueThread y DequeueThread se utilizan para demostrar la puesta en cola y la desconexión de la cola simultáneas.
- Función principal: inicializa la cola, crea dos subprocesos (uno para poner en cola y otro para desconexión de la cola) y espera a que completen sus operaciones.


### Tabla hash concurrente

La tabla hash es una estructura de datos versátil y ampliamente utilizada, y concluimos nuestro análisis de las estructuras de datos concurrentes centrándonos en una tabla hash simple y no redimensionable.

Estructura y rendimiento

- Implementación: La tabla hash concurrente se construye utilizando las listas concurrentes que hemos analizado anteriormente.
- Mecanismo de bloqueo: Cada contenedor hash, representado por una lista, tiene su propio bloqueo. Esto difiere del uso de un único bloqueo para toda la tabla.
- Ventajas: Al asignar un bloqueo por contenedor hash, la tabla hash permite que se produzcan múltiples operaciones simultáneamente, lo que mejora significativamente su rendimiento.
ex3

Optimización prematura: una advertencia
Evitar la optimización excesiva: en la búsqueda del rendimiento, tenga cuidado con la optimización prematura. Concéntrese en realizar mejoras que realmente contribuyan a la eficacia general del programa, en lugar de optimizar aspectos que tienen poco impacto en el rendimiento más amplio.





- Entender las limitaciones de los locks y por que necesitamos primitivas adicionales
- Simularemos Productores/Consumidores an un único buffer.
- Por qué y como aplicar Lampson y Redells.


## Mecanismos de espera eficientes en aplicaciones concurrentes


### Las limitaciones de los bloqueos y la necesidad de primitivas adicionales

Mientras que los locks son cruciales para el manejo de accesos a los recursos compartidos, no son suficiente para todos los escenarios de control de concurrencia.

Es muy común que los threads necesitan esperar por una condición especifica para continuar con la ejecución.


#### Sincronización de hilos Parent-child


Tratemos de reparar el siguiente código para obtener la salida esperada:
```cpp
void *child(void *arg) {
    printf("child\n");
    // Indicate completion needed
    return NULL;
}

int main(int argc, char *argv[]) {
    printf("parent: begin\n");
    pthread_t c;
    Pthread_create(&c, NULL, child, NULL); // create child
    // Wait for child needed
    printf("parent: end\n");
    return 0;
}
```

Salida esperada:


```bash
parent: begin
child
parent: end
```


## Aprendiendo Bloqueos(Locks)

- Entender la utilidad de los Locks
- Implementar lock, fecth y add
- Evaluar locks en un código simple
- Entender la instrucción compare-and-swap
- Tecnicas avanzadas de locks
    - Llamadas Solaris con mecanismo de cola.

Programación concurrente va de la mano con operaciones atomicas.


**Definición**. Un **Lock** es una herramienta para asegurar que operaciones criticas corren de manera atomica. Los locks operan como gatekeepers, permitiendo que un solo hilo a lavez pueda ejecutar el código protegido por el lock.

Por ejemplo consideremos la actualización de una variable:

```cpp
lock_t mutex; // Glocal Lock
// seccion cque debe ser bloqueada
lock(&mutex);
critical_value = critical_value + 1;
unlock(&mutex);
```

### Posix Mutex y hardware que soporta Locks


En la librería de threads POSIX los locks se conocen como **mutex**, que es un acronimo para **mutual exclusion**. Los mutex evitan que distintos threads accedan a la misma memoria compartida.


```cpp
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER; // Inicialicion de Mutex

Pthread_mutex_lock(&lock);   // Try mutex or exit
critical_value = critical_value + 1;       // Seccion protegida
Pthread_mutex_unlock(&lock); // Libreamos el lock
```


## Bloqueo Granular


Cuando queremos proteger distintas partes del código podemos obtar por definir distintos mutex. Lo cual es más eficaz y reduce los cuellos de botella.


## Soporte desde el Hardware y desde el OS

- Hay hardware que facilita el uso de locks a nivel de hardware!
- Usualmente el OS ayuda al control de los locks.

## Qué debemos cuidar al diseñar un lock?

- Asegurar la exclusión mutua.
- Dar la misma oportunidad a cada thread.
- Evitat starvation
- Performance:
    - Overhead de unthread que adquiere y libera el lock
    - Single CPU con multiples threads
    - Multiple CPU con multiples threads


## Controlar las interrupciones

Un metodo efectivo en un solo CPU es activar y desactivar interrupciones en partes criticas.


## Usar Locks a nivel de CPU 


Lock usando una bandera:

```cpp
typedef struct __lock_t { int flag; } lock_t;

void init(lock_t *mutex) {
    // 0 -> lock is available, 1 -> held
    mutex->flag = 0;
}

void lock(lock_t *mutex) {
    while (mutex->flag == 1) // TEST the flag
        ; // spin-wait (do nothing)
    mutex->flag = 1; // now SET it!
}

void unlock(lock_t *mutex) {
    mutex->flag = 0;
}

```

La mecánica del bloqueo es como sigue:

- Inicialización: El bloqueo se inicializa con el indicador a 0, lo que indica que está disponible.
- Adquisición del bloqueo: La función de bloqueo comprueba si el indicador es 1 (bloqueo mantenido por otro hilo). De lo contrario, lo establece a 1, lo que indica que el bloqueo ya está adquirido.
- Liberación del bloqueo: La función de desbloqueo restablece el indicador a 0, lo que permite que el bloqueo vuelva a estar disponible.

Las limitaciones del bloqueo basado en banderas:

- Problema de corrección: 
    - Posibilidad de condiciones de carrera: Existe una ventana crítica entre la comprobación `while (mutex->flag == 1)` y el establecimiento `mutex->flag = 1;` donde otro hilo podría adquirir el bloqueo, lo que provocaría que varios hilos entraran en la sección crítica simultáneamente.
- Problema de rendimiento
    - Espera de turno: Los hilos que esperan el bloqueo entran en un bucle de espera de turno, comprobando continuamente la bandera. Esto puede ser ineficiente, especialmente si el bloqueo se mantiene durante un período prolongado, ya que consume ciclos de CPU sin realizar ningún trabajo útil.



## Contruir un lock de turnos con TestAndSet

Nuevo hardware!!!

Debido a las limitaciones de la desactivación de interrupciones en sistemas multiprocesador y a la insuficiencia de las cargas y almacenamientos básicos, los diseñadores de sistemas comenzaron a incorporar soporte de hardware para mecanismos de bloqueo. Este soporte, presente en los primeros sistemas multiprocesador y ahora estándar en todos los sistemas, es crucial para construir bloqueos eficaces.

La instrucción TestAndSet es una pieza fundamental del soporte de hardware para el bloqueo:

```c
int TestAndSet(int *old_ptr, int new) {
    int old = *old_ptr; // Obtenemos el valor
    *old_ptr = new;     // Guardamos un nuevo valor en old_ptr
    return old;         // Refresamos el valor habia en old_ptr
}
```
Esta instrucción atómica prueba y actualiza simultáneamente un valor. Es esencial para crear un bloqueo de turno básico.

- Adquisición de bloqueo
    - Escenario inicial: Si un hilo llama a `lock()` y ningún otro hilo mantiene el bloqueo, `TestAndSet(flag, 1)` devolverá `0` (el valor anterior) y el hilo adquiere el bloqueo, estableciendo el flag en 1.
    - Bloqueo mantenido por otro hilo: Si otro hilo ya mantiene el bloqueo (el flag es 1), `TestAndSet(flag, 1)` devolverá `1`, lo que provocará que el hilo entre en un bucle de espera hasta que se libere el bloqueo.
- Garantía de exclusión mutua
    - Atomicidad: La naturaleza atómica de la operación de TestAndSet garantiza que solo un hilo pueda adquirir el bloqueo a la vez, lo que proporciona exclusión mutua.
- Desbloqueo
    - Liberación del bloqueo: El hilo que desbloquea restablece el flag a 0, lo que permite que otros hilos adquieran el bloqueo.
- Evaluación de bloqueos por turno
    - Efectividad
        - Exclusión mutua: El bloqueo por turnos permite que solo un hilo a la vez entre en la sección crítica, logrando así su objetivo fundamental. 
    - Equidad
        - Posibilidad de starvation: Los bloqueos por turno no garantizan la equidad. Un hilo podría tener el turno(girar/spin) indefinidamente, lo que podría provocar problemas de starvation.
- Rendimiento
    - Escenario con una sola CPU: En una sola CPU, si el hilo que mantiene el bloqueo es interrumpido, otros hilos desperdiciarán ciclos de CPU en el bucle de espera de un turno.
    - Escenario con varias CPU: Los bloqueos por turno son más eficientes cuando el número de hilos es aproximadamente igual al número de CPU. Los hilos en CPU independientes pueden realizar la espera turno de forma eficaz, adquiriendo rápidamente el bloqueo una vez disponible.


```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class SpinLock {
private:
    std::atomic<bool> flag;

public:
    SpinLock() : flag(false) {}

    void lock() {
        bool expected = false;
        while (!flag.compare_exchange_strong(expected, true)) {
            expected = false;
        }
    }

    void unlock() {
        flag.store(false);
    }
};

void criticalSection(int threadID, SpinLock &spinLock) {
    std::cout << "Thread " << threadID << " intentar adquirir el lock..." << std::endl;
    spinLock.lock();
    std::cout << "Thread " << threadID << " lock adquirido" << std::endl;
    std::cout << "Thread " << threadID << " seccion critica" << std::endl;
    spinLock.unlock();
    std::cout << "Thread " << threadID << " lock liberado" << std::endl;
}

int main() {
    const int numThreads = 5;
    SpinLock spinLock;
    std::vector<std::thread> threads;

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(criticalSection, i, std::ref(spinLock));
    }

    for (auto &thread : threads) {
        thread.join();
    }

    return 0;
}
```

Para compilar 
`g++ -o spinlock_example -std=c++11 spinlock_example.cpp -pthread
`
y para correr el programa `./spinlock_example`

Salida

```bash
Thread 0 intentar adquirir el lock...
Thread Thread 0 lock adquirido.
Thread 0 seccion critica.
Thread 0 lock liberado.
Thread 2 intentar adquirir el lock...
Thread 2 lock adquirido.
Thread 2 seccion critica.
Thread 2 lock liberado.
1 intentar adquirir el lock...
Thread 1 lock adquirido.
Thread 1 seccion critica.
Thread 1 lock liberado.
Thread 3 intentar adquirir el lock...
Thread 3 lock adquirido.
Thread 3 seccion critica.
Thread 3 lock liberado.
Thread 4 intentar adquirir el lock...
Thread 4 lock adquirido.
Thread 4 seccion critica.
Thread 4 lock liberado.
```

Aqui la clase SpinLock imita un bloqueo por turnos(spin) simple mediante una bandera booleana atómica. El método lock "gira" hasta que logra cambiar la bandera de falso a verdadero, y unlock la restablece a falso.
Mientras que la función simula el intento de un hilo de entrar en una sección crítica, adquiriendo y liberando el bloqueo por turnos(spin).
Donde la función principal crea varios hilos, cada uno intentando entrar en la sección crítica.


En el programa de ejemplo usamos std:atomic, para simular TestAndSet sin embargo este tipo de operaciones realmente se hacen a nivel de hardware.

Los bloqueos de spin son efectivos en ciertos escenarios (como duraciones de bloqueos cortos y de baja contención), pero pueden ser ineficientes si se usan en exceso o se aplican incorrectamente, ya que utilizan ciclos de CPU mientras esperan.

El comportamiento de los subprocesos y los bloqueos puede depender en gran medida del scheduler del sistema y de la cantidad de CPU disponibles.


## Compara e intercambia

Comparar e Intercambiar (CAS), conocido como Comparar e Intercambiar en arquitecturas x86, es una primitiva de hardware que ofrecen algunos sistemas para facilitar la programación concurrente.

Funcionalidad de CAS en pseudocódigo de C
El funcionamiento básico de CAS se puede comprender mediante el siguiente pseudocódigo de C:

```c
int CompareAndSwap(int *ptr, int expected, int new) {
    int original = *ptr;
    if (original == expected)
        *ptr = new;
    return original;
}
```

### Principio fundamental de CAS

- Actualización condicional: CAS comprueba si el valor en la dirección especificada por `ptr` es igual al esperado. Si es así, actualiza automáticamente `ptr` con `new`. Si no, deja `ptr` sin cambios.
- Valor de retorno: En ambos casos, CAS devuelve el valor original en `ptr`, lo que permite que el código de llamada determine si la actualización se realizó correctamente.

La implementación seria algo como lo siguiente:

```c
void lock(lock_t *lock) {
    while (CompareAndSwap(&lock->flag, 0, 1) == 1)
        ; // Spin-wait
}
```

La adquisición de bloqueo es a traves de la función de bloqueo que intenta continuamente intercambiar un 1 en bloqueo->bandera si su valor actual es 0. Si la bandera ya es 1 (bloqueo mantenido), el hilo entra en un bucle de espera de turno(spin).

#### Ventajas de CAS

- Versatilidad: CAS es más flexible que el método de prueba y configuración, lo que abre la posibilidad de técnicas de sincronización más avanzadas, como la sincronización sin bloqueos.
- Comportamiento de bloqueo de turno(spin) simple: Cuando se utiliza para bloqueos de spin simples, CAS se comporta de forma similar al bloqueo de spin, esperando(girando) hasta que el bloqueo esté disponible.

```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class CASLock {
private:
    std::atomic<int> flag;

public:
    CASLock() : flag(0) {}

    void lock() {
        int expected = 0;
        while (!flag.compare_exchange_strong(expected, 1)) {
            expected = 0; // Reset expected as it gets modified by compare_exchange_strong
        }
    }

    void unlock() {
        flag.store(0);
    }
};

void criticalSection(int threadID, CASLock &casLock) {
    std::cout << "Thread " << threadID << " attempting to acquire lock..." << std::endl;
    casLock.lock();
    std::cout << "Thread " << threadID << " has acquired lock." << std::endl;
    std::cout << "Thread " << threadID << " is in critical section." << std::endl;
    casLock.unlock();
    std::cout << "Thread " << threadID << " has released lock." << std::endl;
}

int main() {
    const int numThreads = 5;
    CASLock casLock;
    std::vector<std::thread> threads;

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(criticalSection, i, std::ref(casLock));
    }

    for (auto &thread : threads) {
        thread.join();
    }

    return 0;
}
```

Salida

```bash
Thread 0 attempting to acquire lock...
Thread 0 has acquired lock.
Thread 0 is in critical section.
Thread 0 has released lock.
Thread 1 attempting to acquire lock...
Thread 1 has acquired lock.
Thread 1 is in critical section.
Thread 1 has released lock.
Thread 2 attempting to acquire lock...
Thread 2 has acquired lock.
Thread 2 is in critical section.
Thread 2 has released lock.
Thread 3 attempting to acquire lock...
Thread 3 has acquired lock.
Thread 3 is in critical section.
Thread 3 has released lock.
Thread 4 attempting to acquire lock...
Thread 4 has acquired lock.
Thread 4 is in critical section.
Thread 4 has released lock.
```

## Load-Linked y Store-Conditional

Load-Linked (LL) y Store-Conditional (SC) son pares de instrucciones que se utilizan en plataformas como MIPS, ARM y PowerPC para crear bloqueos y otras estructuras concurrentes. Estas instrucciones trabajan juntas para habilitar operaciones atómicas cruciales para la sincronización de hilos.

### Funcionalidad en pseudocódigo de C

- Carga enlazada (LL): Esta instrucción carga un valor desde una ubicación de memoria a un registro. Prepara el almacenamiento condicional posterior.
- Almacenamiento condicional (SC): Esta instrucción intenta almacenar un valor en la ubicación de memoria si no se han realizado actualizaciones desde la última operación de carga enlazada. Devuelve 0 en caso de error, manteniendo el valor sin cambios.

```c
void lock(lock_t *lock) {
    while (LoadLinked(&lock->flag) || 
           !StoreConditional(&lock->flag, 1))
        ; // Spin-wait
}
```

### Mecánica del bloqueo

- Esperando la disponibilidad del bloqueo: El hilo comprueba si lock->flag es 0, lo que indica que el bloqueo no se mantiene.
- Adquiriendo el bloqueo: El hilo intenta establecer el flag en 1 mediante SC. Si el SC tiene éxito, se adquiere el bloqueo.
- Manejo de fallos de SC: Si el SC falla (otro hilo adquirió el bloqueo primero), el bucle continúa y el hilo lo intenta de nuevo.

Este enfoque funciona por que:
- Atomicidad: La combinación de LL y SC garantiza la atomicidad. Cuando dos hilos intentan adquirir el bloqueo simultáneamente después de una operación LL, solo uno tendrá éxito con el SC. El SC del otro hilo fallará, obligándolo a reintentarlo.


#### Forma compacta

- Cortocircuito de condicionales booleanos: Se puede implementar una forma más compacta de la función de bloqueo, acortando el código pero con funcionalidades equivalentes.


Las instrucciones de carga vinculada y almacenamiento condicional proporcionan una forma eficaz de implementar bloqueos en programación concurrente al garantizar operaciones atómicas. Su uso combinado garantiza que solo un hilo pueda adquirir el bloqueo a la vez, lo que evita las condiciones de carrera y permite una sincronización adecuada.

Implementar instrucciones de carga vinculada (LL) y almacenamiento condicional (SC) en C++ para un mecanismo de bloqueo es algo abstracto, ya que se trata de instrucciones a nivel de hardware específicas de ciertas arquitecturas como MIPS, ARM y PowerPC. En C++ estándar, en arquitecturas x86 típicas, no tenemos acceso directo a las instrucciones LL/SC. Sin embargo, podemos imitar su comportamiento utilizando las operaciones atómicas proporcionadas por la biblioteca estándar de C++ para demostrar un concepto similar.

```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class LLSCLock {
private:
    std::atomic<int> flag;

public:
    LLSCLock() : flag(0) {}

    void lock() {
        while (true) {
            int expected = 0;
            // Load-Linked equivalent: load the value
            if (flag.load(std::memory_order_relaxed) == expected) {
                // Store-Conditional equivalent: attempt to store a new value
                if (flag.compare_exchange_strong(expected, 1)) {
                    break; // Break if SC succeeds
                }
            }
        }
    }

    void unlock() {
        flag.store(0, std::memory_order_relaxed);
    }
};

void criticalSection(int threadID, LLSCLock &llscLock) {
    std::cout << "Thread " << threadID << " attempting to acquire lock..." << std::endl;
    llscLock.lock();
    std::cout << "Thread " << threadID << " has acquired lock." << std::endl;
    std::cout << "Thread " << threadID << " is in critical section." << std::endl;
    llscLock.unlock();
    std::cout << "Thread " << threadID << " has released lock." << std::endl;
}

int main() {
    const int numThreads = 5;
    LLSCLock llscLock;
    std::vector<std::thread> threads;

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(criticalSection, i, std::ref(llscLock));
    }

    for (auto &thread : threads) {
        thread.join();
    }

    return 0;
}
```

Salida

```bash
Thread 0 attempting to acquire lock...
Thread Thread 0 has acquired lock.
Thread 0 is in critical section.
Thread 0 has released lock.
1 attempting to acquire lock...
Thread 1 has acquired lock.
Thread 1 is in critical section.
Thread 1 has released lock.
Thread 2 attempting to acquire lock...
Thread 2 has acquired lock.
Thread 2 is in critical section.
Thread 2 has released lock.
Thread 3 attempting to acquire lock...
Thread 3 has acquired lock.
Thread 3 is in critical section.
Thread 3 has released lock.
Thread 4 attempting to acquire lock...
Thread 4 has acquired lock.
Thread 4 is in critical section.
Thread 4 has released lock.
```


- Clase LLSCLock: Simula un bloqueo mediante operaciones atómicas para imitar el comportamiento de LL y SC.
- Función de bloqueo: Intenta continuamente establecer el indicador en 1 (adquirir el bloqueo) solo si actualmente es 0, imitando el patrón LL/SC.
- Función de sección crítica: Muestra cómo los hilos intentan entrar y salir de una sección crítica adquiriendo y liberando el bloqueo.
- Función principal: Crea varios hilos, cada uno de los cuales ejecuta la función de sección crítica.


En el ejemplo utilizamos `std::atomic` para simular LL y SC, pero en el uso real en sistemas que admiten estas instrucciones, se utilizarían directamente para operaciones atómicas de bajo nivel en implementaciones de bloqueo.


## La instrucción "FecthAndAdd" y la implementación del bloqueo de tickets

La instrucción "FetchAndAdd" es una herramienta en la programación concurrente que incrementa automáticamente un valor en una dirección específica y devuelve el valor anterior.


```c
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}
```

Mellor-Crummey y Scott utilizaron la instrucción de FetchAndAdd para desarrollar un sistema de bloqueo de tickets, que utiliza una combinación de variables de ticket y turno.

### Adquisición de Bloqueo

- Asignación de Ticket: Un hilo adquiere un ticket mediante una operación atómica de búsqueda y adición en el contador de tickets. Este número de ticket (myturn) representa la posición del hilo en la cola.
- Condición de Entrada: Un hilo entra en la sección crítica cuando su número de ticket coincide con el turno actual (myturn == turn).

### Mecanismo de Desbloqueo

- Incremento de Turno: Para liberar el bloqueo, el hilo simplemente incrementa la variable turn, permitiendo que el siguiente hilo en la cola entre en la sección crítica.
- Ventajas del Bloqueo de Ticket
    - Progreso Garantizado: Este método garantiza que todos los hilos progresen. A cada hilo se le asigna un ticket y entran en la sección crítica en el orden de sus tickets.
    - Equidad: A diferencia de los métodos anteriores, donde un hilo podía girar indefinidamente, el bloqueo de ticket garantiza que cada hilo finalmente tendrá su turno para entrar en la sección crítica.

Evaluación del Método de Bloqueo de Ticket: El enfoque de bloqueo de ticket aborda los problemas de equidad y de starvation(inanición) observados en implementaciones de bloqueo más simples, como los bloqueos de spin. Al asignar tickets y gestionar turnos, se garantiza un acceso más ordenado y justo a la sección crítica, evitando que los hilos queden bloqueados perpetuamente.

```cpp
#include <iostream>
#include <atomic>
#include <thread>
#include <vector>

class TicketLock {
private:
    std::atomic<int> ticketCounter;
    std::atomic<int> turn;

public:
    TicketLock() : ticketCounter(0), turn(0) {}

    void lock() {
        int myTicket = ticketCounter.fetch_add(1); // Fetch-And-Add
        while (turn.load(std::memory_order_relaxed) != myTicket) {
            ; // Spin-wait
        }
    }

    void unlock() {
        turn.fetch_add(1); // Move to next ticket
    }
};

void criticalSection(int threadID, TicketLock &ticketLock) {
    std::cout << "Thread " << threadID << " attempting to acquire lock..." << std::endl;
    ticketLock.lock();
    std::cout << "Thread " << threadID << " has acquired lock." << std::endl;
    std::cout << "Thread " << threadID << " is in critical section." << std::endl;
    ticketLock.unlock();
    std::cout << "Thread " << threadID << " has released lock." << std::endl;
}

int main() {
    const int numThreads = 5;
    TicketLock ticketLock;
    std::vector<std::thread> threads;

    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(criticalSection, i, std::ref(ticketLock));
    }

    for (auto &thread : threads) {
        thread.join();
    }

    return 0;
}
```

Salida

```bash
Thread 0 attempting to acquire lock...
Thread 2 attempting to acquire lock...
Thread 2 has acquired lock.
Thread 2 is in critical section.
Thread 2 has released lock.
Thread 1 attempting to acquire lock...
Thread 0 has acquired lock.
Thread 0 is in critical section.
Thread 0Thread  has released lock.
Thread 3 attempting to acquire lock...
Thread 4 attempting to acquire lock...
1 has acquired lock.
Thread 1 is in critical section.
Thread 1 has released lock.
Thread 3 has acquired lock.
Thread 3 is in critical section.
Thread 3 has released lock.
Thread 4 has acquired lock.
Thread 4 is in critical section.
Thread 4 has released lock.
```


- Clase TicketLock: Implementa un bloqueo de ticket mediante operaciones atómicas. El método lock usa fetch_add para incrementar automáticamente ticketCounter y obtener un número de ticket. Gira hasta que llega su turno. El método unlock incrementa el turno para permitir que el siguiente titular de ticket adquiera el bloqueo.
- Función de Sección Crítica: Representa el intento de un hilo de entrar en la sección crítica, adquiriendo y liberando el bloqueo de ticket.
- Función Principal: Crea varios hilos para demostrar el mecanismo de bloqueo de ticket.


### Escenario: Rotación en un solo procesador

- Caso práctico: Imagine dos hilos en un solo procesador. El hilo 0 mantiene un bloqueo, pero se interrumpe. El hilo 1 intenta adquirir el bloqueo, lo encuentra ocupado y comienza a rotar.
- Ineficiencia de la rotación: El hilo 1 desperdicia toda su porción de tiempo rotando, comprobando un valor que no cambiará hasta que el hilo 0 reanude y libere el bloqueo.
- Empeoramiento con más hilos: Con más hilos compitiendo por el bloqueo, la ineficiencia se intensifica, ya que N-1 hilos podrían desperdiciar sus porciones de tiempo simplemente rotando.

#### Ceder el paso(**Yield**) para evitar el desperdicio de ciclos de CPU

- Idea básica: En lugar de girar, un hilo podría ceder el paso de CPU a otro. Esto se realiza mediante una llamada al sistema `yield()`, donde el hilo que cede el paso se desprograma, cambiando su estado de en ejecución a listo.
- Efectividad en un escenario de doble hilo: En un escenario de dos hilos en una CPU, esta estrategia basada en el rendimiento funciona bien. Si un hilo no puede adquirir un bloqueo, cede el paso, lo que permite que el hilo que lo mantiene se ejecute y, potencialmente, lo libere.

#### Desafíos con múltiples subprocesos

- Ejemplo de scheduler round-robin: En un sistema con muchos subprocesos compitiendo por un bloqueo, ceder el bloqueo puede provocar frecuentes cambios de contexto. Si un subproceso adquiere el bloqueo y es interrumpido, los demás subprocesos encontrarán secuencialmente el bloqueo, cederán el bloqueo y entrarán en un ciclo de ejecución y cederán.
- Costo del cambio de contexto: Si bien ceder el bloqueo es más eficiente que girar el bloqueo, aún implica costosos cambios de contexto.
- Starvation(Inanición) no abordada: Ceder el bloqueo no resuelve el problema de la Starvation. Un subproceso podría atascarse en un bucle de ceder el bloqueo mientras otros adquieren y liberan el bloqueo repetidamente.


## Usando Colas

Dormir en lugar de Spin

Nuestros métodos anteriores presentaban fallas porque dejaban demasiado al azar. Por lo tanto, si el scheduler elige el hilo equivocado, debe esperar el bloqueo o ceder la CPU inmediatamente. 

Los métodos tradicionales de gestión de hilos y adquisición de bloqueos a menudo han generado ineficiencias e starvation(inanición). Para superar estos problemas, es esencial controlar qué hilo recibe un bloqueo después de que el holder del lock actual lo libere, lo que requiere un mejor soporte del sistema operativo y un mecanismo específico para el seguimiento de los hilos en espera.

Un ejemplo práctico se observa en Solaris, donde se utilizan las funciones `park()` y `unpark(threadID)`.


Implementación en Solaris:

En Solaris, se emplean dos funciones clave, `park()` y `unpark(threadID)`. Estas funciones son fundamentales para gestionar los hilos que intentan adquirir un bloqueo:

- Mecanismo de suspensión y activación: Un hilo se pone en suspensión si intenta adquirir un bloqueo que ya está mantenido y se despierta una vez que se libera el bloqueo. 
- Eficiencia y prevención de inanición: Este enfoque fusiona el método tradicional de prueba y configuración con una cola para adquirentes de bloqueos en espera, lo que mejora la eficiencia de los bloqueos y minimiza la inanición de los mismos.

Guardia y bloqueo giratorio:

La guardia(guard) actúa como un bloqueo spin, protegiendo las operaciones en la bandera y la cola.

- Espera giratoria temporal: En caso de interrupción de un hilo mientras gestiona un bloqueo, otros hilos realizan una espera giratoria, pero este periodo se limita a unas pocas instrucciones, lo que la convierte en una solución viable.

Gestión de colas y manejo de banderas:

Cuando un hilo no puede adquirir un bloqueo, sigue un proceso específico:

- Se añade a la cola mediante la función gettid().
- Libera la guardia y cede la CPU.
- La bandera no se restablece al iniciar un nuevo hilo, lo cual no es un error, sino una característica necesaria para una transferencia de bloqueo fluida.

Abordaje de condiciones de carrera:

Un desafío importante es la condición de carrera que se produce justo antes de la llamada de estacionamiento. Solaris introduce `setpark()` para mitigar este problema:

- Señalización preventiva: Un hilo indica su intención de estacionar, lo que garantiza que si se llama a unpark antes de aparcar, el hilo no se suspenda innecesariamente.
- Cambio mínimo en el código: La implementación dentro de la función lock() es sencilla, ya que implica la adición de setpark() antes de liberar la protección.


```c
queue_add(m->q, gettid());
 setpark(); // new code
 m->guard = 0;
```

Protección a nivel de núcleo: Una solución alternativa es colocar la protección directamente dentro del núcleo, lo que permite operaciones atómicas en la liberación de bloqueos y la desencola de subprocesos, mejorando así la eficiencia general del proceso.


## Soporte por OS

Diferentes sistemas operativos ofrecen un diferente soporte.

### Sistema Futex de Linux:

Linux incorpora una característica similar a la de Solaris, pero con capacidades mejoradas en el núcleo:

- Memoria física y cola: Cada futex en Linux tiene una ubicación de memoria física dedicada y una cola en el núcleo.
- Funciones de suspensión y activación: El sistema proporciona dos llamadas futex principales:
    - futex wait(address, expected): Pone el hilo que realiza la llamada en suspensión a menos que se cumpla la condición, en cuyo caso la llamada finaliza.
    - futex wake(address): Despierta un hilo de la cola.

Implementación de código en el mutex de Linux:

Un ejemplo de estas llamadas futex se puede encontrar en el mutex de Linux, como se ilustra en el código de lowlevellock.h en la biblioteca nptl. 

Complejidades del código Lowlevellock.h:

Estado del bloqueo y seguimiento de los bloqueos en espera: 

El código utiliza un único entero para monitorizar tanto el estado del bloqueo (indicado por el bit alto) como el número de bloqueos en espera (representado por los demás bits). Un valor negativo significa que el bloqueo se mantiene.

Optimización para escenarios comunes: Este fragmento muestra la optimización para el caso habitual en el que un único hilo adquiere y libera un bloqueo, utilizando la prueba y configuración de bits atómicos para el bloqueo y la adición atómica para el desbloqueo.

Comprensión del bloqueo en el mundo real de Linux:

Experimentar con este mecanismo de bloqueo práctico puede mejorar significativamente la comprensión de los sistemas de bloqueo de Linux. Dominar esta área equivale a comprender aplicaciones reales más allá del conocimiento teórico.

Técnicas modernas de construcción de bloqueos:

Los bloqueos contemporáneos combinan compatibilidad con hardware (como instrucciones avanzadas) con compatibilidad con sistemas operativos (como park() y unpark() en Solaris o futex en Linux). Los detalles de estas implementaciones varían, y la codificación para dichos bloqueos suele estar meticulosamente optimizada. 

Recursos de aprendizaje adicionales:

Para quienes buscan una comprensión más profunda, se recomienda examinar el código base de Solaris o Linux. Además, estudios como el de David et al., que analiza las técnicas de bloqueo en los multiprocesadores actuales, ofrecen valiosas perspectivas sobre el tema.



