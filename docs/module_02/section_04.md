# Cancelando tasks y configurando timeouts

Las conexiones de red pueden ser poco fiables. La conexión de puede perderse debido a una ralentización de la red, o un servidor puede colapsar y dejar las solicitudes existentes en el limbo.

Al realizar una de estas solicitudes, debemos tener especial cuidado de **NO esperar indefinidamente**.


Cada objeto de tarea tiene un método llamado `cancel`, al que podemos llamar cuando queramos detenerla. Cancelar una tarea hará que esta genere un error `CanceledError` cuando la esperemos, el cual podemos gestionar según sea necesario.


```python title="Ejemplo cancelando un task" linenums="1"
import asyncio
from asyncio import CancelledError
from util import delay

async def main():
    long_task = asyncio.create_task(delay(10))
    seconds_elapsed = 0
    while not long_task.done():
        print('El task no ha terminado, esperaremos un segundo')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()
    try:
        await long_task
    except CancelledError:
        print('Task Cancelado')

asyncio.run(main())
```

```bash title="Salida"
El task 1 no ha terminado, esperaremos un segundo
Task 1 Durmiendo por 10 segundo(s)
El task 1 no ha terminado, esperaremos un segundo
El task 1 no ha terminado, esperaremos un segundo
El task 1 no ha terminado, esperaremos un segundo
El task 1 no ha terminado, esperaremos un segundo
El task 1 no ha terminado, esperaremos un segundo
Task Cancelado
```

## IMPORTANTE

Importante a tener en cuenta sobre la cancelación es que un `CancelledError` solo puede lanzarse desde una instrucción `await`. Esto significa que si llamamos a `cancel` en una tarea cuando está ejecutando código Python simple, este se ejecutará hasta que se complete hasta que lleguemos a la siguiente instrucción `await` (si existe) y se pueda lanzar un `CancelledError`. Llamar a `cancel` no detendrá la tarea por arte de magia; solo la detendrá si se encuentra en un punto de espera o en su próximo punto de espera.


## Configuración de un timeout y cancelando con wait_for

Asyncio proporciona esta funcionalidad mediante la función `asyncio.wait_for`.
Esta función toma una corrutina o un objeto de tarea y un tiempo de espera especificado en segundos, devuelve una corrutina que podemos esperar. Si la tarea tarda más tiempo en completarse que el tiempo de espera asignado, se generará una `TimeoutException`. Una vez alcanzado el límite de tiempo de espera, la tarea se cancelará automáticamente.


```python title="Ejemplo de timeout" linenums="1"
import asyncio
from util import delay

async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('La tarea fue terminada por timeout!')
        print(f'Estatus de la tarea cancelada? {delay_task.cancelled()}')

asyncio.run(main())
```

```bash title="Salida"
Durmiendo por 2 segundo(s)
La tarea fue terminada por timeout!
Estatus de la tarea cancelada? True
```


## Proteger un task de cancelaciones


```python title="Ejemplo de timeout" linenums="1"
import asyncio
from util import delay

async def main():
    task = asyncio.create_task(delay(10, 1))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except TimeoutError:
        print("El task duro más de 5 segundos, pronto terminara!")
        result = await task
        print(result)

asyncio.run(main())
```

Primero creamos una tarea para encapsular nuestra corrutina. Esto difiere del caso anterior enq que accederemos a la tarea en el bloque `except`. Si hubiéramos pasado una corrutina, `wait_for` la habría encapsulado en una tarea, pero no podríamos referenciarla, ya que es interna a la función. Luego, dentro de un bloque `try`, llamamos a `wait_for` y encapsulamos la tarea en `shield`, lo que evitará que se cancele. Dentro de nuestro bloque `except`, imprimimos un mensaje útil al usuario, informándole de que la tarea sigue en ejecución y luego esperamos la tarea que creamos inicialmente.

```bash title="Salida"
Task 1 Durmiendo por 10 segundo(s)
El task duro más de 5 segundos, pronto terminara!
Task 1 Termino la funcion dormir por 10 segundo(s)
10
```

Notemos que aunque regreso el valor de salida ya no se imprimio el mensaje!
