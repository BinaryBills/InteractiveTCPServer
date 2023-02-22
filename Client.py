#Author: BinaryBills
#Creation Date: February 2, 2023
#Date Modified: February 16, 2023
#Purpose: Encapsulation of Client interactions with the TCP server
import sys
import socket

#Commandline Arguments
if len(sys.argv) == 1:
   print("Specify IP as commandline argument")
   quit()

def noEmptyString(prompt):
    while True:
     userInput = input(prompt)
     if len(userInput) > 0:
        return userInput
     print("Empty Strings are not allowed!")


#Information Required by Project
FORMAT = 'ascii'
commands = ['MSGGET', 'MSGSTORE', 'QUIT', 'SHUTDOWN']
welcomeMsg = "Welcome to the YAMOTD Server!\n MSGSTORE Command sets server message! \n MSGGET Command displays server message \n QUIT disconnects you from the server! \n SHUTDOWN TURNS OFF SERVER FOR ALL CLIENTS!\n\n"

#Prompts user to unqiuely identify themselves
print(welcomeMsg)
username = noEmptyString("Choose a username for this session: ")

#Client connecting to the server
SERVER_IP = sys.argv[1]
SERVER_PORT = 50754
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverStatus = "RESUME"

def clientToServer():
    """Deals with the Client's interactions with the server"""
    while True:
        serverStatus = client.recv(1024).decode(FORMAT)
        msg = noEmptyString("Please enter a command: ")
        message = msg
        client.send(msg.encode(FORMAT))
        try:
            #MSGGET command
            if msg == commands[0]:
                 msgOfDay = client.recv(1024).decode(FORMAT)
                 print(msgOfDay)
            #MSGSTORE command
            elif msg == commands[1]:
               successMsg1 = client.recv(1024).decode(FORMAT)
               print(successMsg1)
               newServerMsg = noEmptyString("Input new Server message: ")
               client.send(newServerMsg.encode(FORMAT))
               successMsg2 = client.recv(1024).decode(FORMAT)
               print(successMsg2)
            #QUIT command
            elif msg == commands[2]:
               successMsg = client.recv(1024).decode(FORMAT)
               print(successMsg)
               client.close()
               print("Goodbye! Thanks for using the program.")
               break
            #SHUTDOWN command
            elif msg == commands[3]:
                passwdMsg = client.recv(1024).decode(FORMAT)
                print(passwdMsg)
                passwd = noEmptyString("Input the server Password: ")
                client.send(passwd.encode(FORMAT))
                response = client.recv(1024).decode(FORMAT)
                print(response)
            #Commands not handled by program   
            else:
                client.send(message.encode(FORMAT))
                print(message,"\n")

            if serverStatus == "CLOSE":
               print("Server has been closed! Goodbye!")
               client.close()
               break
           

        except:
            #If a client produces an error, we will cut the connection.
            client.close()
            print("You have disconnected from the server...")
            break
        
try:
 client.connect(SERVER_ADDRESS)
 client.send(username.encode(FORMAT)) 
 name1 = client.recv(1024).decode('ascii')
 name3 = client.recv(1024).decode('ascii')
 print(name3)
 clientToServer()
except:
    client.close()
    print("Server is not on!!")
    
 