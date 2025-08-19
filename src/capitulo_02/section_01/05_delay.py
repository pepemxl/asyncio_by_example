import asyncio

async def delay(delay_seconds: int) -> int:
    print(f'Durmiendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    print(f'Termino la funcion dormir por {delay_seconds} segundo(s)')
    return delay_seconds