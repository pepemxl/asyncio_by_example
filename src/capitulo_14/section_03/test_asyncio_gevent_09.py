from gevent import monkey
# Parchear las bibliotecas estándar para que sean cooperativas con gevent
monkey.patch_all()
import gevent
import asyncio
from gevent.pool import Pool
from concurrent.futures import ThreadPoolExecutor
import asyncio_gevent
import time


async def tarea_intensiva(id_tarea):
    """Función asíncrona que simula una tarea intensiva."""
    print(f"Tarea {id_tarea} iniciada en greenlet {gevent.getcurrent()}")
    # Usar run_in_executor para ejecutar en el ThreadPoolExecutor
    await asyncio.get_event_loop().run_in_executor(None, time.sleep, 1)
    return f"Resultado de la tarea {id_tarea}"

def tarea_con_trackeo(id_tarea, greenlets_activos, loop):
    """Envolver la tarea asíncrona en un greenlet explícito usando loop.create_task."""
    greenlets_activos.add(gevent.getcurrent())
    # Crear la corrutina y programarla con loop.create_task
    coro = tarea_intensiva(id_tarea)
    task = loop.create_task(coro)
    return task

async def ejecutar_tareas(num_tareas, max_workers, loop):
    """Ejecuta un número dado de tareas con un ThreadPoolExecutor y cuenta los greenlets."""
    # Configurar el ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=max_workers)
    loop.set_default_executor(executor)
    
    greenlets_activos = set()
    
    # Crear un pool de greenlets
    greenlet_pool = Pool()

    # Lanzar tareas en greenlets explícitos, recolectando Tasks
    tasks = []
    greenlets = []
    for i in range(num_tareas):
        greenlet = greenlet_pool.spawn(tarea_con_trackeo, i, greenlets_activos, loop)
        greenlets.append(greenlet)
    
    # Esperar a que los greenlets terminen de crear las tasks
    gevent.joinall(greenlets, timeout=10)

    # Recolectar las Tasks de los greenlets
    for greenlet in greenlets:
        if greenlet.successful():
            tasks.append(greenlet.value)  # Task retornado por create_task

    # Ejecutar todas las tasks en el bucle de eventos
    resultados = await asyncio.gather(*tasks, return_exceptions=True)

    # Reportar cantidad de greenlets creados
    print(f"Número de greenlets creados: {len(greenlets_activos)}")
    print(f"Resultados: {resultados[:5]}...")  # Mostrar primeros 5 resultados para brevidad
    
    # Apagar el executor, esperando a que todas las tareas finalicen
    executor.shutdown(wait=True)
    return len(greenlets_activos)

def testear_configuraciones():
    """Prueba diferentes configuraciones de número de tareas y workers."""
    configuraciones = [
        (5, 2),   # 5 tareas, 2 workers
        (10, 4),  # 10 tareas, 4 workers
        (20, 8),  # 20 tareas, 8 workers
    ]

    # Configurar el bucle de eventos global con asyncio_gevent
    asyncio_gevent_loop = asyncio_gevent.EventLoop()
    asyncio.set_event_loop_policy(asyncio_gevent.EventLoopPolicy())
    asyncio.set_event_loop(asyncio_gevent_loop)

    try:
        for num_tareas, max_workers in configuraciones:
            print(f"\nProbando con {num_tareas} tareas y {max_workers} workers...")
            greenlets_creados = asyncio_gevent_loop.run_until_complete(
                ejecutar_tareas(num_tareas, max_workers, asyncio_gevent_loop)
            )
            print(f"Resumen: {num_tareas} tareas, {max_workers} workers, {greenlets_creados} greenlets")
    finally:
        # Asegurarse de que todas las tareas pendientes estén completadas antes de cerrar
        pending = asyncio.all_tasks(asyncio_gevent_loop)
        if pending:
            asyncio_gevent_loop.run_until_complete(asyncio.wait(pending))
        asyncio_gevent_loop.close()

if __name__ == "__main__":
    # Ejecutar las pruebas
    testear_configuraciones()