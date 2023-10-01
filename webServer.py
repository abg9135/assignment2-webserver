# import socket module
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
  
    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        
        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]
            
            # Open the client requested file.
            with open(filename[1:], 'rb') as f:
                outputdata = f.read()
            
            # Create the HTTP response message with headers
            response = b"HTTP/1.1 200 OK\r\n"
            response += b"Content-Type: text/html; charset=UTF-8\r\n"
            response += b"Content-Length: " + str(len(outputdata)).encode() + b"\r\n"
            response += b"\r\n"  # blank line
            response += outputdata

            # Send the response back to the client
            connectionSocket.send(response)
            connectionSocket.close()
            
        except FileNotFoundError:
            # File not found, send 404 response
            not_found_response = b"HTTP/1.1 404 Not Found\r\n"
            not_found_response += b"Content-Type: text/html; charset=UTF-8\r\n"
            not_found_response += b"\r\n"  # blank line
            not_found_response += b"<html><body><h1>404 Not Found</h1></body></html>"
            connectionSocket.send(not_found_response)
            connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
