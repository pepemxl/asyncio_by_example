import asyncio

async def main():
    await asyncio.sleep(1)

def create_event_loop():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

if __name__ == '__main__':
    create_event_loop()