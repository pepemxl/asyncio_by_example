import asyncio

async def delay(delay_seconds: int) -> int:
    print(f'Durmiendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    print(f'Termino la funcion dormir por {delay_seconds} segundo(s)')
    return delay_seconds

async def add_one(number: int) -> int:
    return number + 1

async def hello_world_message() -> str:
    await delay(1)
    return 'Hello World'

async def main() -> None:
    message = await hello_world_message()
    one_plus_one = await add_one(1)
    print(f"Resultado de one_plus_one es: {one_plus_one}")
    print(f"Resultado de message es: {message}")

asyncio.run(main())