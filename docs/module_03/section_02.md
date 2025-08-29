# Sockets NO bloqueantes

Nuestro servidor anterior permitía la conexión de varios clientes; sin embargo, cuando se conectaba más de uno, surgían problemas donde el principal era que un cliente podía hacer que los demás esperaran a que enviara datos. 

Podemos solucionar este problema activando el modo **sin bloqueo** de los sockets.

Al hacer esto, cada vez que llamamos a un método que bloquearía, como `recv`, se garantiza que regresará instantáneamente. Si el socket tiene datos listos para procesar, los recibiremos como si fuera un socket bloqueado. De lo contrario, el socket "nos informará" inmediatamente que no tiene datos listos y podremos ejecutar otro código.

La única diferencia es que agregaremos una configuración en el servidor y en cada conexión:

- `server_socket.setblocking(False)`
- `connection.setblocking(False)`

## Ejemplo no bloqueante

```python title="Ejemplo para leer y escribir desde y hacia un socket" linenums="1"
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
server_socket.setblocking(False)

connections = []

try:
    while True:
        print("Listo para recibir mensajes!")
        connection, client_address = server_socket.accept()
        connection.setblocking(False)
        print(f"Cliente connectandose desde {client_address}")
        connections.append(connection)
        for connection in connections:
            buffer = b''
            while buffer[-2:] != b'\r\n':
                data = connection.recv(2)
                if not data:
                    break
                else:
                    print(f"Data leida: {data}")
                    buffer = buffer + data
            print(f"Toda la data leida: {buffer}")
            connection.send(buffer)
finally:
    server_socket.close()
```


```bash title="Salida Woops"
Listo para recibir mensajes!
Traceback (most recent call last):
  File "/asyncio_by_example/src/capitulo_03/section_02/01_no_blocking_socket.py", line 16, in <module>
    connection, client_address = server_socket.accept()
                                 ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/socket.py", line 293, in accept
    fd, addr = self._accept()
               ^^^^^^^^^^^^^^
BlockingIOError: [Errno 11] Resource temporarily unavailable
```

Se generará un error `BlockingIOError` porque nuestro socket de servidor aún no tiene conexión y, por lo tanto, no hay datos que procesar.

## Ejemplo no bloqueante con try catch

Para poder evitarlo por el momento usaremos `try... except`

```python title="Ejemplo para leer y escribir desde y hacia un socket" linenums="1"
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()
server_socket.setblocking(False)

connections = []

try:
    while True:
        try:
            #print("Listo para recibir mensajes!")
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f"Cliente connectandose desde {client_address}")
            connections.append(connection)
        except BlockingIOError:
            pass
        for connection in connections:
            try:
                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f"Data leida: {data}")
                        buffer = buffer + data
                print(f"Toda la data leida: {buffer}")
                connection.send(buffer)
            except BlockingIOError:
                pass
finally:
    server_socket.close()
```

```bash title="Salida"
Cliente connectandose desde ('127.0.0.1', 59764)
Data leida: b'Ho'
Data leida: b'la'
Data leida: b' M'
Data leida: b'un'
Data leida: b'do'
Data leida: b'3\r'
Data leida: b'\n\n'
Cliente connectandose desde ('127.0.0.1', 45118)
Data leida: b'Ho'
Data leida: b'la'
Data leida: b' M'
Data leida: b'un'
Data leida: b'do'
Data leida: b'2\r'
Data leida: b'\n\n'
Cliente connectandose desde ('127.0.0.1', 45128)
Data leida: b'Ho'
Data leida: b'la'
Data leida: b' M'
Data leida: b'un'
Data leida: b'do'
Data leida: b'\r\n'
Toda la data leida: b'Hola Mundo\r\n'
Data leida: b'\n'
```


Sin embargo podemos notar que se queda colgado `nc`

vamos a intentar usando telnet

- `telnet localhost 8000`

```bash title="Salida"
Cliente connectandose desde ('127.0.0.1', 53410)
Data leida: b'Ho'
Data leida: b'la'
Data leida: b' m'
Data leida: b'un'
Data leida: b'do'
Data leida: b'\r\n'
Toda la data leida: b'Hola mundo\r\n'
Cliente connectandose desde ('127.0.0.1', 36062)
Data leida: b'Ho'
Data leida: b'la'
Data leida: b' m'
Data leida: b'un'
Data leida: b'do'
Data leida: b'\r\n'
Toda la data leida: b'Hola mundo\r\n'
```

Ahora si trabaja de manera correcta.