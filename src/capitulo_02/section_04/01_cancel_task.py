if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from asyncio import CancelledError
from util.delay_functions import delay

async def main():
    long_task = asyncio.create_task(delay(10, 1))
    seconds_elapsed = 0
    while not long_task.done():
        print('El task 1 no ha terminado, esperaremos un segundo')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()
    try:
        await long_task
    except CancelledError:
        print('Task Cancelado')

if __name__ == '__main__':
    asyncio.run(main())