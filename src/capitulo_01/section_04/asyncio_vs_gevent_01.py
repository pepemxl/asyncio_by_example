from gevent import monkey
# Parchear bibliotecas estándar para gevent
monkey.patch_all()

import time
import psutil
import os
from contextlib import contextmanager
import gevent
import asyncio


# Función para medir el uso de memoria
def memory_usage():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / 1024 / 1024  # Convertir a MB
    return mem

# Simulación de una operación de E/S (por ejemplo, solicitud HTTP)
def simulate_io_task_gevent(i):
    # Simula una operación de E/S con un pequeño retardo
    gevent.sleep(0.01)  # 10ms de espera para simular E/S
    return i

async def simulate_io_task_asyncio(i):
    # Simula una operación de E/S con un pequeño retardo
    await asyncio.sleep(0.01)  # 10ms de espera para simular E/S
    return i

# Función para ejecutar tareas con gevent
def run_gevent_tasks(num_tasks):
    start_time = time.time()
    start_memory = memory_usage()

    # Crear una lista de tareas
    tasks = [gevent.spawn(simulate_io_task_gevent, i) for i in range(num_tasks)]
    # Ejecutar todas las tareas
    gevent.joinall(tasks)

    end_time = time.time()
    end_memory = memory_usage()

    print(f"gevent: {num_tasks} tareas completadas")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
    print(f"Memoria usada: {end_memory - start_memory:.2f} MB")

# Función para ejecutar tareas con asyncio
async def run_asyncio_tasks(num_tasks):
    start_time = time.time()
    start_memory = memory_usage()

    # Crear una lista de tareas
    tasks = [simulate_io_task_asyncio(i) for i in range(num_tasks)]
    # Ejecutar todas las tareas
    await asyncio.gather(*tasks)

    end_time = time.time()
    end_memory = memory_usage()

    print(f"asyncio: {num_tasks} tareas completadas")
    print(f"Tiempo: {end_time - start_time:.2f} segundos")
    print(f"Memoria usada: {end_memory - start_memory:.2f} MB")

# Ejecutar el experimento
def main():
    num_tasks = 10000  # 10,000 tareas concurrentes

    print("Ejecutando con gevent...")
    run_gevent_tasks(num_tasks)

    print("\nEjecutando con asyncio...")
    asyncio.run(run_asyncio_tasks(num_tasks))

if __name__ == "__main__":
    main()