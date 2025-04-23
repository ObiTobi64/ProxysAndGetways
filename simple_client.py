import socket
import time

key = "202412345_Ivan "

start = time.time()
with socket.socket() as s:
    s.connect(('localhost', 8080))
    s.sendall(key.encode())
    response = s.recv(1024)
end = time.time()

print(f"Respuesta: {response.decode()}")
print(f"Tiempo de respuesta: {end - start:.4f} segundos")
