from socket import *
import threading
import pathlib
import os


def thread_function(socket, address):
    # def __init__(self, ip, port, socket):
    #     threading.Thread.__init__(self)
    #     self.ip = ip
    #     self.port = port
    #     self.socket = socket
    try:
        request = socket.recv(1024)
        print(request)

        splitted_request = request.split()
        command = splitted_request[0]
        file_size = splitted_request[1]
        print(file_size[1:])
        file_size = int(file_size[1:])

        for file_name in os.listdir('./html'):
            path_to_file = os.getcwd() + '\\html\\' + file_name
            print('path_to_file  ', path_to_file)
            st = os.stat(path_to_file)
            print(pathlib.Path().absolute())
            print(file_size, file_name, st.st_size)
            if st.st_size == file_size:
                f = open(path_to_file)
                content = f.read()
                f.close()
                response = 'HTTP/1.1 200 OK\n\n' + content
                #self.socket.send(b'HTTP/1.1 200 OK')
                socket.sendall(response.encode())
                print('{} sended. File_size : {}'.format(file_name, file_size))
                break
            elif file_size < 100 or file_size > 20000:
                socket.send(b'400 Bad Request aaa')
                print(b'400 Bad Request')
        socket.close()

    except error:
        print(error)
        socket.send(b'400 Bad Request')
        print(b'bbbbb')
        print(b'400 Bad Request')
        socket.close()


IP = 'localhost'
PORT = 8080

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
threads = []

try:
    server_socket.bind((IP, PORT))
    print('Bind is OK')
except socket.error as msg:
    print(msg)
    sys.exit()

## ??
server_socket.listen(1)

print('Server is ready to receive')


while True:
    connection_socket, address = server_socket.accept()
    print('Connection\nIP Address and port: {}:{}\n{}\nSocket Protocol: {} Socket Family: {} Socket Type: {}'.format(address[0], address[1], connection_socket, connection_socket.proto, connection_socket.family, connection_socket.type))
    childThread = threading.Thread(target=thread_function, args=(connection_socket, address))
    childThread.start()

server_socket.close()
sys.exit()




