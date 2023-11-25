import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/socket_file'
print('connecting to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print('socket error: {}'.format(err))
    sys.exit(1)

try:
    message = b'Sending a message to the server side'
    sock.sendall(message)
    sock.settimeout(2)

    try:
        while True:
            data = sock.recv(32)
            if data:
                print('received {}'.format(data))
            else:
                break
    except(TimeoutError):
        print('timeout error')
finally:
    print('closing socket')
    sock.close()