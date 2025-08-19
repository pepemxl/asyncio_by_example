import asyncio
from typing import Optional

async def delay(delay_seconds: int, task_id: Optional[int] = None) -> int:
    if task_id:
        print(f'Task {task_id} Durmiendo por {delay_seconds} segundo(s)')
    else:
        print(f'Durmiendo por {delay_seconds} segundo(s)')
    await asyncio.sleep(delay_seconds)
    if task_id:
        print(f'Task {task_id} Termino la funcion dormir por {delay_seconds} segundo(s)')
    else:
        print(f'Termino la funcion dormir por {delay_seconds} segundo(s)')
    return delay_seconds

