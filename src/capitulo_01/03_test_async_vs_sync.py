import asyncio
import time


# Codigo sincronico
def synchronous_task():
    print("Inicio de la tarea sincrónica")
    time.sleep(1)  # Simulamos una operacion que toma 1 segundos
    time.sleep(1)  # Simulamos una operacion que toma 1 segundos
    print("Fin de la tarea sincrónica")


# Codigo asincronico con bloqueo
# async def: Define una función corutina que puede contener await para pausar su ejecución.
async def asynchronous_task():
    print("Inicio de la tarea asincrónica con bloqueo")
    # await: Pausa la ejecución de la corutina hasta que se complete el resultado de otra corutina o tarea.
    await asyncio.sleep(1)  # Simulamos una operacion que toma 1 segundos
    await asyncio.sleep(1)  # Simulamos una operacion que toma 1 segundos
    print("Fin de la tarea asincrónica con bloqueo")


# Codigo asincronico con sin bloqueo
async def asynchronous_task_wb():
    print("Inicio de la tarea asincrónica sin bloqueo")
    asyncio.sleep(1)  # Simulamos una operacion que toma 1 segundos
    asyncio.sleep(1)  # Simulamos una operacion que toma 1 segundos
    print("Fin de la tarea asincrónica sin bloqueo")


def test_01():
    # Ejecucion sincronica
    print("Ejecución sincrónica")
    start = time.time()
    synchronous_task()
    end = time.time()
    print(f"Tiempo de ejecución sincrónica: {end - start} segundos")

    # Ejecucion asincronica con bloqueo
    print("\nEjecución asincrónica")
    start = time.time()
    asyncio.run(asynchronous_task())
    end = time.time()
    print(f"Tiempo de ejecución asincrónica: {end - start} segundos")

    # Ejecucion asincronica sin bloqueo
    print("\nEjecución asincrónica")
    start = time.time()
    asyncio.run(asynchronous_task_wb())
    end = time.time()
    print(f"Tiempo de ejecución asincrónica: {end - start} segundos")


def test_02(n_iterations=10):
    # Ejecucion sincronica
    print("Ejecución sincrónica")
    start = time.time()
    for i in range(n_iterations):
        synchronous_task()
    end = time.time()
    print(f"Tiempo de ejecución sincrónica: {end - start} segundos")

    # Ejecucion asincronica
    print("\nEjecución asincrónica")
    start = time.time()
    for i in range(n_iterations):
        asyncio.run(asynchronous_task())
    end = time.time()
    print(f"Tiempo de ejecución asincrónica: {end - start} segundos")

    # Ejecucion asincronica con sin bloqueo
    print("\nEjecución asincrónica")
    start = time.time()
    tasks = []
    for i in range(n_iterations):
        task = asyncio.create_task(asynchronous_task_wb())
        tasks.append(task)
        asyncio.run(task)
    asyncio.gather(*tasks)
    end = time.time()
    print(f"Tiempo de ejecución asincrónica: {end - start} segundos")


if __name__ == "__main__":
    test_01()
    # test_02()