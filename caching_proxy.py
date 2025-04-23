import socket

cache = {'202412345_Navi'}

def get_from_server(key):
    with socket.socket() as s:
        s.connect(('localhost', 8000))
        s.sendall(key.encode())
        return s.recv(1024)

proxy_socket = socket.socket()
proxy_socket.bind(('localhost', 8080))
proxy_socket.listen()

print("Proxy escuchando en puerto 8080...")

while True:
    conn, addr = proxy_socket.accept()
    key = conn.recv(1024).decode()

    if key in cache:
        print("Cache Hit")
        response = cache[key]
    else:
        print("Cache Miss")
        response = get_from_server(key)
        cache[key] = response

    conn.sendall(response)
    conn.close()
