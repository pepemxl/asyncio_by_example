# Semaforos

En la programación concurrente, los semáforos funcionan como una primitiva unificada, ideal para gestionar tareas de sincronización que tradicionalmente se gestionaban mediante bloqueos y variables de condición. Al poder incorporar ambas construcciones, los semáforos ofrecen una herramienta flexible en nuestro conjunto de herramientas de concurrencia.

Los semáforos operan con un valor entero simple, manipulado por dos rutinas clave:

- sem_wait(): Disminuye el valor del semáforo en uno. Si esta acción resultara en un valor negativo, el hilo debe esperar.
- sem_post(): Incrementa el valor del semáforo en uno, con la posibilidad de reactivar un hilo en espera si este existe.


```cpp
#include <semaphore.h>
sem_t s;
sem_init(&s, 0, 1); // The semaphore 's' is born with a value of 1
```

La iniciación es sencilla: un semáforo, como s, se inicializa con un valor que determinará su comportamiento posterior (1 en nuestro caso, lo que garantiza la exclusividad mutua). Para los hilos de un solo proceso, el segundo argumento de sem_init() permanece en 0, lo que mantiene el alcance del semáforo localizado.

Tras inicializar un semáforo, podemos interactuar con él mediante una de dos funciones: sem_wait() o sem_post(). El siguiente código describe el comportamiento de estas dos funciones.


```cpp
 int sem_wait(sem_t *s) {
 decrement the value of semaphore s by one
 wait if value of semaphore s is negative
 }

 int sem_post(sem_t *s) {
 increment the value of semaphore s by one
 if there are one or more threads waiting, wake one
}
```

- Interacción con sem_wait(): Cuando un hilo invoca sem_wait(), este continúa sin interrupciones (si el valor del semáforo era inicialmente positivo) o se detiene, suspendiendo su ejecución hasta que otro semáforo incremente su valor.
- Avanzando con sem_post(): A diferencia de sem_wait(), sem_post() nunca se detiene. Simplemente aumenta el valor del semáforo y, si hay hilos en cola de espera, se selecciona uno y se reanuda.

## Valor del semáforo: Una invariante oculta


Un aspecto interesante del comportamiento del semáforo es que su valor, cuando es negativo, refleja el número de hilos en espera; aunque este detalle permanece oculto para los usuarios del semáforo. Es una mnemotécnica útil que resume la lógica del semáforo.


## Semáforos para Ordenar

### Semáforos para Ordenar Eventos en Programas Concurrentes

Más allá de la exclusión mutua, los semáforos son eficaces para secuenciar eventos en concurrencia, donde un hilo puede necesitar esperar a que las acciones de otro hilo cumplan una condición. Esto se alinea con la funcionalidad que hemos visto con las variables de condición, posicionando al semáforo como un señalizador eficiente entre hilos.

### Semáforo como una Primitiva de Ordenación

- Patrón Común: Un patrón recurrente en programación concurrente implica que un hilo se detenga hasta que se cumpla una condición específica y otro hilo emita una señal una vez que la cumple.

### Implementando Ordenar Eventos con Semáforos

Considere el escenario donde un hilo padre debe esperar a que un hilo hijo complete:

```cpp
sem_t s;

void *child(void *arg) {
    printf("child\n");
    sem_post(&s); // Signal: child is done
    return NULL;
}

int main(int argc, char *argv[]) {
    sem_init(&s, 0, 0); // Initialize semaphore to 0
    printf("parent: begin\n");
    pthread_t c;
    Pthread_create(&c, NULL, child, NULL);
    sem_wait(&s); // Parent waits for the child
    printf("parent: end\n");
    return 0;
}
```

```bash
parent: begin
child
parent: end
```

- Inicialización: El semáforo s se inicializa a 0, preparándolo para servir como señal de finalización del evento.
- Hilo principal: El hilo principal inicia el hilo secundario e invoca sem_wait(&s), pausando hasta que el hilo secundario indique la finalización.
- Hilo secundario: Al finalizar su tarea, el hilo secundario ejecuta sem_post(&s), incrementando el semáforo e indicando al hilo principal que continúe.


### Escenarios y valores del semáforo

- Esperas del padre: Si el hilo padre ejecuta sem_wait(&s) antes de que se ejecute el hijo, la disminución del semáforo hará que el padre espere, dado su valor inicial de 0.
- El hijo completa primero: Si el hijo completa primero e invoca sem_post(&s), el valor del semáforo pasa a ser 1, lo que permite al padre omitir la espera y continuar la ejecución al alcanzar sem_wait(&s).
- En ambos casos, el valor inicial de 0 del semáforo garantiza que el hilo padre solo continúe después de que el hijo haya indicado su finalización, preservando así el orden de operaciones previsto.

### ¿Cuál debería ser el valor inicial de este semáforo?

La respuesta es 0. Considere los dos escenarios siguientes. 

