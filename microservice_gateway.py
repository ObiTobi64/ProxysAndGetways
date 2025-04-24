import socket

user_service, data_service = [('localhost', 8010), ('localhost', 8020)]
micro_gateway = socket.socket()
micro_gateway.bind(('localhost', 9000))
micro_gateway.listen()
print(f'LOGS: Gateway de micro servicio escucando en puerto 9000')

def redirect(service, req_fw):
    print(f'{service}\n{req_fw}\n')
    try:
        with socket.socket() as s:
            print(f'LOGS: Enviando solicitud al servicio {service}')
            s.connect(service)
            s.sendall(req_fw.encode())
            res = s.recv(1024).decode()
            return res
    except Exception as e:
        return f'ERROR: No se pudo conectar con el servicio {e}'


while True:
    conn, addr = micro_gateway.accept()
    while True:
        req = conn.recv(1024).decode()
        if req.startswith('GET/data/') or req.startswith('PUT/data/'):
            response =redirect(data_service, req)
        elif req.startswith('GET/users'):
            response =redirect(user_service, req)
        else:
            response = 'ERROR: Ruta invalida'
        conn.sendall(response.encode())
            
