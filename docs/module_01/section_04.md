# Gevent y como usar asyncio en aplicaciones que usan gevent

**Gevent** es una biblioteca de concurrencia basada en corrutinas que utiliza `libev` o `libuv` para manejar eventos de manera eficiente. 

Gevent es una biblioteca de Python que facilita la programación asíncrona y concurrente utilizando **corrutinas** y el patrón de **event loop**. Está basada en **libev** (un bucle de eventos de alto rendimiento) y **greenlets** (una forma de corrutinas ligeras). Gevent permite escribir código que parece síncrono, pero que en realidad es asíncrono, lo que simplifica la gestión de operaciones de E/S (entrada/salida) bloqueantes, como solicitudes de red, acceso a bases de datos, etc.

### Características principales de Gevent

1. **Programación asíncrona**: Permite manejar múltiples tareas de forma concurrente sin necesidad de hilos, lo que reduce la sobrecarga del sistema.
2. **Greenlets**: Proporciona una implementación de corrutinas llamadas **greenlets**, que son similares a los hilos, pero más ligeras y gestionadas por el bucle de eventos de Gevent.
3. **Monkey patching**: Gevent incluye una función llamada `monkey.patch_all()` que modifica las bibliotecas estándar de Python (como `socket`, `threading`, etc.) para que funcionen de manera asíncrona sin cambiar el código existente.
4. **Escalabilidad**: Es ideal para aplicaciones que necesitan manejar muchas conexiones simultáneas, como servidores web o APIs.

### Ejemplo básico de uso

```python
import gevent
from gevent import monkey

# Aplica el monkey patching para hacer que las operaciones de E/S sean asíncronas.
monkey.patch_all()

import requests

def fetch(url):
    print(f"Iniciando solicitud a {url}")
    response = requests.get(url)
    print(f"Respuesta de {url}: {len(response.content)} bytes")

# Crea tareas asíncronas (greenlets).
greenlets = [
    gevent.spawn(fetch, "https://www.example.com"),
    gevent.spawn(fetch, "https://www.google.com"),
    gevent.spawn(fetch, "https://www.github.com"),
]

# Espera a que todas las tareas terminen.
gevent.joinall(greenlets)
```

`monkey.patch_all()` puede afectar a varios módulos de la biblioteca estándar de Python, incluyendo:

- **socket**: Reemplaza las funciones de red para que sean no bloqueantes.
- **ssl**: Similar a socket, pero para conexiones seguras.
- **select**: Reemplaza las funciones de selección para que funcionen con greenlets.
- **thread**: Reemplaza las funciones relacionadas con hilos para que funcionen con greenlets.
- **time**: Reemplaza funciones relacionadas con el tiempo para que sean compatibles con gevent.
- **os**: Reemplaza ciertas funciones relacionadas con el sistema operativo, como os.fork().
- **subprocess**: Reemplaza las funciones relacionadas con la creación de subprocesos.
- **threading**: Reemplaza las funciones relacionadas con hilos para que funcionen con greenlets.



### Casos de uso comunes

- **Servidores web**: Gevent se usa a menudo con frameworks como Flask o Django para manejar muchas conexiones simultáneas.
- **Scraping web**: Para realizar múltiples solicitudes HTTP de forma concurrente.
- **Procesamiento de colas**: Manejo de tareas en segundo plano de manera eficiente.

### Ventajas

- Fácil de usar si ya estás familiarizado con la programación síncrona.
- Alto rendimiento en aplicaciones de E/S intensiva.
- Compatible con muchas bibliotecas de Python gracias al monkey patching.

### Desventajas

- El monkey patching puede causar problemas si no se usa correctamente.
- No es adecuado para tareas intensivas en CPU, ya que Gevent está diseñado para operaciones de E/S.


## El modulo PyWSGI

El modulo `pywsgi`, proporciona un servidor WSGI llamado `WSGIServer` que tiene características especiales en comparación con los servidores WSGI de Flask o `asyncio.wsgi`. 

