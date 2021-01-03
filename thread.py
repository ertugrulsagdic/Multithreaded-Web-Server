import threading
from socket import *
import os
import pathlib


def Thread(socket, address):
    # def __init__(self, ip, port, socket):
    #     threading.Thread.__init__(self)
    #     self.ip = ip
    #     self.port = port
    #     self.socket = socket
    try:
        request = self.socket.recv(1024)
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
                self.socket.sendall(response.encode())
                print('{} sended. File_size : {}'.format(file_name, file_size))
                break
            elif file_size < 100 or file_size > 20000:
                self.socket.send(b'400 Bad Request aaa')
                print(b'400 Bad Request')
        self.socket.close()

    except:
        self.socket.send(b'400 Bad Request')
        print(b'bbbbb')
        print(b'400 Bad Request')
        self.socket.close()
