# Como usar el modo debug

Al ejecutar en modo de depuración, veremos algunos mensajes de registro útiles cuando una corrutina o tarea tarde más de 100 milisegundos en ejecutarse. Además, si no esperamos una corrutina, se lanza una excepción para que podamos ver dónde agregar correctamente un tiempo de espera.
Hay diferentes maneras de ejecutar en modo de depuración.

## Usando modo debug

La función `asyncio.run` que hemos estado usando para ejecutar corrutinas expone un parámetro de depuración. Por defecto, está configurado como `False`, pero podemos configurarlo como `True` para habilitar el modo de depuración: `asyncio.run(coroutine(), debug=True)`

## Usando flag

El modo de depuración se puede activar pasando un argumento de línea de comandos al iniciar nuestra aplicación Python. Para ello, aplicamos `-X dev`: `python3 -X dev program.py`

## Usando variables de ambiente


También podemos usar variables de entorno para habilitar el modo de depuración estableciendo la variable `PYTHONASYNCIODEBUG` en 1: `PYTHONASYINCIODEBUG=1 python3 program.py`

```python title="Ejemplo CPU bound" linenums="1"
import asyncio
from util import async_timed

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter

async def main() -> None:
    task_one = asyncio.create_task(cpu_bound_work())
    await task_one

asyncio.run(main(), debug=True)
```

```bash title="Salida"
Empezando función <function cpu_bound_work at 0x74716d411440> con args () {}
La función <function cpu_bound_work at 0x74716d411440> termino en 1.8169 segundo(s)
Executing <Task finished name='Task-2' coro=<cpu_bound_work() done, defined at /home/pepe/CURSOS/asyncio_by_example/src/util/async_timer.py:7> result=100000000 created at /usr/lib/python3.11/asyncio/tasks.py:379> took 1.817 seconds
```

Esto puede ser útil para depurar problemas en los que, sin darnos cuenta, podríamos estar realizando una llamada que esté bloqueando. La configuración predeterminada registrará una advertencia si una corrutina tarda más de 100 milisegundos, pero este tiempo puede ser mayor o menor del deseado. Para cambiar este valor, podemos establecer la duración de la devolución de llamada lenta accediendo al bucle de eventos, estableciendo `slow_callback_duration`. Este es un valor de punto flotante que representa los segundos que queremos que dure la devolución de llamada lenta.


```python title="Ejemplo slow_callback_duration" linenums="1"
import asyncio

async def main():
    loop = asyncio.get_event_loop()
    loop.slow_callback_duration = .250

asyncio.run(main(), debug=True)
```

