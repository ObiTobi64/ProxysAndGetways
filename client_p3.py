import socket
import time
with socket.socket() as s:
    s.connect(('192.168.188.136', 9000))
    print("LOGS: Conectado al gateway en el puerto 9000")
    while True:
        key = input('Ingresa la ruta\n')
        start = time.time()
        s.sendall(key.encode())
        response = s.recv(1024)
        end = time.time()
        print(f"OK: Respuesta: {response.decode()}")
        print(f"LOGS: Tiempo de respuesta: {end - start:.4f} segundos")