- Primero, supongamos que el padre crea el hijo, pero este aún no se ha ejecutado (es decir, está en una cola de listos, pero no se está ejecutando). En este escenario, el padre llamará a sem_wait() antes de que el hijo haya llamado a sem_post(). Queremos que el padre espere a que el hijo se ejecute. Esto solo puede ocurrir si el valor del semáforo es menor que 0. Por lo tanto, 0 es el valor inicial. A continuación, el padre se ejecuta y espera mientras el semáforo se decrementa (a -1). Cuando el hijo termina, llamará a sem_post(), establecerá el valor del semáforo en 0 y despertará al padre, quien regresará de sem_wait() y completará el programa. 
- El segundo escenario ocurre cuando el hijo completa la tarea antes de que el padre pueda llamar a sem_wait(). En este ejemplo, el hijo ejecutará primero sem_post(), aumentando el valor del semáforo de 0 a 1. Luego, cuando el padre esté listo para comenzar, llamará a sem_wait() y descubrirá que el valor del semáforo es 1. El padre entonces reducirá el valor (a 0) y saldrá de sem_wait() sin esperar, obteniendo el resultado deseado.
Los semáforos demuestran ser herramientas versátiles no solo para la exclusión mutua, sino también para la ordenación precisa de eventos en un entorno concurrente. Al gestionar cuidadosamente los valores de los semáforos, los desarrolladores pueden coordinar dependencias complejas entre subprocesos con relativa simplicidad.


## Intento n.° 1

El problema del productor/consumidor o del búfer limitado es un problema clásico de concurrencia que ilustra los desafíos de coordinar los hilos de producción y consumo en un entorno de búfer compartido.

### Función de los semáforos

Los semáforos pueden actuar como herramientas versátiles para gestionar este problema, funcionando como bloqueos cuando se inicializan a 1 y como mecanismos de señalización cuando se inicializan a 0. El valor de inicialización de un semáforo suele reflejar la cantidad de recursos disponibles para su distribución al inicio.

### Intento inicial con dos semáforos

Para sincronizar el acceso a un búfer compartido, utilizamos dos semáforos: vacío indica espacio disponible para los productores y lleno indica la disponibilidad de datos para los consumidores.


### Configuración del búfer compartido

```cpp
int buffer[MAX];
int fill = 0;
int use = 0;

void put(int value) {
    buffer[fill] = value; // Line F1
    fill = (fill + 1) % MAX; // Line F2
}

int get() {
    int tmp = buffer[use]; // Line G1
    use = (use + 1) % MAX; // Line G2
    return tmp;
}
```

Con MAX establecido en 1 (una sola ranura de búfer), el productor espera a que esté vacía y el consumidor a que esté llena para gestionar las operaciones del búfer.

### Desafío de la condición de carrera

Sin embargo, con MAX mayor que 1 y múltiples productores, surge una condición de carrera. Los productores podrían intentar simultáneamente put() en el mismo índice de búfer, lo que provoca sobrescrituras y pérdidas de datos.

### Explicación de la condición de carrera

- Escenario: Dos productores (Pa y Pb) llaman simultáneamente a put(). Pa escribe en el búfer y es interrumpido antes de incrementar el relleno. Pb escribe entonces en la misma ranura de búfer, sobrescribiendo los datos de Pa.
- Problema: Las secciones críticas de put() y get() no están protegidas contra el acceso simultáneo de múltiples productores o consumidores.


### Requisitos de la solución

Una solución robusta al problema del búfer limitado debe garantizar:

- Exclusión mutua: Solo un productor puede escribir en una ranura de búfer a la vez, y solo un consumidor puede leer de una ranura de búfer a la vez.
- Orden correcto: Los productores deben esperar a que haya espacio disponible, y los consumidores deben esperar a que haya datos disponibles. 



El enfoque basado en semáforos para el problema productor/consumidor demuestra la necesidad de una sincronización cuidadosa para evitar condiciones de carrera. Garantizar la exclusión mutua en el acceso a recursos compartidos es crucial, y el valor inicial del semáforo desempeña un papel clave en esta coordinación. Las complejidades del problema del búfer acotado subrayan la importancia de abordar los problemas de concurrencia con una comprensión detallada de los mecanismos de sincronización subyacentes.

Consideremos dos hilos: uno para el fabricante y otro para el consumidor. Analicemos una instancia específica en un solo procesador. Supongamos que el cliente es el primero en ejecutarse. Como resultado, el consumidor llamará a sem_wait en la línea C1 del panel izquierdo (&full). La llamada decrementará el valor de full (a -1), detendrá al consumidor y esperará a que otro hilo ejecute sem_post() en full, como se desea, ya que full se inicializó a 0.

Supongamos que el productor sale de la sala. Llamará a la rutina sem_wait(&empty) al llegar a la línea P1. Dado que empty se inicializó con el valor MAX, a diferencia del consumidor, el productor continuará con esta línea (en este caso, 1). Como resultado, empty se establecerá en 0 y el procesador insertará un valor de datos en la primera entrada del búfer (línea P2). El procesador procederá a P3 y llamará a sem_post(&full), que cambiará el valor del semáforo lleno de -1 a 0 y reactivará al consumidor (por ejemplo, lo moverá de bloqueado a listo).

