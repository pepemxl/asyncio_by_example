import asyncio
import time


async def say_after(delay, message):
    # print("Inicio con delay", delay)
    await asyncio.sleep(delay)
    print(message, end=' ')

async def main():
    print(f"started at {time.strftime('%X')}")
    # tasks = []
    # tasks.append(await say_after(3, 'pepe'))
    # tasks.append(await say_after(2, 'World'))
    # tasks.append(await say_after(1, 'Hello'))
    await asyncio.gather(say_after(3, 'pepe'),say_after(2, 'World'), say_after(1, 'Hello'))
    #await asyncio.gather_all(tasks)
    print('')
    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())