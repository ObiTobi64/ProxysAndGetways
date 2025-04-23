import socket
import time

key = "Navi"

with socket.socket() as s:
    s.connect(('localhost', 8080))
    while True:
        key = input('Ingresa la key: ')
        start = time.time()
        s.sendall(key.encode())
        response = s.recv(1024)
        end = time.time()
        print(f"Respuesta: {response.decode()}")
        print(f"Tiempo de respuesta: {end - start:.4f} segundos")

