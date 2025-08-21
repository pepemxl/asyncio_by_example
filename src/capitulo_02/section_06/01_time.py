import asyncio
import time

async def main():
    start = time.time()
    await asyncio.sleep(1)
    end = time.time()
    print(f'Dormir tomo {end - start} segundos')

asyncio.run(main())