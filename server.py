import sys
from socket import *
import threading
import pathlib
import os


# Tread function which executes the request
def thread_function(socket, address):
    try:
        # gets the request
        request = socket.recv(1024)
        print(request)

        # splits the request into part so that we can get the size of the file
        splitted_request = request.split()
        command = splitted_request[0]
        # file size
        file_size = splitted_request[1]
        print(file_size[1:])
        file_size = int(file_size[1:])

        if file_size < 100 or file_size > 20000:
            socket.send(b'400 Bad Request aaa')
            print(b'400 Bad Request')
            socket.close()
        else:
            # checks all the files if there is a file with given size
            for file_name in os.listdir('./html'):
                # gets the file path
                path_to_file = os.getcwd() + '\\html\\' + file_name
                st = os.stat(path_to_file)
                print(file_size, file_name, st.st_size)
                # checks if the file size is equals
                if st.st_size == file_size:
                    # opens the file and reads the content in it
                    f = open(path_to_file)
                    content = f.read()
                    f.close()
                    # creates a response with response message OK and content
                    response = 'HTTP/1.1 200 OK\n\n' + content
                    # sends the message and content
                    socket.sendall(response.encode())
                    print('{} sended. File_size : {}'.format(file_name, file_size))
                    break
            socket.close()
    # if any errors caught it also controls if the file size is int or not
    except error:
        print(error)
        socket.send(b'400 Bad Request')
        print(b'bbbbb')
        print(b'400 Bad Request')
        socket.close()


IP = 'localhost'
# port number
PORT = 8080

# initialize socket
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
threads = []

# bind socket with ip and port
try:
    server_socket.bind((IP, PORT))
    print('Bind is OK')
except socket.error as msg:
    print(msg)
    sys.exit()

server_socket.listen(1)

print('Server is ready to receive')

while True:
    # accepting the incomint request
    connection_socket, address = server_socket.accept()
    print('Connection\nIP Address and port: {}:{}\n{}\nSocket Protocol: {} Socket Family: {} Socket Type: {}'.format(
        address[0], address[1], connection_socket, connection_socket.proto, connection_socket.family,
        connection_socket.type))
    # creates a threads to run incoming requests
    childThread = threading.Thread(target=thread_function, args=(connection_socket, address))
    childThread.start()
    childThread.join()

# closes socket
server_socket.close()
sys.exit()
