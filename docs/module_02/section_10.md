# Funciones más comunes en asyncio

- `run()`: Crea un bucle de eventos, ejecuta una corrutina y lo cierra.
- `Runner`: Un gestor de contexto que simplifica múltiples llamadas a funciones asíncronas.
- `Task`: Objeto de tarea.
- `TaskGroup`: Un gestor de contexto que contiene un grupo de tareas y permite esperar a que todas finalicen.
- `create_task()`: Inicia una tarea asíncrona y la devuelve.
- `current_task()`: Devuelve la tarea actual.
- `all_tasks()`: Devuelve todas las tareas sin terminar de un bucle de eventos.
- `await sleep()`: Suspender durante unos segundos.
- `await gathering()`: Programar y esperar tareas simultáneamente.
- `await wait_for()`: Ejecutar con tiempo de espera.
- `await shield()`: Proteger contra cancelación.
- `await wait()`: Monitorizar la finalización.
- `timeout()`: Ejecutar con tiempo de espera.
- `to_thread()`: Ejecutar una función asíncronamente en un hilo independiente del sistema operativo.
- `run_coroutine_threadsafe()`: Programar una corrutina desde otro hilo del sistema operativo. for in as_completed(): supervisa la finalización con un bucle for.

## Modo de depuración

Se habilita estableciendo `PYTHONASYNCIODEBUG=1`, usando el modo de desarrollo de Python, pasando `debug=True` a `asyncio.run()` o llamando a `loop.set_debug()`.

Hay que configurar el nivel del logger en `logging.DEBUG`.

Para mostrar las advertencias de `ResourceWarning` con la opción `-W`.



