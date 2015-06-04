import socket
import os
from gl import utils
global cons
cons = {}


def create_connection():
    server_address = './uds_socket'

    # Make sure the socket does not already exist
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the port
    print('starting up on %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    return sock


@utils.run_async
def reader(connection, client_address):
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024).decode()
            print('received "%s"' % data)
            if data:
                print('sending data back to the client')
                connection.sendall(data.encode())
            else:
                print('no more data from', client_address)
                break
    finally:
        global cons
        if client_address in cons.keys():
            cons.pop(client_address)
        # Clean up the connection
        connection.close()


@utils.run_async
def handle_listen(sock):
    global cons
    while True:
        print("Accepting")
        connection, client_address = sock.accept()
        cons[client_address] = connection
        reader(connection, client_address)
