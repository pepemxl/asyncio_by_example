from gevent import monkey
# Parchear bibliotecas estándar para gevent
monkey.patch_all()

import time
import tracemalloc
import gevent
import asyncio
import statistics


# Simulación de una operación síncrona bloqueante
def simulate_blocking_task_gevent(i):
    time.sleep(0.01)  # Operación síncrona parcheada por gevent
    return i

async def simulate_blocking_task_asyncio(i):
    # En asyncio, necesitamos usar un executor para operaciones síncronas
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, time.sleep, 0.01)
    return i

# Función para ejecutar tareas con gevent
def run_gevent_tasks(num_tasks):
    tracemalloc.start()
    start_time = time.time()
    start_memory, _ = tracemalloc.get_traced_memory()

    tasks = [gevent.spawn(simulate_blocking_task_gevent, i) for i in range(num_tasks)]
    gevent.joinall(tasks)

    end_time = time.time()
    end_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end_time - start_time, (end_memory - start_memory) / 1024 / 1024

# Función para ejecutar tareas con asyncio
async def run_asyncio_tasks(num_tasks):
    tracemalloc.start()
    start_time = time.time()
    start_memory, _ = tracemalloc.get_traced_memory()

    tasks = [simulate_blocking_task_asyncio(i) for i in range(num_tasks)]
    await asyncio.gather(*tasks)

    end_time = time.time()
    end_memory, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end_time - start_time, (end_memory - start_memory) / 1024 / 1024

# Ejecutar el experimento varias veces
def main():
    num_tasks = 10000
    num_runs = 5
    gevent_times = []
    gevent_memories = []
    asyncio_times = []
    asyncio_memories = []

    print("Ejecutando experimento con operaciones síncronas...")
    for i in range(num_runs):
        print(f"\nIteración {i+1}/{num_runs}")
        
        # gevent
        time_taken, memory_used = run_gevent_tasks(num_tasks)
        gevent_times.append(time_taken)
        gevent_memories.append(memory_used)
        print(f"gevent: Tiempo: {time_taken:.2f} s, Memoria: {memory_used:.2f} MB")

        # asyncio
        time_taken, memory_used = asyncio.run(run_asyncio_tasks(num_tasks))
        asyncio_times.append(time_taken)
        asyncio_memories.append(memory_used)
        print(f"asyncio: Tiempo: {time_taken:.2f} s, Memoria: {memory_used:.2f} MB")

    # Promedios
    print("\nResultados promedio:")
    print(f"gevent: Tiempo: {statistics.mean(gevent_times):.2f} s, Memoria: {statistics.mean(gevent_memories):.2f} MB")
    print(f"asyncio: Tiempo: {statistics.mean(asyncio_times):.2f} s, Memoria: {statistics.mean(asyncio_memories):.2f} MB")

if __name__ == "__main__":
    main()