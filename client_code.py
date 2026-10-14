# Python program to implement client side of chat room.
import socket
import select
import sys

PORT = 5605
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
DISCONNECT_MSG = "CLOSE SOCKET"
ERROR_MSG = "maximum connections have been reached, try again later :)"

#initiate Client socket with the TCP connection
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


# try to connect to the server with associated port and id
client_socket.connect(ADDR) #'127.0.0.1' is the localhost in ipv4
#dont need to bind() the socket object to a real socket because connect() will assign you to any socket by default
#and you dont need to know the socket number because the client is the one reaching out to the server so you need to know the server to reach out
#the arguments of connect() are the IP and port numer of the server process NOT client

# open a connection until sending CLOSE SOCKET
while True:
    message=input("enter your message: ")

    # send message as bytes
    message = message.encode()
    client_socket.send(message)

    #recieve respose if exists
    try:
        response = client_socket.recv(1024).decode()
    except(ConnectionAbortedError, ConnectionResetError, BrokenPipeError): #handles the case where N clients are exceeded and the connection automatically closes from server side
        print(ERROR_MSG)
        print("connection closed")
        break

    print("SERVER: "+response)
    if(response == ''):
        print("connection closed")
        client_socket.close()
        break