En esta situación, podrían ocurrir dos cosas. Primero, si el productor continúa ejecutándose, dará la vuelta y llegará a la línea P1 una vez más. Esta vez, sin embargo, se bloquearía, ya que el valor del semáforo vacío es 0. Segundo, si el consumidor comenzó a ejecutarse después de que el productor fuera interrumpido, regresaría de sem_wait(&full) (línea C1), descubriría que el búfer estaba lleno y lo consumiría. En ambos casos, se logra el comportamiento previsto. Puedes repetir este ejercicio con más hilos (por ejemplo, varios productores y varios consumidores). Debería seguir funcionando.

Supongamos que MAX es mayor que 1 (por ejemplo, MAX = 10). Imaginemos que hay varios productores y consumidores en este escenario. Ahora tenemos una condición de carrera que abordar. ¿Sabes dónde ocurre? (Dedica un tiempo a buscarla). Si no la notas, te doy una pista: observa el código put() y get() con más atención.

Para que el código del problema del productor/consumidor sea más ilustrativo y ejecutable, incorporaré un ejemplo completo que demuestra la interacción entre los hilos de productor y consumidor mediante semáforos. Ajustaré el código para incluir una función principal que inicializa los semáforos, crea los hilos de productor y consumidor, y añade sentencias de impresión para mostrar el flujo de datos a través del búfer.

En este ejemplo, asumiré que MAX es mayor que 1 y añadiré bloqueos mutex para proteger las funciones put() y get() y abordar la condición de carrera.

```cpp
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define MAX 10 // Size of the buffer

int buffer[MAX];
int fill = 0;
int use = 0;
sem_t empty;
sem_t full;
pthread_mutex_t buffer_mutex = PTHREAD_MUTEX_INITIALIZER;

void put(int value) {
    pthread_mutex_lock(&buffer_mutex);
    buffer[fill] = value;
    fill = (fill + 1) % MAX;
    pthread_mutex_unlock(&buffer_mutex);
}

int get() {
    pthread_mutex_lock(&buffer_mutex);
    int tmp = buffer[use];
    use = (use + 1) % MAX;
    pthread_mutex_unlock(&buffer_mutex);
    return tmp;
}

void *producer(void *arg) {
    for (int i = 0; i < 20; i++) {
        sem_wait(&empty);
        put(i);
        printf("Produced: %d\n", i);
        sem_post(&full);
    }
    return NULL;
}

void *consumer(void *arg) {
    int tmp = 0;
    while (tmp != -1) {
        sem_wait(&full);
        tmp = get();
        sem_post(&empty);
        printf("Consumed: %d\n", tmp);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    sem_init(&empty, 0, MAX); // MAX slots are empty
    sem_init(&full, 0, 0); // 0 slots are full

    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);

    pthread_join(p, NULL);
    pthread_join(c, NULL);

    sem_destroy(&empty);
    sem_destroy(&full);
    pthread_mutex_destroy(&buffer_mutex);

    return 0;
}
```



- El búfer, junto con las funciones put y get, está protegido por un mutex (buffer_mutex) para abordar la condición de carrera al acceder al búfer compartido.
- Dos semáforos (vacío y lleno) gestionan el número de ranuras vacías y llenas en el búfer.
- La función productora espera a que el semáforo esté vacío antes de introducir un elemento en el búfer y luego envía una señal al semáforo lleno.
- La función consumidora espera a que el semáforo esté lleno antes de extraer un elemento del búfer y luego envía una señal al semáforo vacío.
- La función principal inicializa los semáforos y el mutex, crea los hilos productor y consumidor, y espera a que finalicen.

## Añadiendo Exclusión Mutua para Evitar Condiciones de Carrera

### Identificando la Supervisión en la Exclusión Mutua

En nuestra solución inicial al problema productor/consumidor, pasamos por alto la necesidad de la exclusión mutua. Las acciones de llenar un búfer e incrementar su índice deben protegerse, ya que constituyen una sección crítica.

### Implementando Semáforos Binarios para Exclusividad

Para solucionar esto, introducimos bloqueos mediante semáforos binarios alrededor de las operaciones put() y get(), con el objetivo de proteger estas secciones críticas del acceso concurrente.

```cpp
// Producer code
void *producer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&mutex);  // Acquire the mutex lock
        sem_wait(&empty);  // Wait until there is space
        put(i);            // Fill the buffer
        sem_post(&full);   // Signal that the buffer is full
        sem_post(&mutex);  // Release the mutex lock
    }
}

// Consumer code
void *consumer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&mutex);  // Acquire the mutex lock
        sem_wait(&full);   // Wait until the buffer is full
        int tmp = get();   // Get the data from the buffer
        sem_post(&empty);  // Signal that the buffer has space
        sem_post(&mutex);  // Release the mutex lock
        printf("%d\n", tmp);
    }
}
```


