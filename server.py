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
        if splitted_request[0]:
            command = splitted_request[0]
        print("command ", command)
        # file size
        if len(splitted_request) >= 2:
            # todo error burda integer olup olmadigini kontrol etmemiz lazim
            try:
                file_size = int(splitted_request[1])
                print(file_size[1:])
                file_size = int(file_size[1:])
                print(b'file size ok')
            except:
                socket.send(b'400 Bad Request')
                socket.send(b'Please enter integer value')
                print(b'400 Bad Request')
                socket.close()
                return

        if command.upper() == b'HEAD' \
                or command.upper() == b'POST' \
                or command.upper() == b'PUT' \
                or command.upper() == b'DELETE' \
                or command.upper() == b'CONNECT' \
                or command.upper() == b'OPTIONS' \
                or command.upper() == b'TRACE':
            socket.send(b'501 Not implemented')
            print(b'501 Not implemented')
            socket.close()
        elif command.upper() == b'GET':
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
                        response_content = f.read()
                        f.close()
                        response_headers = {
                            'Content-Type': 'text/html; encoding=utf8',
                            'Content-Length': len(response_content),
                        }
                        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())

                        # reply as HTTP/1.1 server, saying "HTTP OK" (code 200)
                        socket.send(b'HTTP/1.1 200 OK')
                        # send response
                        socket.send(response_headers_raw.encode())
                        # send response content
                        socket.send(response_content.encode())
                        print('{} sended. File size : {}'.format(file_name, file_size))
                        break
                socket.close()
        else:
            socket.send(b'400 Bad Request')
            print(b'400 Bad Request')
            socket.close()
    # if any errors caught
    except error:
        socket.send(b'400 Bad Request')
        print(b'400 Bad Request')
        print(error)
        socket.close()


IP = 'localhost'
# port number
PORT = 8080
# int(sys.argv[1])

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
    # accepting the incoming request
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
