# Ejecutando concurrencia con tasks

Vimos que al llamar directamente a una corrutina, no la ponemos en el bucle de eventos para su ejecución.

Y obtuvimos un mensaje parecido al siguiente:

```bash
sys:1: RuntimeWarning: coroutine 'coroutine_add_one' was never awaited
```

En lugar de ejecutarlo obtuvimos un objeto de corrutina que luego debemos usar la palabra clave `await` o pasarlo a `asyncio.run` para ejecutarlo y obtener un valor. 

Para ejecutar corrutinas simultáneamente, necesitaremos introducir tareas(`tasks`). Las tareas son envoltorios de una corrutina que programan su ejecución en el bucle de eventos lo antes posible. Esta programación y ejecución se realizan de forma no bloqueante, lo que significa que, una vez creada una tarea, podemos ejecutar otro código al instante mientras la tarea se está ejecutando. Esto contrasta con el uso de la palabra clave `await`, que actúa de forma bloqueante, lo que significa que pausamos toda la corrutina hasta que se devuelva el resultado de la expresión `await`. El hecho de que podamos crear tareas y programarlas para que se ejecuten instantáneamente en el bucle de eventos significa que podemos ejecutar varias tareas prácticamente al mismo tiempo. Cuando estas tareas finalizan una operación de larga duración, cualquier espera que realicen ocurrirá simultáneamente. 

Para mostrar esto, crearemos dos tareas e intentemos ejecutarlas simultáneamente.

Primero para correr un task usamos la instrucción `asyncio.create_task`.

```python title="Ejemplo asyncio sleep" linenums="1"
import asyncio
from util import delay

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)

asyncio.run(main())
```

```bash title="Salida"
<class '_asyncio.Task'>
Durmiendo por 3 segundo(s)
Termino la funcion dormir por 3 segundo(s)
3
```

El uso de "await" en las tareas de nuestra aplicación también tiene implicaciones en la gestión de las excepciones.


## Correr multiples tasks concurrentemente

Dado que las tareas se crean instantáneamente y se programan para ejecutarse lo antes posible, esto nos permite ejecutar varias tareas de larga duración simultáneamente. Podemos lograrlo iniciando secuencialmente varias tareas con nuestra corrutina de larga duración.



```python title="Ejemplo asyncio sleep" linenums="1"
import asyncio
from util import delay

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))
    await sleep_for_three
    await sleep_again
    await sleep_once_more

asyncio.run(main())
```

```bash title="Salida"
1 Durmiendo por 3 segundo(s)
2 Durmiendo por 3 segundo(s)
3 Durmiendo por 3 segundo(s)
1 Termino la funcion dormir por 3 segundo(s)
2 Termino la funcion dormir por 3 segundo(s)
3 Termino la funcion dormir por 3 segundo(s)
```

En el listado anterior, iniciamos tres tareas, cada una de las cuales tarda 3 segundos en completarse. 
Cada llamada a `create_task` regresa instantáneamente, por lo que llegamos a la instrucción `await sleep_for_three` inmediatamente. 

Al haber llegado a `await sleep_for_three`, las tres tareas comienzan a ejecutarse y realizarán cualquier operación de suspensión simultáneamente. Esto significa que el programa se completará en aproximadamente 3 segundos.


TODO: Crear diagrama secuencial donde se muestre como  se realizan las pausas y se realiza el switch de de run a correr otras tareas.


```python title="Corriendo mientras otras tareas se terminan" linenums="1"
import asyncio
from util import delay

async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("Yo me ejecuto mientras otro codigo esta siendo ejecutado")

async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay
```


```bash title="Salida"
Task 1 Durmiendo por 3 segundo(s)
Task 2 Durmiendo por 3 segundo(s)
Yo me ejecuto mientras otro codigo esta siendo ejecutado
Yo me ejecuto mientras otro codigo esta siendo ejecutado
Task 1 Termino la funcion dormir por 3 segundo(s)
Task 2 Termino la funcion dormir por 3 segundo(s)
```