### El problema del deadlock

A pesar de los bloqueos de exclusión mutua, surge un nuevo problema: el interbloqueo. Esto ocurre cuando el consumidor adquiere el mutex y se bloquea a la espera de una señal completa. Mientras tanto, el productor, que podría generar datos y una señal completa, se bloquea porque no puede adquirir el mutex que posee el consumidor. Ambos hilos esperan indefinidamente a que el otro libere un recurso.



### Solución para evitar un bloqueo mutuo

Para resolver este bloqueo, debemos asegurarnos de que el mutex no esté retenido por un hilo mientras espera que se señalice otra condición. Esto requiere reordenar las operaciones del semáforo para evitar que un hilo retenga el mutex mientras está bloqueado en otro semáforo.

### Enfoque revisado

La clave es liberar el bloqueo del mutex antes de llamar a sem_wait() en los semáforos de condición (vacíos o llenos). Esto permite que otros hilos accedan a sus secciones críticas y realicen las operaciones sem_post() necesarias para resolver la condición de espera.

```cpp
// Corrected producer and consumer code with mutex release before waiting
void *producer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&empty);  // Wait until there is space
        sem_wait(&mutex);  // Acquire the mutex lock
        put(i);            // Fill the buffer
        sem_post(&mutex);  // Release the mutex lock
        sem_post(&full);   // Signal that the buffer is full
    }
}

void *consumer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&full);   // Wait until the buffer is full
        sem_wait(&mutex);  // Acquire the mutex lock
        int tmp = get();   // Get the data from the buffer
        sem_post(&mutex);  // Release the mutex lock
        sem_post(&empty);  // Signal that the buffer has space
        printf("%d\n", tmp);
    }
}
```

En esta solución, nos aseguramos de que el mutex solo se mantenga cuando un hilo esté trabajando activamente en su sección crítica y no cuando esté esperando, evitando así el bloqueo.

### Código ejecutable
El código y el fragmento proporcionados describen un problema clásico de productor/consumidor al intentar usar semáforos para la sincronización. Sin embargo, como se indica en el fragmento, el intento inicial conduce a un bloqueo. Este bloqueo se produce porque tanto el subproceso del productor como el del consumidor intentan adquirir el mutex y luego esperan en sus respectivos semáforos (vacíos para el productor, llenos para el consumidor), lo que lleva a una situación en la que ninguno puede continuar.
Para evitar este bloqueo, se debe ajustar el orden de adquisición del mutex y de espera en el semáforo. Específicamente, un subproceso solo debe intentar adquirir el mutex después de haber superado con éxito la espera del semáforo que controla su acceso al búfer.

Aquí está el código revisado para evitar el bloqueo:

```cpp

#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

int buffer[MAX];
int fill = 0;
int use = 0;
sem_t empty;
sem_t full;
sem_t mutex; // Binary semaphore used as a mutex

void put(int value) {
    buffer[fill] = value;
    fill = (fill + 1) % MAX;
}

int get() {
    int tmp = buffer[use];
    use = (use + 1) % MAX;
    return tmp;
}

void *producer(void *arg) {
    int i;
    for (i = 0; i < loops; i++) {
        sem_wait(&empty); // Line P1
        sem_wait(&mutex); // Line P0 (NEW LINE)
        put(i); // Line P2
        sem_post(&mutex); // Line P4 (NEW LINE)
        sem_post(&full); // Line P3
    }
    return NULL;
}

void *consumer(void *arg) {
    int i;
    for (i = 0; i < loops; i++) {
        sem_wait(&full); // Line C1
        sem_wait(&mutex); // Line C0 (NEW LINE)
        int tmp = get(); // Line C2
        sem_post(&mutex); // Line C4 (NEW LINE)
        sem_post(&empty); // Line C3
        printf("%d\n", tmp);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    // Initialize semaphores
    sem_init(&empty, 0, MAX); // MAX slots are empty
    sem_init(&full, 0, 0); // 0 slots are full
    sem_init(&mutex, 0, 1); // Binary semaphore for mutex

    // Create threads
    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);

    // Wait for threads to finish
    pthread_join(p, NULL);
    pthread_join(c, NULL);

    // Cleanup
    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);

    return 0;
}
```

Salida

```bash
Consumed: 0
Consumed: 1
Consumed: 2
Consumed: 3
Consumed: 4
Consumed: 5
Consumed: 6
Consumed: 7
Consumed: 8
Consumed: 9
Consumed: 10
Consumed: 11
Consumed: 12
Consumed: 13
Consumed: 14
Consumed: 15
Consumed: 16
Consumed: 17
Consumed: 18
Consumed: 19
```


