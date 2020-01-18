#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket
import re


# A simple web server

# Issues:
# Ignores CRLF requirement
# Header must be < 1024 bytes
# ...
# probabaly loads more


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
            # Use the server socket as the connection socket and accept incoming requests
            # This is like file IO and you need to open the server socket as the connection socket
            with server_socket.accept()[0] as connection_socket:
                # Save the request received from the connection and decode as ascii
                data_str = connection_socket.recv(1024).decode('ascii')
                request = str(data_str)
                reply = ""
                errorCode = ""
                # Step 1: EXTRACT THE REQUEST LINE
                #### Step1a: Split up the request string by line (\r\n) --> ASSUME: LIST of LINES
                req_array = data_str.split("\r\n")

                #### Step1b: Request line is going to be at index position 0 in our list of lines from Step 1a --> ASSUME: string called req_line
                req_line = req_array[0]

                # Step 2: Extracting the METHOD, URL, and VERSION fields from the Request line
                #### Step2a: Split req_line on spaces --> ASSUME: list of fields
                extract3 = req_array[0].split()

                #### Step2ba: Check the length of list of fields to see if it is 3...if not GENERATE ERROR CODE
                if len(extract3) != 3:
                    errorCode = "400 Bad Request - Not 3"
                else:
                    #### Step2b: METHOD is going to be at index position 0 in list of fields
                    method = extract3[0]
                    #### Step2c: URL is going to be at index position 1 in list of fields
                    url = extract3[1]
                    #### Step2d: VERSION is at index position 2 in list of fields
                    version = extract3[2]

                    methodFlag = False
                    # Step 3: If the values in the Request line are valid, we proceed to check that headers are correctly formatted
                    #### Step3a: Check to see if METHOD is [GET, POST, HEAD, PUT, PATCH, DELETE]: If it is not --> GENERATE ERROR CODE
                    if method == "GET":
                        methodFlag = False
                    elif method == "POST":
                        methodFlag = False
                    elif method == "HEAD":
                        methodFlag = False
                    elif method == "PUT":
                        methodFlag = False
                    elif method == "PATCH":
                        methodFlag = False
                    elif method == "DELETE":
                        methodFlag = False
                    else:
                        errorCode = "400 Error - Bad Method"
                        methodFlag = True
                    if methodFlag == False:
                    #### Step3b: Check to see if VERSION is [HTTP/1.1, HTTP/1.0]: If it is not --> GENERATE ERROR CODE
                        if version == "HTTP/1.1" or version == "HTTP/1.0":
                            #### Step3d: If METHOD is not GET, GENERATE ERROR CODE, otherwise keep going forward
                            if method == "GET":
                                # Step 4: Check if the requested file is available or not
                                if url == "/":
                                    reply = "<!DOCTYPE html> \n <html> \n <body> \n <h1>Simple Web Server</h1> \n <p>I love computer networks!</p> \n </body> \n </html>"
                                else:
                                    errorCode = "404 File Not Found - Please use /"
                            else:
                                errorCode = "503 Service Unavailable - That Method is not implemented yet"
                                #### Step4a: Check to see if the file exists: If it does not --> GENERATE ERROR CODE

                                # Step 5: Send the response
                                #### Step5a: If an error code was generated, send the error code
                                #### Step5b: If no error code was generated, serve the default HTML
                        else:
                            errorCode = "505 HTTP Version Not Supported - Please use 1.0 or 1.1"
                    # Generate a reply by sending the request received to http_handle()
                    # CS460_TODO

                    # Use the connection socket to send the reply encoded as bytestream
                    # CS460_TODO
                if errorCode == "":
                    print("\n\nReceived request")
                    print("======================")
                    print(request.rstrip())
                    print("======================")
                    print("\n\nReplied with")
                    print("======================")
                    print("200 OK \n")
                    connection_socket.send(reply.encode('ascii'))
                    print(reply.rstrip())
                    print("======================")
                else:
                    print("\n\nReceived request")
                    print("======================")
                    print(request.rstrip())
                    print("======================")
                    print("\n\nReplied with")
                    print("======================")
                    connection_socket.send(errorCode.encode('ascii'))
                    print(errorCode)
                    print("======================")


if __name__ == "__main__":
    sys.exit(main())