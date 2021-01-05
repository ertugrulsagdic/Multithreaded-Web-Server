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
        file_size = 0
        if len(splitted_request) >= 2:
            try:
                file_size = splitted_request[1]
                print(file_size[1:])
                file_size = int(file_size[1:])
                print(b'file size ok')
            except:
                socket.send(b'400 Bad Request')
                socket.send(b'File size is not integer\n')
                socket.send(b'Please provide an integer value')
                print(b'400 Bad Request')
                print(b'File size is not integer')
                print(b'Please provide an integer value')
                socket.close()
                return

        if command == b'HEAD' \
                or command == b'POST' \
                or command == b'PUT' \
                or command == b'DELETE' \
                or command == b'CONNECT' \
                or command == b'OPTIONS' \
                or command == b'TRACE':
            socket.send(b'501 Not implemented')
            print(b'501 Not implemented')
            socket.close()
        elif command == b'GET':
            if file_size < 100:
                socket.send(b'400 Bad Request')
                socket.send(b'File size is less than 100\n')
                socket.send(b'Please provide file size between 100 and 20000')
                print(b'400 Bad Request')
                print(b'File size is less than 100')
                print(b'Please provide file size between 100 and 20000')
                socket.close()
            elif file_size > 20000:
                socket.send(b'400 Bad Request')
                socket.send(b'File size is less than 100\n')
                socket.send(b'Please provide file size between 100 and 20000')
                print(b'400 Bad Request')
                print(b'File size is greater than 20000')
                print(b'Please provide file size between 100 and 20000')
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
                        response = 'HTTP/1.1 200 OK' + response_headers_raw + "\n" + response_content
                        socket.send(response.encode())
                        # # send response
                        # socket.send(response_headers_raw.encode())
                        # # send response content
                        # socket.send(response_content.encode())
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
