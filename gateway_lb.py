import socket
import threading

# Lista de servidores backend
backends = [('192.168.91.97', 8001), ('192.168.91.98', 8002)]
counter = 0  # Para Round Robin
counter_lock = threading.Lock()  # Para proteger el acceso al contador

def handle_client(conn, addr):
    global counter
    print(f"Cliente conectado desde {addr}")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Cliente {addr} desconectado")
                break

            print(f"Gateway recibió de {addr}: {data}")

            # Elegir backend de forma segura (con lock)
            with counter_lock:
                backend = backends[counter % len(backends)]
                counter += 1

            try:
                with socket.socket() as backend_socket:
                    backend_socket.connect(backend)
                    backend_socket.sendall(data.encode())
                    response = backend_socket.recv(1024)
            except Exception as e:
                print(f"Error al conectar con backend {backend}: {e}")
                other_backend = backends[(counter) % len(backends)]  # Ir al siguiente backend si uno falla
                print(f"Intentando con el siguiente backend: {other_backend}")
                try:
                    with socket.socket() as backend_socket:
                        backend_socket.connect(other_backend)
                        backend_socket.sendall(data.encode())
                        response = backend_socket.recv(1024)
                except Exception as e:
                    response = f"Error: Ningún backend disponible ({e})".encode()

            conn.sendall(response)
        
        except Exception as e:
            print(f"Error con cliente {addr}: {e}")
            break

    conn.close()

# MAIN SERVER
gateway_socket = socket.socket()
gateway_socket.bind(('0.0.0.0', 9000))
gateway_socket.listen()

print("Gateway escuchando en puerto 9000...")

while True:
    conn, addr = gateway_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()