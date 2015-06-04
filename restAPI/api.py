#!/usr/bin/env python
from flask import Flask
import socket
import sys

app = Flask(__name__)


# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = './uds_socket'
print('connecting to %s' % server_address)
try:
    sock.connect(server_address)
except socket.error as msg:
    print(msg)
    exit(1)


def send_recv(msg):
    tdata = ""
    try:
        # Send data
        message = msg  # 'This is the message.  It will be repeated.'
        print('sending "%s"' % message)
        sock.sendall(message.encode())

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(1024).decode()
            tdata += data
            amount_received += len(data)
            print('received "%s"' % data)
    finally:
        return tdata
    # finally:
    #     print(sys.stderr, 'closing socket')
    #     sock.close()


@app.route('/')
def index():
    m = send_recv('Hello, World!')
    return m
    # return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
