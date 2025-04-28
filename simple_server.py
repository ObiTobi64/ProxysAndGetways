import socket
import threading

db = {'69017': 'Andres', '70835': 'Ivan', '70419': 'Adrian', '64931': 'Mishel'}

def handle_client(conn, addr):
    print(f"Conectado con {addr}")
    while True:
        data = conn.recv(1024)
        if not data: break
        data = data.decode().split(' ')[1]
        # print(data)
        if data in db:
            response = db[data].encode()
            print(f"Servidor devolvio de {addr}: {data}")
        else:
            db[data] = data
            print(f"Servidor actualizo de {addr}: {data}")
            response = db[data].encode()
            
            
        # response = f"{data} del servidor".encode()
        conn.sendall(response)
    
    conn.close()
    print(f"Conexión cerrada con {addr}")

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen()

print("Servidor original escuchando en puerto 8000...")

while True:
    conn, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
