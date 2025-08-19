if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from util.delay_functions import delay

async def main():
    sleep_for_three = asyncio.create_task(delay(3, 1))
    sleep_again = asyncio.create_task(delay(3, 2))
    sleep_once_more = asyncio.create_task(delay(3, 3))
    await sleep_for_three
    await sleep_again
    await sleep_once_more

if __name__ == '__main__':
    asyncio.run(main())
