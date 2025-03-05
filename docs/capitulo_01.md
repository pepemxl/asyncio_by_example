# **¿Qué es asyncio?**

`asyncio` es un módulo de Python que proporciona soporte para la programación asíncrona, permitiendo ejecutar múltiples tareas concurrentemente sin necesidad de usar hilos (`threads`) o procesos múltiples.

`asyncio` es un **framework de programación asíncrona** basado en la ejecución de un **loop de eventos**. Este facilita la ejecución de **código no bloqueante**, lo que significa que una tarea puede avanzar mientras espera que otras terminen.

Este módulo es útil para manejar múltiples tareas de I/O (entrada/salida), como:

- Llamadas a APIs.
- Acceso a bases de datos.
- Lectura y escritura de archivos.
- Servidores web o clientes que manejan muchas conexiones simultáneamente.

## **Beneficios de asyncio**

1. **Eficiencia y Concurrencia**
   - `asyncio` permite manejar miles de conexiones sin necesidad de múltiples hilos o procesos.
   - Evita bloqueos al usar operaciones de I/O asíncronas.
   
2. **Menor Consumo de Recursos**
   - A diferencia de los hilos (`threads`), `asyncio` no requiere cambiar el contexto de ejecución, lo que ahorra memoria y CPU.

3. **Código Más Sencillo y Legible**
   - En comparación con `threading` o `multiprocessing`, `asyncio` permite escribir código secuencial que sigue una lógica más natural.

4. **Ideal para Aplicaciones de Red**
   - Servidores web como **FastAPI** o bibliotecas como **aiohttp** dependen de `asyncio` para manejar muchas solicitudes concurrentes sin bloquear el programa.

### **Ejemplo de asyncio**

Podemos ver como en el siguiente código el tiempo utilizado en la versicón asincrónica es alrededor de 2 segundos, mientras que su version serial le toma alrededor de 4 segundos!

```python
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

```bash
Inicio de tarea
Inicio de tarea
Tarea completada
Tarea completada
Tiempo usado:  2.0031697750091553
```

### **Ejemplo de código sincrónico**

```python
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
