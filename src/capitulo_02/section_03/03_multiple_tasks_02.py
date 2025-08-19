if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from util.delay_functions import delay

async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("Yo me ejecuto mientras otro codigo esta siendo ejecutado")

async def main():
    first_delay = asyncio.create_task(delay(3, 1))
    second_delay = asyncio.create_task(delay(3, 2))
    await hello_every_second()
    await first_delay
    await second_delay

if __name__ == '__main__':
    asyncio.run(main())