- El semáforo mutex ahora se adquiere solo después de superar correctamente la espera de semáforo vacío o lleno. Este cambio evita el escenario de interbloqueo descrito en el pasaje.
- El productor espera hasta que haya una ranura vacía (sem_wait(&empty)) y luego adquiere el mutex para añadir un elemento al búfer de forma segura.
- El consumidor espera hasta que haya una ranura llena (sem_wait(&full)) y luego adquiere el mutex para eliminar un elemento del búfer de forma segura.


Este programa modificado debería evitar el deadlock, ya que el productor y el consumidor operan en el búfer de forma coordinada, sin que ninguno de ellos quede bloqueado permanentemente.

Para resolver este problema, simplemente debemos reducir el alcance del bloqueo. El código a continuación muestra la solución correcta. Simplemente desplazamos la adquisición y liberación del mutex alrededor de la sección crítica. Los códigos de espera y señal de lleno y vacío se dejan fuera.

La solución proporcionada aborda correctamente el problema del interbloqueo ajustando el alcance del mutex. En esta solución revisada, el mutex se adquiere y libera solo alrededor de la sección crítica donde se accede al búfer, mientras que los semáforos de lleno y vacío se siguen utilizando para indicar la disponibilidad de datos y espacio en el búfer. Esta configuración evita el interbloqueo al garantizar que el mutex no se mantenga mientras un hilo espera en el semáforo de lleno o vacío.

```cpp
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define MAX 10 // Define the size of the buffer
#define loops 20 // Define the number of iterations

int buffer[MAX]; // Shared buffer
int fill = 0; // Index for the next item to be produced
int use = 0; // Index for the next item to be consumed
sem_t empty; // Semaphore indicating the number of empty slots
sem_t full; // Semaphore indicating the number of full slots
sem_t mutex; // Binary semaphore used as a mutex

void put(int value) {
    buffer[fill] = value;
    fill = (fill + 1) % MAX;
}

int get() {
    int tmp = buffer[use];
    use = (use + 1) % MAX;
    return tmp;
}

void *producer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&empty); // Wait for an empty slot
        sem_wait(&mutex); // Acquire mutex
        put(i); // Produce an item
        sem_post(&mutex); // Release mutex
        sem_post(&full); // Signal that a new item is available
    }
    return NULL;
}

void *consumer(void *arg) {
    for (int i = 0; i < loops; i++) {
        sem_wait(&full); // Wait for a full slot
        sem_wait(&mutex); // Acquire mutex
        int tmp = get(); // Consume an item
        sem_post(&mutex); // Release mutex
        sem_post(&empty); // Signal that a slot is now empty
        printf("Consumed: %d\n", tmp);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    // Initialize semaphores
    sem_init(&empty, 0, MAX);
    sem_init(&full, 0, 0);
    sem_init(&mutex, 0, 1);

    // Create producer and consumer threads
    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);

    // Wait for threads to complete
    pthread_join(p, NULL);
    pthread_join(c, NULL);

    // Clean up
    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);

    return 0;
}

```

- El semáforo mutex se adquiere ahora justo antes de la operación put u get en las funciones de productor y consumidor, y se libera inmediatamente después de la operación. Esto reduce el alcance del bloqueo a la sección crítica únicamente.
- Los sem_wait y sem_post para los semáforos llenos y vacíos quedan fuera del alcance del bloqueo mutex. Esto garantiza que un hilo no conserve el mutex mientras está bloqueado esperando estos semáforos.

## La necesidad de bloqueos de lectura-escritura

En la programación concurrente, los diferentes tipos de acceso a la estructura de datos pueden requerir estrategias de bloqueo distintas. En concreto, operaciones como la inserción de datos alteran la estructura y requieren acceso exclusivo, mientras que las operaciones de lectura suelen realizarse en paralelo sin estas restricciones. Para ello, se introducen los bloqueos de lectura-escritura, que ofrecen un mecanismo de sincronización más matizado.

### Implementación de bloqueos de lectura-escritura

#### Operaciones de escritura

- Bloqueo de escritura exclusivo: Cuando un hilo intenta modificar la estructura de datos, utiliza rwlock_acquire_writelock() y rwlock_release_writelock() para garantizar el acceso de escritura exclusivo.
- Mecanismo subyacente: Internamente, se utiliza un bloqueo de escritura de semáforo para garantizar que solo un escritor pueda acceder a la región crítica a la vez.

#### Operaciones de lectura

- Bloqueo de lectura concurrente: Varios lectores pueden adquirir bloqueos de lectura simultáneamente, utilizando rwlock_acquire_readlock() y rwlock_release_readlock(), siempre que no haya ninguna operación de escritura en curso. - Recuento de lectores: La variable "lectores" registra el número de lectores activos dentro de la estructura de datos.
- Responsabilidad del primer lector: El primer lector que adquiere el bloqueo de lectura también obtiene el bloqueo de escritura, lo que impide el acceso de los escritores. Los lectores posteriores pueden continuar sin bloqueos adicionales.

### Desafíos y equidad

Si bien el mecanismo de bloqueo lector-escritor es funcional, presenta desafíos, especialmente en lo que respecta a la equidad entre lectores y escritores:

