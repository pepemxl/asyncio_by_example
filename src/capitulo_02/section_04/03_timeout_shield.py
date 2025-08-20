if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from asyncio import CancelledError
from util.delay_functions import delay

async def main():
    task = asyncio.create_task(delay(10, 1))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except TimeoutError:
        print("El task duro más de 5 segundos, pronto terminara!")
        result = await task
        print(result)

if __name__ == '__main__':
    asyncio.run(main())