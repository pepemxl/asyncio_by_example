if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
from util.async_timer import async_timed
from util.delay_functions import delay
from util.sync_timed import sync_timed

@async_timed()
async def cpu_bound_work(task_id) -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


async def test_01() -> None:
    print("---Empezando test 01---")
    task_one = asyncio.create_task(cpu_bound_work(task_id=1))
    await task_one
    print("-----------------------")

async def test_02() -> None:
    print("Empezando test 02")
    task_delay = asyncio.create_task(delay(5,1))
    task_one = asyncio.create_task(cpu_bound_work(task_id=2))
    task_two = asyncio.create_task(cpu_bound_work(task_id=3))
    await task_one
    await task_two
    await task_delay
    print("-----------------------")

async def test_03() -> None:
    print("Empezando test 03")
    task_one = asyncio.create_task(cpu_bound_work(task_id=1))
    task_two = asyncio.create_task(cpu_bound_work(task_id=2))
    task_delay = asyncio.create_task(delay(5,3))
    await task_one
    await task_two
    await task_delay
    print("-----------------------")

@sync_timed()
def main() -> None:
    asyncio.run(test_01())
    asyncio.run(test_02())
    asyncio.run(test_03())


if __name__ == '__main__':
    main()