# Tópicos avanzados de Asyncio

## Como trabajar con  librerias bloqueantes?

Un ejemplo de código bloqueante es la librería `sockets`.

Para usar librerías tradicionalmente bloqueantes como `socket` con asyncio de manera no bloqueante, tenemos varias opciones:

## 1. Usar las versiones específicas de asyncio

Asyncio proporciona sus propias versiones de muchas operaciones de red:

```python
import asyncio

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    
    writer.write(message.encode())
    await writer.drain()  # Espera a que sea apropiado reanudar la escritura
    
    data = await reader.read(100)
    print(f'Received: {data.decode()}')
    
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('Hello World!'))
```

## 2. Usar `loop.sock_*` para sockets estándar

Si necesitas usar sockets tradicionales, puedes convertirlos a no bloqueantes y usar los métodos del event loop:

```python
import asyncio
import socket

async def tcp_client():
    # Crear socket tradicional
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)  # ¡Importante! Hacer el socket no bloqueante
    
    loop = asyncio.get_event_loop()
    
    try:
        await loop.sock_connect(sock, ('127.0.0.1', 8888))
        await loop.sock_sendall(sock, b'Hello World')
        data = await loop.sock_recv(sock, 1024)
        print(f'Received: {data.decode()}')
    finally:
        sock.close()

asyncio.run(tcp_client())
```

## 3. Usar ejecutores para operaciones bloqueantes

Para código que no puede hacerse nativamente asíncrono, puedes usar ejecutores de threads:

```python
import asyncio
import socket

def blocking_socket_operation():
    # Código bloqueante tradicional
    s = socket.socket()
    s.connect(('127.0.0.1', 8888))
    s.send(b'Hello')
    return s.recv(1024)

async def main():
    loop = asyncio.get_event_loop()
    # Ejecutar en un thread separado
    result = await loop.run_in_executor(None, blocking_socket_operation)
    print(f'Received: {result.decode()}')

asyncio.run(main())
```


1. **Siempre debemos marcar los sockets como no bloqueantes** con `setblocking(False)` antes de usarlos con asyncio.
2. **Evita mezclar APIs** - No uses métodos bloqueantes (como `recv`) con await, ya que aún bloquearán el event loop.
3. **Prefer las APIs nativas de asyncio** (`open_connection`, `start_server`, etc.) cuando sea posible.
4. **Para operaciones intensivas de CPU**, usa `run_in_executor` para no bloquear el event loop.

Las librerías modernas como `aiohttp` para HTTP o `asyncpg` para PostgreSQL proporcionan APIs nativas para asyncio que son preferibles a adaptar librerías bloqueantes.




