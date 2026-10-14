# Python program to implement server side of chat room.
import socket
import select
import sys

#initiate server socket with the TCP connection
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# binding the server socket with the localhost as ip and port number
port=5605
server_socket.bind(('127.0.0.1',port)) # '127.0.0.1' is the localhost in ipv4

# make the socket listen on this port
server_socket.listen(3) #makes it queue up to 3 pending connections

# listening forever
while True :
    print("waiting for a connection")
    client,add = server_socket.accept() # when a connection to a client is accepted
    # Break the connection when 'CLOSE SOCKET' is recieved
    print("connection started")

    while True:
        try:
            # recieve meassage as bytes
                    recBytes = client.recv(1024) #will only accept 1024 bytes at a time, but should be put in a loop to wait for a delimiter
            
                    # decoding the bytes into characters
                    msg = recBytes.decode()
                    print("CLIENT: "+msg)
            
                    #Check if the message was 'CLOSE SOCKET' to close connection
                    if(msg=="CLOSE SOCKET" or msg == ""): #this is when a connection is terminated cleanly so server recieves tcp FIN packet
                        print("connection closed")
                        client.close()
                        break
                    else: # otherwise capitalize the decoded message
                        returnMsg = msg.upper()
                        print("SERVER: "+returnMsg)
            
                    # send the response as bytes again
                    returnMsg = returnMsg.encode()
                    client.send(returnMsg)
        except ConnectionResetError, BrokenPipeError:  # this is when the client process is terminated forcefully so a RST packet is sent which gives this error
              print("client terminated unexpectedly")
              break