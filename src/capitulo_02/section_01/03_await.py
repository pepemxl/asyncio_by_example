import asyncio

async def add_one(number: int) -> int:
    return number + 1

async def main() -> None:
    one_plus_one = await add_one(1)
    two_plus_one = await add_one(2)
    print(f"Resultado de one_plus_one es: {one_plus_one}")
    print(f"Resultado de two_plus_one es: {two_plus_one}")

asyncio.run(main())