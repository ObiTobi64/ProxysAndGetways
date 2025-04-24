import socket

def handle_request(data):
    return f"{data} desde el servidor en puerto 8002".encode()

server_socket = socket.socket()
server_socket.bind(('localhost', 8002))
server_socket.listen()

print("Servidor escuchando en puerto 8002...")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    print(f"Servidor 8002 recibió: {data}")
    response = handle_request(data)
    conn.sendall(response)
    conn.close()
