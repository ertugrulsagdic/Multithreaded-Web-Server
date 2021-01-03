from socket import *
from thread import *

IP = 'localhost'
PORT = 12000

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
threads = []
server_socket.bind((IP, PORT))
server_socket.listen(1)

print('Server is ready to receive')


while True:
    connection_socket, address = server_socket.accept()
    print('Connection\nIP Address and port: {}:{}\n{}\nSocket Protocol: {} Socket Family: {} Socket Type: {}'.format(address[0], address[1], connection_socket, connection_socket.proto, connection_socket.family, connection_socket.type))
    connection = Thread(address[0], address[1], connection_socket)
    connection.process()
    threads.append(connection)





