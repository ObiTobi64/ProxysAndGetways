import socket

data = {}
data_socket = socket.socket()
data_socket.bind(('localhost', 8020))
data_socket.listen()

print('LOGS: Data service escuchando en puerto 8020')


while True:
    conn, addr = data_socket.accept()
    with conn:
        req = conn.recv(1024).decode().strip()
        print(f'LOGS: Data service recibio {req}')
        if req.startswith('GET/data/'):
            key = req.split('/')[-1]
            
            if key in data:
                res = data[key]
            else:
                res = f'ERROR: Clave no encontrada'
        elif req.startswith('PUT/data/'):
            body = req.split('/')[-1]
            key, value = body.split('_')
            if key in data:
                res = f'Valor actualizado para {key}'
                data[key] = value
            else:
                res =f'Valor guardado para {key}'
                data[key] = value
        else:
            res = f'ERROR: Ruta invalida'
        conn.sendall(res.encode())

        


    