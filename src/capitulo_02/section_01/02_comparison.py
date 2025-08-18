import asyncio

async def coroutine_add_one(number: int) -> int:
    return number + 1

coroutine_result = asyncio.run(coroutine_add_one(1))
print(f"El resultado de la corutina es {coroutine_result} y su tipo es {type(coroutine_result)}")