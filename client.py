from socket import *
import time

# port number
server_name = 'localhost'
server_port = 8080
# connection to server
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

request = input('Waiting for user command :')
client_socket.send(request.encode())

# calculation of RTT
start_time = time.time()
# waits for response from server
while 1:
    response = client_socket.recv(1024)
    if not response:
        break
    print('From server: ', response.decode())
end_time = time.time()
rtt = end_time - start_time

print('RTT: ', rtt)





client_socket.close()

