# Midiendo el tiempo de ejecución de Corutinas


```python title="Ejemplo" linenums="1"
import asyncio
import time

async def main():
    start = time.time()
    await asyncio.sleep(1)
    end = time.time()
    print(f'Dormir tomo {end - start} segundos')

asyncio.run(main())
```

```bash title="Salida"
Dormir tomo 1.001190423965454 segundos
```

La mejor manera de medir el tiempo de las corutinas sera usandod decoradores.


```python title="Decorador" linenums="1"
import functools
import time
from typing import Callable, Any

def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Empezando función {func} con args {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'La función {func} termino en {total:.4f} segundo(s)')
        return wrapped
    return wrapper
```





```python title="Decorador" linenums="1"
import asyncio

@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'Durmniendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    print(f'Termino de dormir en {delay_seconds} segundo(s)')
    return delay_seconds

@async_timed()
async def main():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))
    await task_one
    await task_two

asyncio.run(main())
```

```bash title="Salida"
Empezando función <function main at 0x76bafa82f2e0> con args () {}
Empezando función <function delay at 0x76bafb211440> con args (2,) {}
Durmniendo por 2 segundo(s)
Empezando función <function delay at 0x76bafb211440> con args (3,) {}
Durmniendo por 3 segundo(s)
Termino de dormir en 2 segundo(s)
La función <function delay at 0x76bafb211440> termino en 2.0024 segundo(s)
Termino de dormir en 3 segundo(s)
La función <function delay at 0x76bafb211440> termino en 3.0016 segundo(s)
La función <function main at 0x76bafa82f2e0> termino en 3.0018 segundo(s)
```

Podemos ver que nuestras dos llamadas de retardo se iniciaron y finalizaron en aproximadamente 2 y 3 segundos, respectivamente, para un total de 5 segundos. Sin embargo, observe que nuestra corrutina principal solo tardó 3 segundos en completarse porque estuvimos esperando simultáneamente.

