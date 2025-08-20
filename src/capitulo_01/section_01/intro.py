import asyncio


async def greeting_async() -> str:
    """
    Demonstrates a simple asynchronous function that returns a greeting.
    """
    await asyncio.sleep(1)  # Simulate async I/O or waiting
    return "Hello World!"


async def main() -> None:
    result = await greeting_async()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())