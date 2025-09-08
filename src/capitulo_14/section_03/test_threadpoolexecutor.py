import gevent
from gevent import monkey
from concurrent.futures import ThreadPoolExecutor
import time
from gevent.pool import Pool

# Parchear las bibliotecas estándar para que sean cooperativas con gevent
monkey.patch_all()

def tarea_intensiva(id_tarea):
    """Función que simula una tarea intensiva en CPU."""
    print(f"Tarea {id_tarea} iniciada en greenlet {gevent.getcurrent()}")
    time.sleep(1)  # Simula trabajo intensivo
    return f"Resultado de la tarea {id_tarea}"

def ejecutar_con_gevent_y_threadpool(num_tareas, max_workers):
    """Ejecuta tareas usando gevent y ThreadPoolExecutor, contando greenlets."""
    # Crear un pool de greenlets
    greenlet_pool = Pool()

    # Contador de greenlets activos
    greenlets_activos = []

    # Crear ThreadPoolExecutor con número de workers especificado
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Función para envolver la tarea y trackear greenlets
        def tarea_en_greenlet(id_tarea):
            greenlets_activos.append(gevent.getcurrent())
            result = executor.submit(tarea_intensiva, id_tarea).result()
            return result

        # Lanzar tareas en el pool de greenlets
        trabajos = [greenlet_pool.spawn(tarea_en_greenlet, i) for i in range(num_tareas)]

        # Esperar a que todas las tareas finalicen
        gevent.joinall(trabajos)

        # Obtener resultados
        resultados = [job.get() for job in trabajos]

    # Reportar cantidad de greenlets creados
    print(f"Número de greenlets creados: {len(greenlets_activos)}")
    print(f"Resultados: {resultados}")
    return len(greenlets_activos)

def testear_configuraciones():
    """Prueba diferentes configuraciones de tareas y workers."""
    configuraciones = [
        (5, 2),   # 5 tareas, 2 workers
        (10, 4),  # 10 tareas, 4 workers
        (20, 8),  # 20 tareas, 8 workers
    ]

    for num_tareas, max_workers in configuraciones:
        print(f"\nProbando con {num_tareas} tareas y {max_workers} workers...")
        greenlets_creados = ejecutar_con_gevent_y_threadpool(num_tareas, max_workers)
        print(f"Resumen: {num_tareas} tareas, {max_workers} workers, {greenlets_creados} greenlets")

if __name__ == "__main__":
    # Ejecutar las pruebas
    testear_configuraciones()