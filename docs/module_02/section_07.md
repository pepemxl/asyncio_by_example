# Pitfalls de corutinas y tareas


Al observar las mejoras de rendimiento que podemos obtener al ejecutar algunas de nuestras tareas más largas simultáneamente, podemos sentirnos tentados a usar corrutinas y tareas en todas nuestras aplicaciones. Si bien esto depende de la aplicación que se esté desarrollando, simplemente marcar las funciones como asíncronas y encapsularlas en tareas puede no mejorar el rendimiento de la aplicación. En ciertos casos, esto puede degradar el rendimiento de las aplicaciones. (Ojo mucho ojo!)

Se producen dos errores principales al intentar convertir las aplicaciones en asíncronas. El primero es intentar ejecutar código limitado por la CPU en tareas o corrutinas sin usar multiprocesamiento; el segundo es usar API bloqueantes de E/S sin usar multihilo.

Podemos tener funciones que realizan cálculos computacionalmente costosos, como recorrer un diccionario grande o realizar un cálculo matemático. Si tenemos varias de estas funciones con el potencial de ejecutarse simultáneamente, podemos considerar ejecutarlas en tareas separadas. 

En teoría, esto es era una buena idea, pero recordemos que asyncio tiene un modelo de concurrencia de **UN solo hilo**. Esto significa que aún estamos sujetos a las limitaciones de un solo hilo y del bloqueo global del intérprete.


## Ejemplo con un task CPU Bound

El siguiente ejemplo son dos tasks que son CPU bound dentro de una corutina.

```python title="Ejemplo CPU Bound" linenums="1"
import asyncio
from util import delay

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await task_one
    await task_two

asyncio.run(main())
```

Como era de esperarse el tiempo de realizar ambas tareas es el mismo que de haber hecho esta tarea de manera serial.

```bash title="Salida"
Empezando función <function main at 0x712866d6f1a0> con args () {}
Empezando función <function cpu_bound_work at 0x7128676d1440> con args () {}
La función <function cpu_bound_work at 0x7128676d1440> termino en 1.7814 segundo(s)
Empezando función <function cpu_bound_work at 0x7128676d1440> con args () {}
La función <function cpu_bound_work at 0x7128676d1440> termino en 1.7840 segundo(s)
La función <function main at 0x712866d6f1a0> termino en 3.5657 segundo(s)s
```


Podríamos pensar que no hay inconvenientes en usar `async` y `await` en todo nuestro código. Al fin y al cabo, tarda el mismo tiempo que si lo hubiéramos ejecutado secuencialmente. Sin embargo, al hacerlo, podemos encontrarnos con situaciones en las que el rendimiento de nuestra aplicación se vea afectado. Esto es especialmente cierto cuando tenemos otras corrutinas o tareas con expresiones `await`. 
Consideremos la posibilidad de crear dos tareas limitadas por la CPU junto con una tarea de larga duración, como nuestra corrutina de retardo.


## Ejemplo mezclando CPU bound task con I/O Bound task

```python title="Ejemplo CPU Bound + I/O Bound" linenums="1"
import asyncio
from util import async_timed, delay

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))
    await task_one
    await task_two
    await delay_task
```

```bash title="Salida"
Empezando función <function main at 0x75abfc86f240> con args () {}
Empezando función <function cpu_bound_work at 0x75abfd1b1440> con args () {}
La función <function cpu_bound_work at 0x75abfd1b1440> termino en 1.7838 segundo(s)
Empezando función <function cpu_bound_work at 0x75abfd1b1440> con args () {}
La función <function cpu_bound_work at 0x75abfd1b1440> termino en 1.7702 segundo(s)
Durmiendo por 4 segundo(s)
Termino la funcion dormir por 4 segundo(s)
La función <function main at 0x75abfc86f240> termino en 7.5586 segundo(s)
```

## Ejemplo mezclado CPU bound tasj con I/O bound task donde el orden importa

Pequeñas variaciones del codigo pueden provocar comportamientos distintos

```python title="Ejemplo" linenums="1"
import asyncio
from util import async_timed, delay

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter

@async_timed()
async def main():
    delay_task = asyncio.create_task(delay(4))
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await delay_task
    await task_one
    await task_two
```