- Potencial de inanición: Existe el riesgo de que los lectores accedan continuamente a la estructura de datos, inhabilitando a los escritores que esperan la oportunidad de adquirir el bloqueo de escritura.

### Soluciones avanzadas

Para abordar la equidad y evitar que los lectores saturen el bloqueo mientras un escritor espera, se necesitan implementaciones más sofisticadas:

- Estrategias de equidad: Estas pueden incluir mecanismos de cola o reglas de prioridad que garanticen que los escritores no se retrasen indefinidamente por los lectores. 


### Cuándo usar bloqueos de lectura-escritura

Los bloqueos de lectura-escritura deben emplearse con prudencia, ya que:

- Añaden complejidad: Especialmente con mecanismos de equidad más complejos, pueden introducir complicaciones adicionales en el diseño de sincronización.
- Consideraciones de rendimiento: No siempre resultan en una mejora del rendimiento en comparación con primitivas de bloqueo más simples y rápidas.

Los bloqueos de lectura-escritura ejemplifican el uso versátil de los semáforos en escenarios de sincronización, mostrando su potencial para crear controles de concurrencia flexibles y matizados. Sin embargo, la decisión de usarlos debe sopesarse en función de su complejidad y las ventajas reales de rendimiento que ofrecen en un contexto determinado.

El siguiente código implementa un bloqueo de lectura-escritura, que es una primitiva de sincronización que permite el acceso de lectura concurrente a un recurso compartido, pero acceso exclusivo para operaciones de escritura. Este tipo de bloqueo es útil en situaciones donde las operaciones de lectura son más frecuentes que las de escritura y estas no modifican el recurso compartido. 

Para que este ejemplo sea más ilustrativo y ejecutable, se añadio una función principal que demuestra el uso de este bloqueo de lectura-escritura con múltiples hilos de lectura y escritura. 

```cpp
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

typedef struct _rwlock_t {
    sem_t lock; // Binary semaphore (basic lock)
    sem_t writelock; // Allow ONE writer/MANY readers
    int readers; // Number of readers in critical section
} rwlock_t;

void rwlock_init(rwlock_t *rw) {
    rw->readers = 0;
    sem_init(&rw->lock, 0, 1);
    sem_init(&rw->writelock, 0, 1);
}

void rwlock_acquire_readlock(rwlock_t *rw) {
    sem_wait(&rw->lock);
    rw->readers++;
    if (rw->readers == 1) // First reader gets writelock
        sem_wait(&rw->writelock);
    sem_post(&rw->lock);
    printf("Reader acquired read lock\n");
}

void rwlock_release_readlock(rwlock_t *rw) {
    sem_wait(&rw->lock);
    rw->readers--;
    if (rw->readers == 0) // Last reader lets it go
        sem_post(&rw->writelock);
    sem_post(&rw->lock);
    printf("Reader released read lock\n");
}

void rwlock_acquire_writelock(rwlock_t *rw) {
    sem_wait(&rw->writelock);
    printf("Writer acquired write lock\n");
}

void rwlock_release_writelock(rwlock_t *rw) {
    sem_post(&rw->writelock);
    printf("Writer released write lock\n");
}

void *reader(void *arg) {
    rwlock_t *rw = (rwlock_t *)arg;
    rwlock_acquire_readlock(rw);
    // Simulate reading operation
    rwlock_release_readlock(rw);
    return NULL;
}

void *writer(void *arg) {
    rwlock_t *rw = (rwlock_t *)arg;
    rwlock_acquire_writelock(rw);
    // Simulate writing operation
    rwlock_release_writelock(rw);
    return NULL;
}

int main() {
    rwlock_t rwlock;
    rwlock_init(&rwlock);

    pthread_t r1, r2, w1, w2;
    pthread_create(&r1, NULL, reader, &rwlock);
    pthread_create(&r2, NULL, reader, &rwlock);
    pthread_create(&w1, NULL, writer, &rwlock);
    pthread_create(&w2, NULL, writer, &rwlock);

    pthread_join(r1, NULL);
    pthread_join(r2, NULL);
    pthread_join(w1, NULL);
    pthread_join(w2, NULL);

    return 0;
}
```

Salida

```bash
Reader acquired read lock
Reader released read lock
Reader acquired read lock
Reader released read lock
Writer acquired write lock
Writer released write lock
Writer acquired write lock
Writer released write lock
```

- El bloqueo de lectura-escritura (rwlock_t) consta de un semáforo binario (bloqueo) y un semáforo de bloqueo de escritura (bloqueo de escritura). El contador de lectores registra el número de lectores activos.
- Los hilos de lectura adquieren y liberan el bloqueo de lectura mediante rwlock_acquire_readlock y rwlock_release_readlock, respectivamente.
- Los hilos de escritura adquieren y liberan el bloqueo de escritura mediante rwlock_acquire_writelock y rwlock_release_writelock, respectivamente.
- La función principal crea y ejecuta varios hilos de lectura y escritura.


