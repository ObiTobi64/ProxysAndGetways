import socket

cache = {'Navi': 'Navi'}

proxy_socket = socket.socket()
proxy_socket.bind(('localhost', 8080))
proxy_socket.listen()

print("Proxy escuchando en puerto 8080...")

while True:
    conn, addr = proxy_socket.accept()
    while True:
        print(f'Esperando key en proxy...')
        key = conn.recv(1024).decode()

        if key in cache:
            print("Cache Hit")
            response = cache[key]
        else:
            print("Cache Miss")
            with socket.socket() as s:
                s.connect(('localhost', 8000))
                s.sendall(key.encode())
                server_res = s.recv(1024).decode()
            cache[key] = server_res
            response = cache[key]

        conn.sendall(response.encode())
