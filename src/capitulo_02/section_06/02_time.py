import asyncio
import functools
import time
from typing import Callable, Any

def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Empezando función {func} con args {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'La función {func} termino en {total:.4f} segundo(s)')
        return wrapped
    return wrapper


@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'Durmniendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    print(f'Termino de dormir en {delay_seconds} segundo(s)')
    return delay_seconds


@async_timed()
async def main():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))
    await task_one
    await task_two

asyncio.run(main())