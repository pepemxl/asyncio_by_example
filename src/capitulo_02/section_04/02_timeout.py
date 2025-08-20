if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from asyncio import CancelledError
from util.delay_functions import delay

async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('La tarea fue terminada por timeout!')
        print(f'Estatus de la tarea cancelada? {delay_task.cancelled()}')

if __name__ == '__main__':
    asyncio.run(main())