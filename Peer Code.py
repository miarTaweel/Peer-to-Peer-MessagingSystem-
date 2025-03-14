"""
Miar Taweel


"""

import re
import socket
import threading
from datetime import datetime

def get_ip_address(): # A function that finds the Ip Address of the current peer
    try:
        # Create a UDP socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))# Connect to a remote server (doesn't actually connect, just gives us the local IP)
        ip_address = s.getsockname()[0] # Get the local IP address
        s.close()  # Close the socket

        return ip_address
    except Exception as e:
        print("Error:", e)
        return None



#Used Arrays
messages = []
clients =[]
last=[]
lastR=[]


PORT =5050 #The chosen port number
MYIP= get_ip_address()#Finding the Ip address of this peer
SERVER = '' #Enter here The broadcast Ip of the Lan Network
ADDR = ('', PORT) #bind the port number with an appropriately chosen IP

#Socket Constuction
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#creates the UDP socket
server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)#Giving broadcast permisson
server.bind(ADDR)# binding the socket to our identity

#Reading the Peers' Data
fname=input ("Enter First name:")
lname=input ("Enter Last name:")

print("-------Start Chat----------")


def recieve():#A function that recieves the messgaes arriving at this peer
    global name
    while True:
        try:
            message,addr= server.recvfrom(1024) # Recieving the data with buffer size of 1024
            current_time = datetime.now()
            time = current_time.strftime("%H:%M:%S")# Extracting the formatted time

            if(addr!=(MYIP,PORT)): #Not Recieving the message if the address of the sender is equal to the address of the receiving peer

                if message.decode().startswith("NAME:"):#Reading the information of the other sending peers
                    components = message.decode().split()
                    name= components[1] +" " +components[2]

                if not message.decode().startswith("NAME:"):
                    messages.insert(0, (message, addr,time))  # putting the messages in the messages array


                if addr not in [client[0] for client in clients]:  # checking if addr is present in the clients list
                    clients.append((addr, name))  # appending the (addr, name) tuple to the clients list

            if not message.decode().startswith("NAME:"):
                z=0
                lastR.clear()
                if clients and messages: #Checking if any messages have been recieved
                    print("")
                    print(fname,lname,"'s Last Recieved Messages: ")

                for client in clients:#A loop that prints the last recieved message from each user
                    for m in messages:
                       if(client[0]==m[1]):
                           lastR.insert(0, (client[1], m[2],m[0]))
                           break
                # Sorting the last recieved messages based on the time (the last arriving message on top)
                last = sorted(lastR, key=lambda x: x[1], reverse=True)

                # Printing the last recieved messages
                for l in last:
                    z = z + 1
                    print(z,".Message Received from",l[0],"at",l[1])

        except:
            pass


#Using multithreading to keep the peer listening to recieve messages at any time
t1 = threading.Thread(target=recieve)
t1.start()


while True: #An ongoing loop to Send the inputted messages at any time

    # Reading the message wanted to be sent
    m= input("")
    pattern = r"(\d+)D"
    last = sorted(lastR, key=lambda x: x[1], reverse=True)

    # Checking if a display message command is entered
    match = re.match(pattern, m)
    if match:
        number_before_d = int(match.group(1))
        #Checking if the display command's number exists in the messages
        if number_before_d <= len(last):
            print("The Message :", last[number_before_d-1][2].decode())
        else:
            print("->User Doesn't Exist.....")
    else:
        #Sending the message with the peers information
        server.sendto(f"NAME: {fname} {lname} ".encode(), (SERVER, PORT))
        server.sendto(f"{m}".encode(), (SERVER,PORT))
        print("The message(",m,") has been sent")
