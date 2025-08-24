if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from util.delay_functions import delay

def call_later():
    print("Esta función será llamada después")


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

if __name__ == '__main__':
    asyncio.run(main())