```bash title="Salida"
Empezando función <function main at 0x7afa8c373240> con args () {}
Durmiendo por 4 segundo(s)
Empezando función <function cpu_bound_work at 0x7afa8ccd5440> con args () {}
La función <function cpu_bound_work at 0x7afa8ccd5440> termino en 1.7641 segundo(s)
Empezando función <function cpu_bound_work at 0x7afa8ccd5440> con args () {}
La función <function cpu_bound_work at 0x7afa8ccd5440> termino en 1.7755 segundo(s)
Termino la funcion dormir por 4 segundo(s)
La función <function main at 0x7afa8c373240> termino en 4.0028 segundo(s)
```

Este ejemplo muestra como la creación del task literalmente afecta el comportamiento.
Donde haber encolado la tarea que es I/O nos ayudo realmente a empezar a trabajar dicha tarea, y para cuando acabaron las tareas CPU bound dicha tarea termino.


## Ejemplo con librerias bloqueantes

También podríamos vernos tentados a usar nuestras bibliotecas existentes para operaciones de E/S envolviéndolas en corrutinas. Sin embargo, esto generará los mismos problemas que vimos con las operaciones de CPU. Estas API bloquean el hilo principal. Por lo tanto, al ejecutar una llamada a la API de bloqueo dentro de una corrutina, bloqueamos el propio hilo del bucle de eventos, lo que significa que detenemos la ejecución de otras corrutinas o tareas.


```python title="Ejemplo con librerias bloqueantes" linenums="1"
import asyncio
import requests
from util.async_timer import async_timed

@async_timed()
async def get_example_status() -> int:
    return requests.get('http://www.google.com').status_code

@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())
    await task_1
    await task_2
    await task_3

if __name__ == '__main__':
    asyncio.run(main())
```

```bash title="Salida"
Empezando función <function main at 0x735c060965c0> con args () {}
Empezando función <function get_example_status at 0x735c06f5c540> con args () {}
La función <function get_example_status at 0x735c06f5c540> termino en 0.1208 segundo(s)
Empezando función <function get_example_status at 0x735c06f5c540> con args () {}
La función <function get_example_status at 0x735c06f5c540> termino en 0.1015 segundo(s)
Empezando función <function get_example_status at 0x735c06f5c540> con args () {}
La función <function get_example_status at 0x735c06f5c540> termino en 0.1029 segundo(s)
La función <function main at 0x735c060965c0> termino en 0.3255 segundo(s)
```

No obtuvimos ninguna ventaja de la concurrencia!


## Ejemplo de CPU bound a I/O bound

se nos podría ocurrir la siguiente idea, por que no volver cooperativa una tarea CPU bound.

```python title="Ejemplo con sync timer" linenums="1"
import asyncio
from util.async_timer import async_timed


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter

@async_timed()
async def cpu_bound_work_awaitable() -> int:
    counter = 0
    async def add_counter():
        nonlocal counter
        counter = counter + 1
    for i in range(100000000):
        await add_counter()
    return counter

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work_awaitable())
    await task_one
    await task_two


if __name__ == '__main__':
    asyncio.run(main())
```

```bash title="Salida"
Empezando función <function main at 0x71ecec173380> con args () {}
Empezando función <function cpu_bound_work at 0x71ececaf5440> con args () {}
La función <function cpu_bound_work at 0x71ececaf5440> termino en 1.9740 segundo(s)
Empezando función <function cpu_bound_work_awaitable at 0x71ecec173240> con args () {}
La función <function cpu_bound_work_awaitable at 0x71ecec173240> termino en 9.7383 segundo(s)
La función <function main at 0x71ecec173380> termino en 11.7125 segundo(s)
```

Como podemos ver volver esperable una tarea CPU bound se volvio contraproducente, incrementando el tiempo de aproximadamente 2 segundos a casi 12 segundos para la misma tarea!


## Ejemplo con un timer sync

### Task I/O bound con tiempo mayor al Task CPU bound


