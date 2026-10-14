# Python program to implement server side of chat room.
import socket
import select
import sys
import threading
import random

PORT=5605
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
ALLOWED_BYTES = 1024
N_CLIENTS = 15
PENDING = 3
DISCONNECT_MSG = "CLOSE SOCKET"
ACTIVE_CLIENTS = []
COOKIES = []

def start():
    #initiate server socket with the TCP connection
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # binding the server socket with the localhost as ip and port number
    server_socket.bind(ADDR) # '127.0.0.1' is the localhost in ipv4

    # make the socket listen on this port
    server_socket.listen(PENDING) # makes it queue up to 3 pending connections

    # listening forever
    print("waiting for a connection")
    while True :
        client,addr = server_socket.accept()
        # when a connection to a client is accepted, {client} is the new port on the server that is used to communicate with the client device, which is why every time you connect a new client process to it the port will be different
        # and {add} is the client device's socket info (ip and port)
        # Break the connection when 'CLOSE SOCKET' is recieved
        cookie = add_client(addr)
        chatThread = threading.Thread(target= chat, args = (client, addr, cookie))
        chatThread.start()
        print("new connection started")
        print(f"active clients are {ACTIVE_CLIENTS}")
        print(f"their unique IDs are {COOKIES}")


def chat(client, addr, cookie):
    while True:
        try:
            # recieve meassage as bytes
            recBytes = client.recv(ALLOWED_BYTES) #will only accept 1024 bytes at a time, but should be put in a loop to wait for a delimiter
            
            # decoding the bytes into characters
            msg = recBytes.decode(FORMAT)
            print(f"CLIENT {cookie}: "+msg)
            
            #Check if the message was 'CLOSE SOCKET' to close connection
            if(msg== DISCONNECT_MSG or msg == ""): #this is when a connection is terminated cleanly so server recieves tcp FIN packet
                client.close()
                print("connection closed")
                remove_client(addr, cookie)
                break
            else: # otherwise capitalize the decoded message
                returnMsg = msg.upper()
                print("SERVER: "+returnMsg)
            
            # send the response as bytes again
            returnMsg = returnMsg.encode()
            client.send(returnMsg)
        except ConnectionResetError, BrokenPipeError:  # this is when the client process is terminated forcefully so a RST packet is sent which gives this error
            print(f"client {cookie} terminated unexpectedly")
            remove_client(addr, cookie)
            break
    print(f"active clients are {COOKIES}")

def add_client(addr):
    ACTIVE_CLIENTS.append(addr)
    while True:
        cookie = random.randint(1, N_CLIENTS)
        if(cookie not in COOKIES):
            break
    COOKIES.append(cookie)
    return cookie

def remove_client(addr, cookie):
    ACTIVE_CLIENTS.remove(addr)
    COOKIES.remove(cookie)


start()
