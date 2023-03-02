import socket

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

client_socket = socket.socket()
client_socket.connect((HOST, PORT))

client_socket.sendall('CMD:PRINTFILE'.encode())

# wait for an answer
bytes_read = client_socket.recv(1024)
received_data = bytes_read.decode()

print(f'server send: {received_data}')
if received_data == 'READY':
    print('server is ready to accept the file... sending...')
    client_socket.sendall('STARTFILE'.encode())

    with open('send/data.xml', 'rb') as f:
        client_socket.sendall(f.read())

    client_socket.sendall('ENDFILE'.encode())

    print('File send. Waiting for an answer...')

    # wait for an answer
    bytes_read = client_socket.recv(1024)
    received_data = bytes_read.decode()

    if received_data == 'OK':
        print('Server accknowledged receival of file. Sending printer name...')
        client_socket.sendall('PRINTER:my-printer'.encode())
        client_socket.sendall('ENDCMD'.encode())
    
        bytes_read = client_socket.recv(1024)
        received_data = bytes_read.decode()

        if received_data == 'ENDCMD':
            print('command succesfully executed on server.')

client_socket.close()