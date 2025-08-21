from asyncio import Future

my_future = Future()
print(f'my_future termino? {my_future.done()}')
my_future.set_result(42)
print(f'my_future termino? {my_future.done()}')
print(f'Cual es el resultado de my_future? {my_future.result()}')