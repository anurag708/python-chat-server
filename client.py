import socket
import select
import sys
import pickle


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.connect((IP_address, Port))

 
while True:

    sockets_list = [sys.stdin, server]
 
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048).decode()
            sys.stdout.write(message+'\n')
            sys.stdout.flush()
        else:
            message = [sys.stdin.readline()]
            sys.stdin.flush()
            message+=sys.stdin.readline().split()
            
            if len(message)<2:
                print("Please enter a valid receiver\n")
            else:
                sent=pickle.dumps(message)
                server.send(sent)
                sys.stdout.write("<You>")
                sys.stdout.write(message[0])
            sys.stdout.flush()

server.close()