### Concurrencia basada en corrutinas (greenlets)

- **gevent**: Utiliza greenlets, que son corrutinas que permiten la ejecución concurrente sin necesidad de hilos del sistema operativo. Esto permite manejar miles de conexiones simultáneas con un overhead mínimo, ya que los greenlets son más ligeros que los hilos tradicionales.
- **Flask**: Por defecto, Flask utiliza el servidor WSGI de Werkzeug, que es un servidor síncrono y no está diseñado para manejar concurrencia de manera eficiente. Para manejar múltiples solicitudes simultáneamente, se necesitaría usar un servidor WSGI externo como `gunicorn` con workers.
- **asyncio.wsgi**: `asyncio` es una biblioteca de Python para programación asíncrona basada en `async/await`. Aunque `asyncio` puede manejar concurrencia, no utiliza greenlets, sino que se basa en el bucle de eventos de `asyncio` para manejar tareas asíncronas.

Aunque asyncio es eficiente para aplicaciones diseñadas para ser asíncronas, la gestión del bucle de eventos y el uso de async/await introducen una pequeña sobrecarga en comparación con el modelo de gevent. Además, si una aplicación síncrona se ejecuta en un executor (como un ThreadPoolExecutor), se pierde parte de la ventaja de la concurrencia asíncrona, ya que se recurre a hilos del sistema operativo, que son más pesados que los greenlets.

Existe una fuerte idea de que el modelo de gevent es más eficiente en términos de memoria y cambio de contexto para grandes cantidades de tareas concurrentes. Sin embargo, optimizaciones de asyncio dejan claro que esto ya no es asi. Asyncio suele mostrar un rendimiento bruto superior al de GEvent, especialmente en Python 3.11 y versiones posteriores. Las pruebas de rendimiento sugieren que Asyncio puede ser hasta un 50 % más rápido que GEvent en algunos casos.

`uvloop` puede mejorar significativamente el rendimiento de asyncio, duplicando potencialmente su velocidad en comparación con `gevent`. `uvloop` es una implementación de bucle de eventos alternativa para asyncio que utiliza `libuv`, una biblioteca de E/S asincrónica de alto rendimiento.

asyncio con uvloop puede aproximarse al rendimiento de los programas epoll nativos, alcanzando hasta el 88% del rendimiento epoll nativo en algunas pruebas.


Vamos a hacer algunas pruebas en sistemas más modernos y usando python3.11+.



```python title="Gevent vs Asyncio" linenums="1"
import time
import psutil
import os
from contextlib import contextmanager
import gevent
from gevent import monkey
import asyncio

# Parchear bibliotecas estándar para gevent
monkey.patch_all()

# Función para medir el uso de memoria
def memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024  # Convertir a MB
    return mem

# Simulación de una operación de E/S (por ejemplo, solicitud HTTP)
def simulate_io_task_gevent(i):
    # Simula una operación de E/S con un pequeño retardo
    gevent.sleep(0.01)  # 10ms de espera para simular E/S
    return i

async def simulate_io_task_asyncio(i):
    # Simula una operación de E/S con un pequeño retardo
    await asyncio.sleep(0.01)  # 10ms de espera para simular E/S
    return i

# Función para ejecutar tareas con gevent
def run_gevent_tasks(num_tasks):
    start_time = time.time()
    start_memory = memory_usage()

    # Crear una lista de tareas
    tasks = [gevent.spawn(simulate_io_task_gevent, i) for i in range(num_tasks)]
    # Ejecutar todas las tareas
    gevent.joinall(tasks)

    end_time = time.time()
    end_memory = memory_usage()

    print(f"gevent: {num_tasks} tareas completadas")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
    print(f"Memoria usada: {end_memory - start_memory:.2f} MB")

# Función para ejecutar tareas con asyncio
async def run_asyncio_tasks(num_tasks):
    start_time = time.time()
    start_memory = memory_usage()

    # Crear una lista de tareas
    tasks = [simulate_io_task_asyncio(i) for i in range(num_tasks)]
    # Ejecutar todas las tareas
    await asyncio.gather(*tasks)

    end_time = time.time()
    end_memory = memory_usage()

    print(f"asyncio: {num_tasks} tareas completadas")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
    print(f"Memoria usada: {end_memory - start_memory:.2f} MB")

# Ejecutar el experimento
def main():
    num_tasks = 10000  # 10,000 tareas concurrentes

    print("Ejecutando con gevent...")
    run_gevent_tasks(num_tasks)

    print("\nEjecutando con asyncio...")
    asyncio.run(run_asyncio_tasks(num_tasks))

if __name__ == "__main__":
    main()
```

