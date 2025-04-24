import socket

# Lista de servidores backend
backends = [('localhost', 8001), ('localhost', 8002)]
counter = 0  # Para Round Robin

gateway_socket = socket.socket()
gateway_socket.bind(('localhost', 9000))
gateway_socket.listen()

print("Gateway escuchando en puerto 9000...")

while True:
    conn, addr = gateway_socket.accept()

    while True:
        print(f'Gateway en espera...')
        data = conn.recv(1024).decode()

        print(f"Gateway recibió: {data}")

        backend = backends[counter % len(backends)]
        counter += 1
        try:
            with socket.socket() as backend_socket:
                backend_socket.connect(backend)
                backend_socket.sendall(data.encode())
                response = backend_socket.recv(1024)
        except Exception as e:
            print(f"Error al conectar con backend {backend}: {e}")
            other_backend = backends[(counter) % len(backends)] # Ira al siguiente backend si uno falla
            print(f"Intentando con el siguiente backend: {other_backend}")
            try:
                with socket.socket() as backend_socket:
                    backend_socket.connect(other_backend)
                    backend_socket.sendall(data.encode())
                    response = backend_socket.recv(1024)
            except Exception as e:
                response = f"Error: Ningún backend disponible ({e})".encode()

        conn.sendall(response)

    
