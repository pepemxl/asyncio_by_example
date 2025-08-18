# Ejemplos de Asyncio

## Hello World

Crearemos una corutina que correra de manera asincrona `src/capitulo_01/section_01/intro.py`

```python title="Hello World con Asyncio" linenums="1"
import asyncio

async def greeting_async() -> str:
    """
    Simple ejemplo de función asincrona
    """
    await asyncio.sleep(1)  # Simulamos una tarea asincrona I/O
    return "Hello World!"

async def main() -> None:
    result = await greeting_async()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## **Ejemplo de asyncio vs serial**

Podemos ver como en el siguiente código el tiempo utilizado en la versicón asincrónica es alrededor de 2 segundos, mientras que su version serial le toma alrededor de 4 segundos!

```python title="Ejemplo con Asyncio" linenums="1"
import asyncio
import time


# async def: Define una función asíncrona.
async def tarea():
    print("Inicio de tarea")
    # await asyncio.sleep(2): Suspende la ejecución y permite que otras tareas corran mientras espera.
    await asyncio.sleep(2)  # Simula una operación asíncrona
    print("Tarea completada")

async def main():
    # asyncio.gather(): Ejecuta múltiples tareas en paralelo.
    await asyncio.gather(tarea(), tarea())  # Ejecuta dos tareas en paralelo


if __name__ == '__main__':
    start = time.time()
    # asyncio.run(main()): Inicia el loop de eventos.
    asyncio.run(main())
    end = time.time()
    print("Tiempo usado: ", end-start)
```

#### Salida

```bash title="Salida"
Inicio de tarea
Inicio de tarea
Tarea completada
Tarea completada
Tiempo usado:  2.0031697750091553
```

### **Ejemplo de código sincrónico**

```python title="Ejemplo sincrónico" linenums="1"
import time


def tarea():
    print("Inicio de tarea")
    time.sleep(2)
    print("Tarea completada")

def main():
    tarea()
    tarea()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Tiempo usado: ", end-start)
```

#### Salida

```bash
Inicio de tarea
Tarea completada
Inicio de tarea
Tarea completada
Tiempo usado:  4.004451036453247
```


A alto nivel asyncio proporciona APIs para trabajar con **coroutines** y **tasks**.

## Coroutines

Las Coroutines se declaran con la sintaxis async/await.

Por ejemplo, el siguiente fragmento de código imprime `hola`, espera 1 segundo y luego imprime `mundo`:

```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')
```

Para correr esta corrutina usamos

```python
asyncio.run(main())
```