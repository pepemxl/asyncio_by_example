import asyncio
import gevent
from gevent import monkey
from concurrent.futures import ThreadPoolExecutor
import asyncio_gevent
import time

# Parchear las bibliotecas estándar para que sean cooperativas con gevent
monkey.patch_all()

# Configurar el bucle de eventos global con asyncio_gevent
asyncio_gevent_loop = asyncio_gevent.EventLoop()
asyncio.set_event_loop_policy(asyncio_gevent.EventLoopPolicy())
asyncio.set_event_loop(asyncio_gevent_loop)

# Configurar el ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=100)
asyncio_gevent_loop.set_default_executor(executor)

async def tarea_intensiva(id_tarea):
    """Función asíncrona que simula una tarea intensiva."""
    print(f"Tarea {id_tarea} iniciada en greenlet {gevent.getcurrent()}")
    # Usar run_in_executor para ejecutar en el ThreadPoolExecutor
    result = await asyncio.get_event_loop().run_in_executor(None, time.sleep, 1)
    return f"Resultado de la tarea {id_tarea}"

async def ejecutar_tareas(num_tareas):
    """Ejecuta un número dado de tareas y cuenta los greenlets generados."""
    greenlets_activos = set()

    async def tarea_con_trackeo(id_tarea):
        greenlets_activos.add(gevent.getcurrent())
        return await tarea_intensiva(id_tarea)

    # Crear tareas asíncronas
    tareas = [tarea_con_trackeo(i) for i in range(num_tareas)]
    
    # Ejecutar todas las tareas
    resultados = await asyncio.gather(*tareas)

    # Reportar cantidad de greenlets creados
    print(f"Número de greenlets creados: {len(greenlets_activos)}")
    print(f"Resultados: {resultados[:5]}...")  # Mostrar primeros 5 resultados para brevidad
    return len(greenlets_activos)

def testear_configuraciones():
    """Prueba diferentes configuraciones de número de tareas."""
    configuraciones = [5, 10, 20]  # Número de tareas a probar

    for num_tareas in configuraciones:
        print(f"\nProbando con {num_tareas} tareas...")
        # Ejecutar en el bucle global
        greenlets_creados = asyncio_gevent_loop.run_until_complete(ejecutar_tareas(num_tareas))
        print(f"Resumen: {num_tareas} tareas, {greenlets_creados} greenlets")

if __name__ == "__main__":
    # Ejecutar las pruebas
    try:
        testear_configuraciones()
    finally:
        # Limpiar recursos
        executor.shutdown()
        asyncio_gevent_loop.close()