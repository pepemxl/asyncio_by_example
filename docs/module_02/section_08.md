# Accesando y manejando manualment el event loop


## Como crear un event loop manualmente

Podemos crear un bucle de eventos usando el método `asyncio.new_event_loop`. Esto devolverá una instancia del bucle de eventos. Con esto, tenemos acceso a todos los métodos de bajo nivel que ofrece el bucle de eventos. Con el bucle de eventos, tenemos acceso a un método llamado `run_until_complete`, que toma una corrutina y la ejecuta hasta su finalización. Una vez finalizado el bucle de eventos, debemos cerrarlo para liberar los recursos que estaba utilizando. Esto normalmente debería estar en un bloque `finally` para que las excepciones lanzadas no nos impidan cerrar el bucle. Usando estos conceptos, podemos crear un bucle y ejecutar una aplicación asyncio.


```python title="Crear event loop manualmente" linenums="1"
import asyncio

async def main():
    await asyncio.sleep(1)

def create_event_loop():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

if __name__ == '__main__':
    create_event_loop()
```

## Accesando un event loop

```python title="Accesando event loop manualmente" linenums="1"
import asyncio
from util.delay_functions import delay

def call_later():
    print("Esta función será llamada después")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

if __name__ == '__main__':
    asyncio.run(main())
```

```bash title="Salida"
Durmiendo por 1 segundo(s)
Esta función será llamada después
Termino la funcion dormir por 1 segundo(s)
```

La corrutina principal obtiene el bucle de eventos con `asyncio.get_running_loop` y le indica que ejecute `call_later`, que toma una función y la ejecutará en la siguiente iteración del bucle de eventos. 



