import socket
import threading

cache = {}

proxy_socket = socket.socket()
proxy_socket.bind(('0.0.0.0', 8080))
proxy_socket.listen()

print("Proxy escuchando en puerto 8080...")

def handle_client(conn, addr):
    print(f"Nuevo cliente conectado desde {addr}")
    while True:
        print('Esperando key en proxy...')
        key = conn.recv(1024).decode()
        if not key:
            break  # Cliente cerró conexión

        if key in cache:
            print("Cache Hit")
            response = cache[key]
        else:
            print("Cache Miss")
            with socket.socket() as s:
                s.connect(('0.0.0.0', 8000))
                s.sendall(key.encode())
                server_res = s.recv(1024).decode()
            cache[key] = server_res
            response = cache[key]

        conn.sendall(response.encode())


    conn.close()
    print(f"Cliente {addr} desconectado")

while True:
    conn, addr = proxy_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