```bash title="Salida"
Ejecutando con gevent...
gevent: 10000 tareas completadas
Tiempo: 0.25 segundos
Memoria usada: 16.44 MB

Ejecutando con asyncio...
asyncio: 10000 tareas completadas
Tiempo: 0.09 segundos
Memoria usada: 1.42 MB
```

#### Ejemplo utilizando funciones bloqueantes

```python title="Ejemplo con funcion bloqueante" linenums="1"
from gevent import monkey
# Parchear bibliotecas estándar para gevent
monkey.patch_all()

import time
import tracemalloc
import gevent
import asyncio
import statistics


# Simulación de una operación síncrona bloqueante
def simulate_blocking_task_gevent(i):
    time.sleep(0.01)  # Operación síncrona parcheada por gevent
    return i

async def simulate_blocking_task_asyncio(i):
    # En asyncio, necesitamos usar un executor para operaciones síncronas
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, time.sleep, 0.01)
    return i

# Función para ejecutar tareas con gevent
def run_gevent_tasks(num_tasks):
    tracemalloc.start()
    start_time = time.time()
    start_memory, _ = tracemalloc.get_traced_memory()

    tasks = [gevent.spawn(simulate_blocking_task_gevent, i) for i in range(num_tasks)]
    gevent.joinall(tasks)

    end_time = time.time()
    end_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end_time - start_time, (end_memory - start_memory) / 1024 / 1024

# Función para ejecutar tareas con asyncio
async def run_asyncio_tasks(num_tasks):
    tracemalloc.start()
    start_time = time.time()
    start_memory, _ = tracemalloc.get_traced_memory()

    tasks = [simulate_blocking_task_asyncio(i) for i in range(num_tasks)]
    await asyncio.gather(*tasks)

    end_time = time.time()
    end_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end_time - start_time, (end_memory - start_memory) / 1024 / 1024

# Ejecutar el experimento varias veces
def main():
    num_tasks = 10000
    num_runs = 5
    gevent_times = []
    gevent_memories = []
    asyncio_times = []
    asyncio_memories = []

    print("Ejecutando experimento con operaciones síncronas...")
    for i in range(num_runs):
        print(f"\nIteración {i+1}/{num_runs}")
        
        # gevent
        time_taken, memory_used = run_gevent_tasks(num_tasks)
        gevent_times.append(time_taken)
        gevent_memories.append(memory_used)
        print(f"gevent: Tiempo: {time_taken:.2f} s, Memoria: {memory_used:.2f} MB")

        # asyncio
        time_taken, memory_used = asyncio.run(run_asyncio_tasks(num_tasks))
        asyncio_times.append(time_taken)
        asyncio_memories.append(memory_used)
        print(f"asyncio: Tiempo: {time_taken:.2f} s, Memoria: {memory_used:.2f} MB")

    # Promedios
    print("\nResultados promedio:")
    print(f"gevent: Tiempo: {statistics.mean(gevent_times):.2f} s, Memoria: {statistics.mean(gevent_memories):.2f} MB")
    print(f"asyncio: Tiempo: {statistics.mean(asyncio_times):.2f} s, Memoria: {statistics.mean(asyncio_memories):.2f} MB")

if __name__ == "__main__":
    main()
```

