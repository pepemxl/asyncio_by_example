import asyncio
import time


async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message, end=' ')

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')
    await say_after(3, 'pepe')
    print('')
    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())