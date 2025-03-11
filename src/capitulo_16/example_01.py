import asyncio
import capnp
import socket

import test_capability_capnp


class Server(test_capability_capnp.TestInterface.Server):

    def __init__(self, val=1):
        self.val = val

    async def foo(self, i, j, **kwargs):
        return str(i * 5 + self.val)


async def client(read_end):
    client = capnp.TwoPartyClient(read_end)

    cap = client.bootstrap()
    cap = cap.cast_as(test_capability_capnp.TestInterface)

    remote = cap.foo(i=5)
    response = await remote

    assert response.x == '125'

async def main():
    client_end, server_end = socket.socketpair(socket.AF_UNIX)
    # This is a toy example using socketpair.
    # In real situations, you can use any socket.

    client_end = await capnp.AsyncIoStream.create_connection(sock=client_end)
    server_end = await capnp.AsyncIoStream.create_connection(sock=server_end)

    _ = capnp.TwoPartyServer(server_end, bootstrap=Server(100))
    await client(client_end)


if __name__ == '__main__':
    asyncio.run(capnp.run(main()))