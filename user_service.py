import socket

users = {'69017': 'Andres', '70835': 'Ivan', '70419': 'Adrian', '64931': 'Mishel'}

user_socket = socket.socket()
user_socket.bind(('localhost', 8010))
user_socket.listen()

print('User service escuchando en puerto 8010')

while True:
    conn, addr = user_socket.accept()
    with conn:
        req = conn.recv(1024).decode().strip()
        print(f'LOGS: User service recibio {req}')
        if req.startswith('GET/users/'):
            codigo = req.split('/')[-1]
            if codigo in users:
                res = f'Usuario: {users[codigo]}'
            else:
                res = f'ERROR: Usuario no encontrado'
        else:
            res = f'ERROR: Ruta invalida'
        conn.sendall(res.encode())
        


    