from socket import *
import time

server_name = 'localhost'
server_port = 8000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

request = input('Waiting for user command :')
client_socket.send(request.encode())

start_time = time.time()
while 1:
    response = client_socket.recv(1024)
    if not response:
        break
    print('From server: ', response.decode())
end_time = time.time()
rtt = end_time - start_time

print('RTT: ', rtt)





client_socket.close()

