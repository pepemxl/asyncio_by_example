import asyncio
import time


async def say_after(delay, message):
    print(f"Start with delay of {delay} segs")
    await asyncio.sleep(delay)
    print(message, end=' ')

async def main():
    print(f"Started at {time.strftime('%X')}")
    await asyncio.gather(say_after(3, 'pepe'),say_after(2, 'World'), say_after(1, 'Hello'))
    print('')
    print(f"Finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())