```bash title="Salida"
Ejecutando experimento con operaciones síncronas...

Iteración 1/5
gevent: Tiempo: 0.51 s, Memoria: 10.14 MB
asyncio: Tiempo: 5.99 s, Memoria: 7.65 MB

Iteración 2/5
gevent: Tiempo: 0.49 s, Memoria: 10.00 MB
asyncio: Tiempo: 5.86 s, Memoria: 7.12 MB

Iteración 3/5
gevent: Tiempo: 0.49 s, Memoria: 10.00 MB
asyncio: Tiempo: 5.90 s, Memoria: 7.12 MB

Iteración 4/5
gevent: Tiempo: 0.52 s, Memoria: 10.03 MB
asyncio: Tiempo: 5.93 s, Memoria: 7.12 MB

Iteración 5/5
gevent: Tiempo: 0.50 s, Memoria: 9.99 MB
asyncio: Tiempo: 5.91 s, Memoria: 7.12 MB

Resultados promedio:
gevent: Tiempo: 0.50 s, Memoria: 10.03 MB
asyncio: Tiempo: 5.92 s, Memoria: 7.23 MB
```

Comparación con la expectativa inicial: Se plantea que gevent es más eficiente que asyncio para aplicaciones síncronas en términos de memoria y cambio de contexto. Los resultados de este experimento respaldan parcialmente esta afirmación:

- Cambio de contexto: gevent es claramente más eficiente, con un tiempo de ejecución mucho menor (0.50 s vs. 5.92 s). Esto se debe a que los greenlets permiten cambios de contexto rápidos en el espacio de usuario, mientras que asyncio depende de un thread pool para operaciones síncronas, lo que introduce una sobrecarga significativa.
- Memoria: Contrario a la expectativa, asyncio usa menos memoria (7.23 MB vs. 10.03 MB). Esto sugiere que, en este caso específico, la gestión de corutinas y el thread pool de asyncio son más eficientes en términos de memoria que los greenlets y el monkey patching de gevent. Sin embargo, la diferencia (~2.8 MB) no es tan grande como la diferencia en tiempo de ejecución, y podría estar influenciada por cómo tracemalloc mide la memoria o por optimizaciones específicas del entorno corriendo el test.



```bash title="Salida"
Ejecutando experimento con operaciones síncronas...

Iteración 1/5
gevent: Tiempo: 73.68 s, Memoria: 12.20 MB
asyncio: Tiempo: 5.03 s, Memoria: 4.87 MB

Iteración 2/5
gevent: Tiempo: 7.79 s, Memoria: 1.85 MB
asyncio: Tiempo: 4.98 s, Memoria: 4.78 MB

Iteración 3/5
gevent: Tiempo: 7.51 s, Memoria: 1.72 MB
asyncio: Tiempo: 4.95 s, Memoria: 4.13 MB

Iteración 4/5
gevent: Tiempo: 7.58 s, Memoria: 1.71 MB
asyncio: Tiempo: 5.06 s, Memoria: 4.52 MB

Iteración 5/5
gevent: Tiempo: 7.50 s, Memoria: 1.76 MB
asyncio: Tiempo: 6.17 s, Memoria: 4.68 MB

Resultados promedio:
gevent: Tiempo: 20.81 s, Memoria: 3.85 MB
asyncio: Tiempo: 5.24 s, Memoria: 4.60 MB
```

#### Request hacia un endpoint real ( solo 1000 llamadas )

```bash
gevent: Tiempo: 987.07 s, Memoria: 5.16 MB
asyncio: Tiempo: 4.24 s, Memoria: 2.73 MB

Resultados promedio:
gevent: Tiempo: 947.55 s, Memoria: 4.33 MB
asyncio: Tiempo: 8.06 s, Memoria: 2.97 MB
```

