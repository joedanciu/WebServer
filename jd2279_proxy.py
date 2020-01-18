#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
import threading
import _thread
from socket import socket as Socket
import re


# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


def http_handle(connection_socket, client_address):
    request = connection_socket.recv(1024).decode('ascii')
    # parse the first line
    first_line = request.split('\n')[0]
    #print(first_line)

    # get url
    url = first_line.split(' ')[1]
    realurl = url[7:]
    print(realurl)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((realurl, 80))
    s.send(request.encode('ascii'))
    print("Sending request to " + realurl + "...")

    reply = ""
    while reply == "":
        reply += s.recv(1024).decode("ascii")
    return reply


#GET http://example.com HTTP/1.0

def main():
    # Command line arguments. Use a port > 1024 by default so that we can run
    # without sudo, for use as a real server you need to use port 80.
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int, help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.

        # Set socket options
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to port
        server_socket.bind(('', 2080))

        # Have socket listen
        server_socket.listen(0)

        print("server ready")

        while True:
            connection_socket, client_address = server_socket.accept()
            d = threading.Thread(name=str(client_address), target=http_handle, args=(connection_socket, client_address))
            d.setDaemon(True)
            print("Starting Thread " + d.name)
            d.start()


if __name__ == "__main__":
    sys.exit(main())