# Python program to implement client side of chat room.
import socket
import select
import sys

#initiate Client socket with the TCP connection
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


# binding the client socket with the localhost as ip and port number
port=5605
# try to connect to the server with associated port and id
client_socket.connect(('127.0.0.1',port)) #'127.0.0.1' is the localhost in ipv4
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
    response = client_socket.recv(1024)
    if(response == b''):
        print("connection closed")
        client_socket.close()
        break
    response = response.decode()
    print("SERVER: "+response)