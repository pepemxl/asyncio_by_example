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