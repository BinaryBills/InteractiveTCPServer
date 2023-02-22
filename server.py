#Author: BinaryBills
#Creation Date: February 2, 2023
#Date Modified: February 18, 2023
#Purpose:This server implements the YAMOTD protocol. 
#It communicates with clients using TCP sockets and performs 
#the MSGSTORE, MSGGET, QUIT, and shutdown functionalities.

from multiprocessing.connection import Client
import threading
import socket
import time

#Information Required by Project
FORMAT = 'ascii'
global msgOfDay
msgOfDay = "An apple a day keeps the doctor away\n"
commands = ['MSGGET', 'MSGSTORE', 'QUIT', 'SHUTDOWN']
successMsg = "200 OK\n"
failureMSG = "400 Bad Request! NOT TERMINATED WITH ENDLINE\n"
passwdMSG = "300 PASSWORD REQUIRED!\n"
wrongpassMSG = "301 WRONG PASSWORD\n"
serverStatus = "RESUME"
passwd = "123!abc"

#Gets the IP address of the host executing the script and chooses the specified port on the host
SERVER_IP = socket.gethostbyname(socket.gethostname()) 
SERVER_PORT = 50754
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

#Creates a list of the clients connected to the server and usernames chosen by them.
clients = []
usernames = []

#Creates an internet socket for TCP connections then listens for incoming connections from clients
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(SERVER_ADDRESS)
SERVER.listen()

def printUserMessage(client,msg):
    """Prints messages received from the client to the server"""
    global clients
    index = clients.index(client)
    username = usernames[index]
    print(f'{username} sent the message: ', msg)
         
def serverShutdown(clients):
    """Thread that handles shutting down the server"""
    while True:
        if (serverStatus == "CLOSE"):
            if (len(clients) < 1):
                break

    SERVER.close()

def OneClient(client):
    """Encapsulates the execution of one particular client"""
    while True:
        global msgOfDay
        global serverStatus
        try:
            client.send(serverStatus.encode(FORMAT))
            clientMessage = client.recv(1024)
            msg = clientMessage.decode(FORMAT)

            #User executes MSGGET command
            if (msg == commands[0]):
                printUserMessage(client,msg)
                strToSend = successMsg + msgOfDay
                time.sleep(2)
                client.send(strToSend.encode(FORMAT))

            #User executes MSGGSTORE command
            elif (msg == commands[1]):
               printUserMessage(client,msg)
               time.sleep(2)

               client.send(successMsg.encode(FORMAT))

               clientInput = client.recv(1024).decode(FORMAT)
               printUserMessage(client,clientInput)
               msgOfDay = clientInput + "\n"
               client.send(successMsg.encode(FORMAT))
          
            #User executes QUIT command
            elif (msg == commands[2]):
                printUserMessage(client,msg)
                client.send(successMsg.encode(FORMAT))
                raise Exception("Quiting the program...")

            #User executes SHUTDOWN command
            elif (msg == commands[3] ):
                printUserMessage(client,msg)
                client.send(passwdMSG.encode(FORMAT))
                clientInput = client.recv(1024).decode(FORMAT)
                printUserMessage(client,clientInput)

                if clientInput == passwd:
                    client.send(successMsg.encode(FORMAT))
                    serverStatus = "CLOSE"
                else:
                    client.send(wrongpassMSG.encode(FORMAT))
            
                    
            #User inputs anything that isn't a qualified command        
            else:
                 userMSG = client.recv(1024).decode(FORMAT)
                 printUserMessage(client, userMSG)
               
            if serverStatus == "CLOSE":
                raise Exception("Shutdown has been triggered clients...")
            
        except:
         #If a client produces an error or someone shutdown server, we will cut the connection to that particular client and end the thread.
         index = clients.index(client)
         clients.remove(client)
         client.close()
         username = usernames[index]
         print("Current People connected:", len(clients))
         print(f'{username} has left the server!')
         usernames.remove(username)
         break

def OneServer():
    global serverStatus
    global clients
    """Encapsulates the execution of the server"""
    
    while True:
       try:
       
        client, address = SERVER.accept()
        print(f'Connected with {str(address)}')
        
        #We prompt client for username then receive it!
        client.send('USERNAMESET'.encode(FORMAT))
        username = client.recv(1024).decode(FORMAT)
        usernames.append(username)
        clients.append(client)
        print(len(clients))
        print(f'Nickname of the client is {username}')
        
        #announce(f'{username} joined the server!\n'.encode(FORMAT))
        client.send('Connected to the server\n'.encode(FORMAT))

        #Threading to handle multiple users and several requests at same time
        thread = threading.Thread(target=OneClient, args= (client,))
        thread.start()

        #Threading to handle server shutdown
        thread3 = threading.Thread(target=serverShutdown, args= (clients,))
        thread3.start()
       except:
           break
    
  
serverStatus = "RESUME"
print("Server is listening on", SERVER_IP)

OneServer()