```python title="Ejemplo con sync timer" linenums="1"
import asyncio
from util.async_timer import async_timed
from util.delay_functions import delay
from util.sync_timed import sync_timed

@async_timed()
async def cpu_bound_work(task_id) -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


async def test_01() -> None:
    print("---Empezando test 01---")
    task_one = asyncio.create_task(cpu_bound_work(task_id=1))
    await task_one
    print("-----------------------")

async def test_02() -> None:
    print("Empezando test 02")
    task_delay = asyncio.create_task(delay(5,1))
    task_one = asyncio.create_task(cpu_bound_work(task_id=2))
    task_two = asyncio.create_task(cpu_bound_work(task_id=3))
    await task_one
    await task_two
    await task_delay
    print("-----------------------")

async def test_03() -> None:
    print("Empezando test 03")
    task_one = asyncio.create_task(cpu_bound_work(task_id=1))
    task_two = asyncio.create_task(cpu_bound_work(task_id=2))
    task_delay = asyncio.create_task(delay(5,3))
    await task_one
    await task_two
    await task_delay
    print("-----------------------")

@sync_timed()
def main() -> None:
    asyncio.run(test_01())
    asyncio.run(test_02())
    asyncio.run(test_03())


if __name__ == '__main__':
    main()
```

```bash title="Salida"
Empezando función sincrona <function main at 0x7e478686b560> con args () {}
---Empezando test 01---
Empezando función <function cpu_bound_work at 0x7e4786830fe0> con args () {'task_id': 1}
La función <function cpu_bound_work at 0x7e4786830fe0> termino en 1.8737 segundo(s)
-----------------------
Empezando test 02
Task 1 Durmiendo por 5 segundo(s)
Empezando función <function cpu_bound_work at 0x7e4786830fe0> con args () {'task_id': 2}
La función <function cpu_bound_work at 0x7e4786830fe0> termino en 1.8369 segundo(s)
Empezando función <function cpu_bound_work at 0x7e4786830fe0> con args () {'task_id': 3}
La función <function cpu_bound_work at 0x7e4786830fe0> termino en 1.8190 segundo(s)
Task 1 Termino la funcion dormir por 5 segundo(s)
-----------------------
Empezando test 03
Empezando función <function cpu_bound_work at 0x7e4786830fe0> con args () {'task_id': 1}
La función <function cpu_bound_work at 0x7e4786830fe0> termino en 1.7980 segundo(s)
Empezando función <function cpu_bound_work at 0x7e4786830fe0> con args () {'task_id': 2}
La función <function cpu_bound_work at 0x7e4786830fe0> termino en 1.7814 segundo(s)
Task 3 Durmiendo por 5 segundo(s)
Task 3 Termino la funcion dormir por 5 segundo(s)
-----------------------
La función sincrona <function main at 0x7e478686b560> termino en 15.4637 segundo(s)
```

### Task I/O bound con tiempo similar a Task CPU bound

Ahora reduzcamos el tiempo de ejecución de delay a 2 segundos que es approximadamente lo que tarda la tarea `cpu_bound`.

Con ello obtenemos la siguiente salida

```bash title="Ejemplo cambiando a 2 segundos"
Empezando función sincrona <function main at 0x7997b8663560> con args () {}
---Empezando test 01---
Empezando función <function cpu_bound_work at 0x7997b8628fe0> con args () {'task_id': 1}
La función <function cpu_bound_work at 0x7997b8628fe0> termino en 1.8079 segundo(s)
-----------------------
Empezando test 02
Task 1 Durmiendo por 2 segundo(s)
Empezando función <function cpu_bound_work at 0x7997b8628fe0> con args () {'task_id': 2}
La función <function cpu_bound_work at 0x7997b8628fe0> termino en 1.8219 segundo(s)
Empezando función <function cpu_bound_work at 0x7997b8628fe0> con args () {'task_id': 3}
La función <function cpu_bound_work at 0x7997b8628fe0> termino en 1.8353 segundo(s)
Task 1 Termino la funcion dormir por 2 segundo(s)
-----------------------
Empezando test 03
Empezando función <function cpu_bound_work at 0x7997b8628fe0> con args () {'task_id': 1}
La función <function cpu_bound_work at 0x7997b8628fe0> termino en 1.8370 segundo(s)
Empezando función <function cpu_bound_work at 0x7997b8628fe0> con args () {'task_id': 2}
La función <function cpu_bound_work at 0x7997b8628fe0> termino en 1.8337 segundo(s)
Task 3 Durmiendo por 2 segundo(s)
Task 3 Termino la funcion dormir por 2 segundo(s)
-----------------------
La función sincrona <function main at 0x7997b8663560> termino en 11.1424 segundo(s)
```

Si las tareas fueran cooperativas las tres tareas tomarian alrededor de 6 segundos. Sin embargo, 
estan tomando 11 segundos.



