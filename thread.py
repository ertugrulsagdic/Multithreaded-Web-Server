import threading
from socket import *
import os

BYTES = 20000

class Thread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
    
    def process(self):

        request = self.socket.recv(BYTES)
        print(request)

        splitted_request = request.split()
        file_size = splitted_request[1]
        file_size = int(file_size[1:])


        for file_name in os.listdir('/'):
            if os.stat(file_name).st_size == file_size:
                f = open(file_name)
                content = f.read()
                self.socket.send(b'HTTP/1.1 200 OK')
                self.socket.send(content.encode())
                print('{} sended. File_size : {}'.format(file_name, file_size))
                self.socket.close()
                return
        
        self.socket.send(b'HTTP/1.1 404 Not Found')
        print('{} bytes file not found'.format(file_size))
        self.socket.close()
        







