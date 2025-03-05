# # Introduccion a estructuras de datos thread safe

para entender este tema veremos que esta por debajo de nuestras herramientas asi que haremos un poco de código de C/C++


- Entender los fundamentos de las estructuras de datos concurrentes
- Implementar operaciones thread safe 
- Analizar y resolver problemas de performance
- Evaluar concurrent vs trade off de performance


Antes de profundizar en el ámbito de los bloqueos, es fundamental comprender cómo integrarlos en estructuras de datos comunes para lograr la seguridad de los subprocesos. 

Las preguntas clave aquí son:

- **Cómo agregar bloqueos(Locks) de manera efectiva**: ¿Cuáles son las estrategias para agregar bloqueos a una estructura de datos para garantizar un acceso simultáneo correcto?
-- **Consideraciones de rendimiento**: ¿Cómo se pueden aplicar los bloqueos de una manera que mantenga la velocidad y permita el acceso simultáneo de varios subprocesos?


Empecemos con el caso del la estructura de datos El Contador.


Crea un Contador no concurrente de la manera más simnple sería parecido al siguiente ejemplo:

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

### Observaciones

- Simplicidad: este contador es fácil de implementar, pero carece de seguridad para subprocesos.
- Problemas de escalabilidad: sin sincronización, este contador no es adecuado para entornos concurrentes.

## Hagamos el contador thread safe


Agregaremos un Lock (Bloqueo)

Para hacer el contador thread-safe vamos a agregar un lock cada vez que cualquier metodo intente manipular la información de la estructura de datos y lo liberaremos al retornar desde la llamada.


Ejemplo de lock


```cpp
// Pseudo codigo para el contador thread-safe 
lock_t lock; 

void increment(counter_t *c) {
    lock(&lock);
    c->value++;
    unlock(&lock);
}
// lo mismo para incrementar su valor u obtenerlo
```


## Patrón de Diseño


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
|6|5->0|1|3|4|5(from L1)|
|7|0|2|4|5->0|10(from L4)|


El umbral `S` se establece en 5 en este ejemplo, y los subprocesos en cada una de las cuatro CPU están actualizando sus conteos locales L1 ... L4. A medida que el tiempo disminuye, el valor del contador global (G) también se indica en el seguimiento. Un contador local se puede incrementar en cada paso de tiempo, si el valor local alcanza el umbral S, se transfiere al contador global y el contador local se reinicia.

El rendimiento de los contadores de aproximación con un umbral `S` de 1024 muestra que el rendimiento es excelente. Actualizar el contador cuatro millones de veces en cuatro procesadores lleva aproximadamente la misma cantidad de tiempo que actualizarlo un millón de veces en una CPU.

El valor del umbral `S`, con cuatro subprocesos en cuatro CPU, cada uno incrementando el contador un millón de veces. Cuando `S` es bajo, el rendimiento es terrible (aunque el conteo global siempre es preciso). Cuando S es alto, el rendimiento es excelente, pero el recuento global se retrasa (como máximo, en la cantidad de CPU multiplicada por S). Los contadores aproximados permiten este equilibrio entre precisión y rendimiento.


