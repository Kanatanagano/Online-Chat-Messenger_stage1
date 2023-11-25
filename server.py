import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = '/socket_file'

# server address unlinked if already exists
try:
    os.unlink(server_address)
except FileExistsError:
    pass

print('starting up on {}'.format(server_address))
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print('connection from {}'.format(client_address))
        while True:
            data = connection.recv(16)
            data_str = data.decode('utf-8')
            print('received {}'.format(data_str))

            if data:
                response = 'processing' + data_str
                connection.sendall(response.encode('utf-8'))
            else:
                print('no data from {}'.format(client_address))
                break
    finally:
        print('closing connection')
        connection.close()