donde algunas corridas fallaron con mensaje similar a
`requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='<URL>', port=443): Read timed out. (read timeout=None)`

### Escalabilidad

- **gevent**: Debido a su modelo de concurrencia basado en greenlets, `gevent` es altamente escalable y puede manejar un gran número de conexiones simultáneas con un uso de memoria relativamente bajo.
- **Flask**: El servidor de desarrollo de Flask no está diseñado para producción y no escala bien para manejar muchas conexiones simultáneas. Para producción, se recomienda usar un servidor WSGI como `gunicorn` con workers o `uWSGI`.
- **asyncio.wsgi**: `asyncio` puede escalar bien para aplicaciones asíncronas, pero requiere que la aplicación esté escrita de manera asíncrona (usando `async/await`). No es tan eficiente como `gevent` para aplicaciones síncronas.

### Compatibilidad con código síncrono

- **gevent**: Una de las mayores ventajas de `gevent` es que puede ejecutar código síncrono existente de manera concurrente sin necesidad de modificarlo. Esto se debe a que `gevent` monkey-patching (parchea) las bibliotecas estándar de Python para hacerlas compatibles con greenlets.
- **Flask**: Flask no hace nada especial para manejar código síncrono de manera concurrente. Si necesitas concurrencia, debes usar un servidor WSGI externo con workers.
- **asyncio.wsgi**: `asyncio` requiere que el código esté escrito de manera asíncrona (usando `async/await`). Si tienes código síncrono, no podrás aprovechar las ventajas de `asyncio` sin modificarlo.

### Monkey-patching

- **gevent**: `gevent` realiza un "monkey-patching" de las bibliotecas estándar de Python (como `socket`, `threading`, etc.) para hacerlas compatibles con greenlets. Esto permite que el código síncrono existente se comporte de manera asíncrona sin cambios.
- **Flask**: No realiza monkey-patching. El código síncrono se ejecuta de manera síncrona.
- **asyncio.wsgi**: No realiza monkey-patching. El código debe ser explícitamente asíncrono.

### Uso en producción

- **gevent**: `gevent` es adecuado para producción, especialmente en escenarios donde se necesitan manejar muchas conexiones simultáneas con un uso eficiente de recursos.
- **Flask**: El servidor de desarrollo de Flask no es adecuado para producción. Se recomienda usar `gunicorn` o `uWSGI` en producción.
- **asyncio.wsgi**: `asyncio` es adecuado para producción, pero requiere que la aplicación esté escrita de manera asíncrona.

### Facilidad de uso

- **gevent**: Es relativamente fácil de usar, especialmente si ya tienes código síncrono que quieres ejecutar de manera concurrente. Sin embargo, el monkey-patching puede introducir complejidad en algunos casos.
- **Flask**: Es muy fácil de usar para aplicaciones pequeñas o medianas, pero requiere configuración adicional para manejar concurrencia en producción.
- **asyncio.wsgi**: Requiere que el código esté escrito de manera asíncrona, lo que puede ser más complejo si no estás familiarizado con `async/await`.


Con todo esto tenemos que **gevent** es ideal para aplicaciones que necesitan manejar muchas conexiones simultáneas con un uso eficiente de recursos, especialmente si ya tienes código síncrono que no quieres modificar, mientras que **Flask** es bueno para aplicaciones pequeñas o medianas, pero requiere un servidor WSGI externo para producción y no escala tan bien como `gevent`, por otro lado, **asyncio.wsgi** es adecuado para aplicaciones asíncronas, pero requiere que el código esté escrito de manera asíncrona.







## Referencias

- [https://dev.to/skywind3000/performance-asyncio-vs-gevent-vs-native-epoll-bnl](https://dev.to/skywind3000/performance-asyncio-vs-gevent-vs-native-epoll-bnl)
