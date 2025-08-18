# Introducción a corutinas que corren durante mucho tiempo con sleep

Los ejemplos anteriores no usaron operaciones lentas y nos ayudaron a aprender la sintaxis básica de las corrutinas. Para comprender plenamente los beneficios y mostrar cómo podemos ejecutar varios eventos simultáneamente, introduciremos algunas operaciones de larga duración. En lugar de realizar consultas a la API web o a la base de datos directamente, cuya duración no es determinista, simularemos operaciones de larga duración especificando el tiempo de espera. Para ello, utilizaremos la función `asyncio.sleep`.


Podemos usar `asyncio.sleep` para que una corrutina se suspenda durante un número determinado de segundos.
Esto pausará nuestra corrutina durante el tiempo que le demos, simulando lo que sucedería si tuviéramos una llamada de larga duración a una base de datos o API web.

`asyncio.sleep` es en sí misma una corrutina, por lo que debemos usarla con la palabra clave `await`. Si la llamamos por sí sola, obtendremos un objeto de corrutina. Dado que `asyncio.sleep` es una corrutina,
esto significa que cuando una corrutina la espera, otro código podrá ejecutarse.

```python title="Ejemplo asyncio sleep" linenums="1"
import asyncio

async def hello_world_message() -> str:
    await asyncio.sleep(1)
    return 'Hello World'

async def main() -> None:
    print("Empezo  la función main")
    message = await hello_world_message()
    print(message)

asyncio.run(main())
```

Al ejecutar este código es claro que paso algún tiempo entre el primer mensaje y el mensaje `Hello World`.


Podemos crear una función delay

```python title="Delay" linenums="1"
import asyncio

async def delay(delay_seconds: int) -> int:
    print(f'Durmiendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    print(f'Termino la funcion dormir por {delay_seconds} segundo(s)')
    return delay_seconds
```
