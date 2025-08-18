# Básicos Asyncio

## Introducción a Corutinas

Las corutinas nos permiten ejecutar varias operaciones que consumen mucho tiempo simultáneamente, lo que bien utilizado mejora considerablemente el rendimiento de nuestras aplicaciones.

Para crear y pausar una corrutina, usamos la palabra clave `async` y `await` de Python. 

La palabra clave `async` nos permite definir una corrutina; mientras que la palabra clave `await` nos permite pausarla cuando tengamos una operación de larga duración.


```python title="Definición de un corutina"
async def my_coroutine() -> None:
    print("Hello World")
```

```python title="Comparación de async vs sync" linenums="1"
async def coroutine_add_one(number: int) -> int:
    return number + 1

def add_one(number: int) -> int:
    return number + 1

function_result = add_one(1)
coroutine_result = coroutine_add_one(1)

print(f"El resultado serial es {function_result} y su tipo es {type(function_result)}")
print(f"El resultado de la corutina es {coroutine_result} y su tipo es {type(coroutine_result)}")
```

```bash title="Salida" hl_lines="3"
El resultado serial es 2 y su tipo es <class 'int'>
El resultado de la corutina es <coroutine object coroutine_add_one at 0x76f7f8f362c0> y su tipo es <class 'coroutine'>
sys:1: RuntimeWarning: coroutine 'coroutine_add_one' was never awaited # (warning)
```

Observemos cómo, al llamar a nuestra función normal `add_one`, esta se ejecuta inmediatamente y devuelve lo que esperaríamos: otro entero. Sin embargo, al llamar a `coroutine_add_one`, el código de la corrutina no se ejecuta. En su lugar, se obtiene un objeto de corrutina.

Y tenemos una advertencia que que nunca fue esperada la función `coroutine_add_one`.

Este punto es importante, ya que las corrutinas no se ejecutan al llamarlas directamente. En su lugar, se crea un objeto de corrutina que puede ejecutarse posteriormente. Para ejecutar una corrutina, debemos ejecutarla explícitamente en un bucle de eventos. 



```python title="Ejecutando una corutina" linenums="1"
import asyncio

async def coroutine_add_one(number: int) -> int:
    return number + 1

coroutine_result = asyncio.run(coroutine_add_one(1))
print(f"El resultado de la corutina es {coroutine_result} y su tipo es {type(coroutine_result)}")
```

```bash title="Salida"
El resultado de la corutina es 2 y su tipo es <class 'int'>
```


`asyncio.run` ejecuto nuestra corutina en un event loop.

1. Crea un nuevo event loop, 
2. una vez creado, toma cualquier corutina pendiente y la ejecuta
3. se realizan algunas taras de limpieza relacionadas
4. apaga y cierra el event loop


## Pausar tareas con await

El ejemplo que vimos arriba no necesitaba ser una corrutina, ya que solo ejecutaba código Python no bloqueante. La ventaja de asyncio es poder pausar la ejecución para que el bucle de eventos ejecute otras tareas durante una operación de larga duración. 

Para pausar la ejecución, usamos la palabra clave `await`. Esta palabra clave suele ir seguida de una llamada a una corrutina, específicamente, un objeto conocido como `awaitable`, que no siempre es una corrutina. 

Usar la palabra clave `await` hará que se ejecute la corrutina que le sigue, a diferencia de llamar directamente a una corrutina, que produce un objeto de corrutina. La expresión `await` también pausará la corrutina que la contiene hasta que la corrutina que esperábamos finalice y devuelva un resultado.

Cuando la corrutina que esperábamos finalice, tendremos acceso al resultado que devolvió, y la corrutina que la contiene se activará para procesar el resultado. Podemos usar la palabra clave `await` antes de una llamada a una corrutina. Ampliando nuestro programa anterior, podemos escribir un programa donde llamamos a la función `add_one` dentro de una función asíncrona `main` y obtenemos el resultado.


```python title="Ejemplo de await" linenums="1"
import asyncio

async def add_one(number: int) -> int:
    return number + 1

async def main() -> None:
    one_plus_one = await add_one(1)
    two_plus_one = await add_one(2)
    print(f"Resultado de one_plus_one es: {one_plus_one}")
    print(f"Resultado de two_plus_one es: {two_plus_one}")

asyncio.run(main())
```

```bash title="Salida"
Resultado de one_plus_one es: 2
Resultado de two_plus_one es: 3
```

Primero esperamos la llamada a `add_one(1)`. Una vez obtenido el resultado, se reanudará la función principal y asignaremos el valor de retorno de `add_one(1)` a la variable `one_plus_one`, que en este caso será dos. Luego, hacemos lo mismo con `add_one(2)` e imprimimos los resultados.








