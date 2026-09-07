import socket

from config import HOST, PORT
from security.tls_manager import create_server_context

context = create_server_context()

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"[SERVER] Запущен на {HOST}:{PORT}")

tls_server = context.wrap_socket(
    server_socket,
    server_side=True
)

while True:

    client_socket, address = tls_server.accept()

    print(f"[SERVER] Клиент: {address}")

    data = client_socket.recv(1024)

    message = data.decode()

    print(f"[SERVER] Получено: {message}")

    answer = f"Сервер получил: {message}"

    client_socket.send(answer.encode())

    client_socket.close()