## Operaciones concurrentes en una Liked List

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
Posibles alternativas
Enfoques híbridos: investigar un método híbrido, donde se adquiere un bloqueo para cada pocos nodos, podría ser una solución más práctica. Colas concurrentes: el enfoque de Michael y Scott
Estructura de cola de dos bloqueos
Implementación: a diferencia del método más simple de usar un solo bloqueo prominente, el diseño de Michael y Scott para una cola concurrente implica dos bloqueos separados: uno para la cabeza y otro para la cola.
Mejora de la concurrencia: esta estructura permite que las operaciones de encolado utilicen principalmente el bloqueo de cola y las operaciones de desencolado utilicen el bloqueo de cabeza, lo que permite la ejecución concurrente de estas funciones.
Técnica del nodo ficticio
Propósito: un nodo ficticio, asignado durante la inicialización de la cola, separa las operaciones de cabeza y cola, lo que mejora aún más la concurrencia.
Comprensión de la cola
Interacción con el código: para comprender completamente cómo funciona la cola concurrente de Michael y Scott, es beneficioso leer, escribir y ejecutar el código usted mismo. Medir su rendimiento puede proporcionar información valiosa.
Aplicación de colas en sistemas multiproceso
Frecuencia de uso: las colas son comunes en aplicaciones multiproceso, pero a menudo requieren más que solo bloqueos para satisfacer las demandas de dichos sistemas.
Próximo tema: el próximo capítulo explorará una cola limitada más desarrollada que utiliza variables de condición, adecuadas para escenarios en los que un hilo necesita esperar si la cola está vacía o demasiado llena.
El programa en el panel izquierdo muestra el proceso de poner y quitar elementos de la cola, mostrando la concurrencia lograda mediante el uso de bloqueos separados para la cabeza y la cola de la cola.



Explicación:
Inicialización de la cola: la función Queue_Init inicializa una cola vacía con un nodo ficticio.
Operaciones de puesta en cola y desconexión de la cola: Queue_Enqueue agrega un elemento en la cola y Queue_Dequeue elimina un elemento de la cabecera de la cola. Ambas operaciones están protegidas por bloqueos separados (head_lock y tail_lock), lo que mejora la concurrencia.
Funciones de subproceso: EnqueueThread y DequeueThread se utilizan para demostrar la puesta en cola y la desconexión de la cola simultáneas.
Función principal: inicializa la cola, crea dos subprocesos (uno para poner en cola y otro para desconexión de la cola) y espera a que completen sus operaciones.


## Tabla hash concurrente
La tabla hash es una estructura de datos versátil y ampliamente utilizada, y concluimos nuestro análisis de las estructuras de datos concurrentes centrándonos en una tabla hash simple y no redimensionable.
Estructura y rendimiento
Implementación: La tabla hash concurrente se construye utilizando las listas concurrentes que hemos analizado anteriormente.
Mecanismo de bloqueo: Cada contenedor hash, representado por una lista, tiene su propio bloqueo. Esto difiere del uso de un único bloqueo para toda la tabla.
Ventajas: Al asignar un bloqueo por contenedor hash, la tabla hash permite que se produzcan múltiples operaciones simultáneamente, lo que mejora significativamente su rendimiento.
ex3
El gráfico anterior representa el rendimiento de la tabla hash cuando se realizan muchas actualizaciones simultáneamente (de 10 000 a 50 000 actualizaciones simultáneas de cada uno de los cuatro subprocesos, en el mismo iMac con cuatro CPU). El rendimiento de una lista enlazada también se muestra con fines comparativos (con un único bloqueo). Esta sencilla tabla hash concurrente escala perfectamente, como se muestra en el gráfico; Por otro lado, la lista enlazada no lo hace.
Resumen de lecciones de las estructuras de datos concurrentes
Conclusiones clave
Gestión de bloqueos: tenga cuidado al adquirir y liberar bloqueos, especialmente durante los cambios en el flujo de control. Un manejo inadecuado puede generar errores e ineficiencias.
Concurrencia frente a rendimiento: aumentar la concurrencia no siempre se traduce en un mejor rendimiento. Es importante equilibrar los mecanismos de concurrencia con los beneficios de rendimiento reales que aportan.
Abordar los problemas de rendimiento: es esencial identificar y resolver los problemas de rendimiento a medida que surgen. Sin embargo, esto debe equilibrarse con las necesidades generales de rendimiento del programa.
Optimización prematura: una advertencia
Evitar la optimización excesiva: en la búsqueda del rendimiento, tenga cuidado con la optimización prematura. Concéntrese en realizar mejoras que realmente contribuyan a la eficacia general del programa, en lugar de optimizar aspectos que tienen poco impacto en el rendimiento más amplio.