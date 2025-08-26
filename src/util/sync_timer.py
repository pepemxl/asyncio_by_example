import functools
import time
from typing import Callable, Any

def sync_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            print(f'Empezando función sincrona {func} con args {args} {kwargs}')
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'La función sincrona {func} termino en {total:.4f} segundo(s)')
        return wrapped
    return wrapper