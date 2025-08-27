import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

try:
    print("Listo para recibir mensajes")
    connection, client_address = server_socket.accept()
    print(f"Cliente connectandose desde {client_address}")
    buffer = b''
    while buffer[-2:] != b'\r\n':
        data = connection.recv(2)
        if not data:
            break
        else:
            print(f"Data leida: {data}")
            buffer = buffer + data
    print(f"Toda la data leida: {buffer}")
    connection.sendall(b'Gracias por su Mensaje\n')
finally:
    server_socket.close()
    