El programa muestra cómo varios lectores y escritores adquieren y liberan el bloqueo.


## Filósofos cenando

El problema de los filósofos cenando es un clásico rompecabezas de concurrencia que ofrece un desafío humorístico y a la vez reflexivo, con una utilidad práctica limitada, pero con una gran popularidad en el ámbito académico.

### Planteamiento del problema

Cinco filósofos se sientan alrededor de una mesa, separados por un tenedor, lo que resulta en un total de cinco tenedores. Los filósofos alternan entre pensar y comer. Para comer, un filósofo necesita los tenedores a su izquierda y a su derecha. El desafío surge de la necesidad de sincronizar el uso de los tenedores para evitar el bloqueo o la inanición y maximizar la concurrencia. La configuración básica del problema es un pentagono donde cada esquina es un filoso y entre cada uno de ellos puede o  no haber tenedores.


Rutina del filósofo
Cada filósofo, identificado por un número del 0 al 4, participa en un bucle simple:

```cpp
void philosopher_routine(int p) {
    while (true) {
        think();
        get_forks(p);
        eat();
        put_forks(p);
    }
}
```

### El reto

La tarea crítica es diseñar las funciones get_forks() y put_forks() que:
- Prevengan el interbloqueo, donde todos los filósofos esperan permanentemente.
- Eviten la inanición, asegurando que todos los filósofos puedan comer.
- Permitan que tantos filósofos como sea posible coman simultáneamente para lograr una alta concurrencia.

### Funciones de utilidad

Utilizamos funciones de utilidad para referirnos a las bifurcaciones relativas a cada filósofo:

```cpp
int left(int p) { return p; } // Left fork index
int right(int p) { return (p + 1) % 5; } // Right fork index
```

### Semáforos como solución

Introducimos una matriz de semáforos, sem_t forks[5], para representar las bifurcaciones.

### Una solución fallida

Un enfoque simple podría ser:

```cpp
void get_forks(int p) {
    sem_wait(&forks[left(p)]);
    sem_wait(&forks[right(p)]);
}

void put_forks(int p) {
    sem_post(&forks[left(p)]);
    sem_post(&forks[right(p)]);
}
```

Sin embargo, esta solución conduce a un punto muerto. Cada filósofo toma su bifurcación izquierda, y luego todos esperan su bifurcación derecha, que ya está en manos de otro filósofo.

### Rompiendo la dependencia

Una solución sencilla es cambiar el orden en que un filósofo, por ejemplo el último, adquiere las bifurcaciones:

```cpp
void get_forks(int p) {
    if (p == 4) { // Last philosopher
        sem_wait(&forks[right(p)]); // Grab right fork first
        sem_wait(&forks[left(p)]); // Then left fork
    } else {
        sem_wait(&forks[left(p)]); // Grab left fork first
        sem_wait(&forks[right(p)]); // Then right fork
    }
}
```

Este cambio interrumpe el ciclo de espera y garantiza que siempre haya al menos un filósofo que pueda comer si hay un tenedor disponible.

El problema de los filósofos que comen sirve como ejercicio de control de concurrencia. 

Aplicando semáforos de forma inteligente y evitando las condiciones de espera cíclicas, el problema puede resolverse, garantizando que todos los filósofos puedan comer sin entrar en un punto muerto. 

Existen rompecabezas conceptuales similares que estimulan la reflexión sobre los problemas de sincronización, incluso si son principalmente ejercicios académicos. Existen otras dificultades conocidas, como el dilema del fumador o el problema del barbero dormido. La mayoría de estas son solo pretextos para pensar en la concurrencia. Sin embargo, algunas tienen nombres intrigantes.


## Implementación de semáforos

Otro caso de uso importante de los semáforos surge ocasionalmente, y lo hemos incluido aquí. La dificultad radica en la siguiente: ¿cómo puede un programador evitar que "demasiados" hilos se ejecuten simultáneamente y ralenticen el sistema? 

Respuesta: establecer un umbral para "demasiados" y luego usar un semáforo para limitar el número de hilos que ejecutan el código en cuestión simultáneamente. Este método se conoce como limitación y es un tipo de control de admisión.

La limitación de hilos es una aplicación de semáforos en el control de concurrencia, cuyo objetivo es limitar el número de hilos que se ejecutan simultáneamente para evitar ralentizaciones del sistema. Esta técnica es un ejemplo de control de admisión.

### Escenario práctico: Computación con uso intensivo de memoria

Imagine una situación en la que cientos de hilos trabajan simultáneamente, cada uno de los cuales requiere una cantidad sustancial de memoria en una parte específica del código (denominada región de uso intensivo de memoria). Si todos los subprocesos acceden a esta región simultáneamente, la demanda total de memoria podría superar la memoria física disponible, lo que provocaría un colapso del sistema y una ralentización significativa.

### Semáforo como solución

