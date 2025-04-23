import socket

def handle_request(data):
    return f"{data} del servidor".encode()

server_socket = socket.socket()
server_socket.bind(('localhost', 8000))
server_socket.listen()

print("Servidor original escuchando en puerto 8000...")

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    print(f"Servidor recibió: {data}")
    response = handle_request(data)
    conn.sendall(response)
    conn.close()
