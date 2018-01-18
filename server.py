# Python program to implement server side of chat room.
import socket
import select
import sys
from _thread import *
import pickle


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
 
IP_address = str(sys.argv[1])
 
Port = int(sys.argv[2])

server.bind((IP_address, Port))
 
server.listen(100)
 
list_of_clients = []
 
def clientthread(conn, addr):
 
    conn.send("Welcome to this chatroom!".encode())
 
    while True:
            try:
                message = pickle.loads(conn.recv(2048))

                if message:

                    print ("<" + addr[0] + "> " + str(message[0]))
 
                    message_to_send = "<" + addr[0] + "> " + str(message[0])
                    broadcast(message_to_send,message[1:],conn)
 
                else:
                    remove(conn)
 
            except:
                continue
 
def broadcast(message, recipients,conn):
    for client in list_of_clients:
        if client[1] in recipients and client[0]!=conn:
            try:
                client[0].send(message.encode())
            except:
                client[0].close()
 
                remove(client[0])
 
def remove(connection):
    for i in list_of_clients:
        if i[0]==connection:
            list_of_clients.remove(i)
            break
 
while True:
 
    conn, addr = server.accept()
 
    list_of_clients.append([conn,addr[0]])
 
    print (addr[0] + " connected")
 
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()