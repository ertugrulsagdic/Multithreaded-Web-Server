import sys
from socket import *
import threading
import pathlib
import os
from urllib.request import Request, urlopen, HTTPError

IP = '127.0.0.1'
# port number
PORT = 8888

def get_file(file_size):
    file_from_cache = get_file_from_cache(file_size)
    if file_from_cache:
        print('Hit Cache')
        return True, file_from_cache
    else:
        print('File is not in cache.')
        message_header_content = get_file_from_server(file_size)

        if len(message_header_content) > 2:
            save_to_cache(file_size, message_header_content)
            return True, message_header_content
        else:
            return False, message_header_content

def save_to_cache(file_size, content):
    print('Save the file to the cache')
    file_that_will_be_cached = open('cached_files/' + str(file_size) + 'bytes.html', 'wb')
    print(len(content))
    file_that_will_be_cached.write(content.encode())
    file_that_will_be_cached.close()


def get_file_from_server(file_size):
    print("DEBUG1")
    url = 'http://127.0.0.1:8080/' + str(file_size)
    print("Debug2", url)
    request = Request(url)
    print("DEBUG3")

    try:
        response = urlopen(request)
        # print('Response',response)
        # print("decode",response.read().decode())
        # print('info',response.info())

        return response.read().decode()
    except HTTPError:
        print(HTTPError)
        return None


def get_file_from_cache(file_size):

    for file_name in os.listdir('./cached_files'):
        # get the file path
        path_to_file = os.getcwd() + '\\cached_files\\' + file_name
        st = os.stat(path_to_file)
        if st.st_size == file_size:
            # open the file and read the content.
            f = open(path_to_file)
            response_content = f.read()
            f.close()

            return response_content

    return None
    #         response_headers = {
    #             'Content-Type': 'text/html; encoding=utf8',
    #             'Content-Length': len(response_content),
    #         }
    #         response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())
    #         # reply as HTTP/1.1 server, saying "HTTP OK" (code 200)
    #         response = 'HTTP/1.1 200 OK' + response_headers_raw + "\n\n" + response_content
    #         socket.send(response.encode())
    #         print('{} sended. File size : {}'.format(file_name, file_size))
    #         socket.close()
    #         return True
    # return False

def thread_function(socket, address):
    # Get the request
    request = socket.recv(1024).decode()
    print('request ', request)

    splitted_request = request.split()
    command = splitted_request[0]
    print("command ", command)

    if request == b'':
        return

    '''
    proxy server has a restriction. If the requested file size is greater than 9,999 (in
    other words, if the URI is greater than 9,999) it would not pass the request to the web server.
    Rather it sends “Request-URI Too Long” message with error code 414.
    '''
    # if file_size > 9999:
    #     socket.send(b'414 Request-URI Too Long')
    #     print(b'414 Request-URI Too Long')
    #     socket.close()

    if command == 'HEAD' \
            or command == 'POST' \
            or command == 'PUT' \
            or command == 'DELETE' \
            or command == 'CONNECT' \
            or command == 'OPTIONS' \
            or command == 'TRACE':
        # reply "HTTP Not Implemented" (code 501)
        socket.send(b'501 Not implemented')
        print(b'501 Not implemented')
        socket.close()
    elif command == 'GET':

        file_size = 0
        if len(splitted_request) >= 2:
            file_size = splitted_request[1]
            if(file_size[0] == '/'):
                print(file_size[1:])
                file_size = int(file_size[1:])
            else:
                print(file_size)
                urll = file_size.split('/')
                print(urll)
                file_size = int(urll[-1])
                print(file_size)
            print(b'file size ok')

        if file_size < 100:
            # reply "HTTP Bad Request" (code 400)
            socket.send(b'HTTP/1.1 400 Bad Request\r\n')
            socket.send(b'File size is less than 100\r\n')
            socket.send(b'Please provide file size between 100 and 20000')
            print(b'400 Bad Request')
            print(b'File size is less than 100')
            print(b'Please provide file size between 100 and 20000')
            socket.close()
        elif file_size > 9999:
            # reply "HTTP Bad Request" (code 400)
            socket.send(b'414 Request-URI Too Long')
            print(b'414 Request-URI Too Long')
            socket.close()
        else:

            try:
                isTrue, content_or_response = get_file(file_size)
            except:
                socket.send(b'404 Not Found')
                print(b'404 Not Found')
                socket.close()
                return

            if isTrue:
                response_headers = {
                    'Content-Type': 'text/html; encoding=utf8',
                    'Content-Length': len(content_or_response),
                }
                response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())
                response = 'HTTP/1.0 200 OK\n' + response_headers_raw + '\n' + content_or_response
                socket.send(response.encode())
                print('Proxy has sent the file. File size : {}'.format(file_size))
                socket.close()
            else:
                print('response ', content_or_response)
                socket.send(content_or_response)
                print('Proxy has sent the response from the server.')
                socket.close()
    else:
        # reply "HTTP Bad Request" (code 400)
        socket.send(b'400 Bad Request')
        print(b'400 Bad Request')
        socket.close()


def main():
    # Init socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        server_socket.bind((IP, PORT))
        print('Bind is OK')
    except socket.error as msg:
        print(msg)
        sys.exit()

    server_socket.listen(10)

    print('Proxy Server ready to receive')
    
    while True:
        connection_socket, address = server_socket.accept()

        childThread = threading.Thread(target=thread_function, args=(connection_socket, address))
        childThread.start()
        #childThread.join()

        #connection_socket.close()

    server_socket.close()
    sys.exit()


if __name__ == '__main__':
    main()