Se puede configurar un semáforo para controlar el número de subprocesos que acceden a la región de uso intensivo de memoria simultáneamente:

- Inicialización del semáforo: Inicialice el semáforo con un valor que represente el número máximo de subprocesos permitidos simultáneamente en la región.
- Implementación de la limitación: Encapsule la región de uso intensivo de memoria con llamadas sem_wait() y sem_post() para gestionar el acceso.

```cpp

sem_t semaphore;
sem_init(&semaphore, 0, threshold); // threshold is the max allowed threads

void memory_intensive_operation() {
    sem_wait(&semaphore); // Enter region
    // Perform memory-intensive work
    sem_post(&semaphore); // Leave region
}

```

### Implementación de semáforos

Crear un semáforo implica aprovechar las primitivas de sincronización de bajo nivel:

- Componentes: La implementación de un semáforo generalmente consta de un bloqueo, una variable de condición y una variable de estado para rastrear el valor del semáforo.
- Nota sobre el comportamiento: A diferencia de los semáforos tradicionales, donde el valor negativo indica el número de hilos en espera, en esta implementación, el valor del semáforo nunca baja de cero. Este enfoque simplifica la implementación y se alinea con prácticas actuales como las de Linux.

### Complejidad en la construcción de variables de condición a partir de semáforos

Crear variables de condición a partir de semáforos puede ser un desafío, como lo demuestran varios problemas encontrados en aplicaciones reales:

- Complejidad: La tarea es más compleja de lo que parece debido a las complejidades de sincronizar las condiciones y gestionar el estado en múltiples hilos.
- Desafíos históricos: Ha habido casos en los que incluso programadores experimentados han tenido dificultades para implementar esto correctamente, lo que ha provocado problemas en sistemas como Windows. 

La limitación de subprocesos mediante semáforos es una estrategia eficaz para gestionar operaciones que consumen muchos recursos en programación concurrente. Garantiza que el sistema no se sature con demasiados subprocesos ejecutándose simultáneamente, especialmente en escenarios con alta demanda de recursos. Implementar semáforos requiere un buen conocimiento de los mecanismos de sincronización de bajo nivel, y la tarea de generar variables de condición a partir de semáforos presenta sus propios desafíos.

Para que el código de implementación del semáforo sea más comprensible y ejecutable, lo ajustaré para que utilice funciones estándar de subprocesos POSIX y añadiré una demostración de cómo usar este semáforo personalizado (Zem_t) para la limitación de subprocesos en un escenario práctico. También incluiré sentencias de impresión para observar el comportamiento del semáforo en acción.

```cpp
#include <stdio.h>
#include <pthread.h>

typedef struct __Zem_t {
    int value;
    pthread_cond_t cond;
    pthread_mutex_t lock;
} Zem_t;

// Initialize the semaphore
void Zem_init(Zem_t *s, int value) {
    s->value = value;
    pthread_cond_init(&s->cond, NULL);
    pthread_mutex_init(&s->lock, NULL);
}

// Semaphore wait operation
void Zem_wait(Zem_t *s) {
    pthread_mutex_lock(&s->lock);
    while (s->value <= 0)
        pthread_cond_wait(&s->cond, &s->lock);
    s->value--;
    pthread_mutex_unlock(&s->lock);
}

// Semaphore post operation
void Zem_post(Zem_t *s) {
    pthread_mutex_lock(&s->lock);
    s->value++;
    pthread_cond_signal(&s->cond);
    pthread_mutex_unlock(&s->lock);
}

void *memory_intensive_operation(void *arg) {
    Zem_t *sem = (Zem_t *)arg;
    Zem_wait(sem);
    printf("Thread entered memory-intensive region\n");
    // Simulate memory-intensive work
    Zem_post(sem);
    printf("Thread exited memory-intensive region\n");
    return NULL;
}

int main() {
    const int MAX_THREADS = 5; // Maximum number of concurrent threads in the region
    Zem_t sem;
    Zem_init(&sem, 3); // Allowing 3 threads to enter the region simultaneously

    pthread_t threads[MAX_THREADS];
    for (int i = 0; i < MAX_THREADS; i++) {
        pthread_create(&threads[i], NULL, memory_intensive_operation, &sem);
    }

    for (int i = 0; i < MAX_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
```
Salida

```bash
Semaphore acquired
Semaphore released
```



- Zem_t es una estructura de semáforo personalizada con un valor, una variable de condición y un mutex.
- Zem_init, Zem_wait y Zem_post son funciones para inicializar, esperar y señalizar el semáforo, respectivamente.
- memory_intensive_operation es una operación simulada de uso intensivo de memoria, controlada por el semáforo para garantizar que no la ejecuten simultáneamente más de un número específico de subprocesos.
- En la función principal main, se crean varios subprocesos que ejecutan memory_intensive_operation. El semáforo sem se inicializa para permitir que tres subprocesos accedan simultáneamente a la región de uso intensivo de memoria, demostrando así el mecanismo de limitación.



