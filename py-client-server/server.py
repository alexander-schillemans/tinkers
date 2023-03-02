import socket

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

server_socket = socket.socket()
server_socket.bind((HOST, PORT))

server_socket.listen(5)

while True:
    client_socket, address = server_socket.accept()
    print(f'{address} connected')
    cmd = None
    last_recv = False

    while True:
        bytes_read = client_socket.recv(1024)
        if not bytes_read:
            break
        
        print(f'{address} send: {bytes_read}')
        received_data = bytes_read.decode()

        if 'ENDCMD' in received_data:
            last_recv = True
            received_data = received_data.replace('ENDCMD', '')
        
        if 'CMD' in received_data:
            if cmd:
                print('previous cmd has not been terminated yet. Skipping this data...')
                continue
            
            cmd = received_data.split(':')[1]
            print(f'received cmd: {cmd}')

            client_socket.sendall('READY'.encode())

        if cmd:
            if cmd == 'PRINTFILE':

                if received_data == 'STARTFILE':
                    print('received STARTFILE, waiting for file data...')
                    with open('received/data.xml', 'wb') as f:
                        while True:
                            bytes_read = client_socket.recv(1024)

                            if bytes_read.find(b'ENDFILE') != -1:
                                print('received ENDFILE')
                                f.write(bytes_read.replace(b'ENDFILE', b''))
                                client_socket.sendall('OK'.encode())
                                break

                            f.write(bytes_read)
                
                if 'PRINTER' in received_data:
                    printer = received_data.split(':')[1]
                    print(f'client has given a printer: {printer}')

                    
        if last_recv:
            client_socket.sendall('ENDCMD'.encode())
            cmd = None
            client_socket.close()
            last_recv = False
            break