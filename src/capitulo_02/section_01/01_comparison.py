async def coroutine_add_one(number: int) -> int:
    return number + 1

def add_one(number: int) -> int:
    return number + 1

function_result = add_one(1)
coroutine_result = coroutine_add_one(1)

print(f"El resultado serial es {function_result} y su tipo es {type(function_result)}")
print(f"El resultado de la coruutina es {coroutine_result} y su tipo es {type(coroutine_result)}")