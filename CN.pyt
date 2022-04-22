from email import message
from operator import truediv
from pprint import pprint
import socket
import threading
from urllib import request

HEADER = 4096
PORT = 5378
FORMAT = 'UTF-8'
SERVER = "143.47.184.219"
host_port = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host_port))

login = input("What's yours nickname?\n")
string_bytes1 = "HELLO-FROM " + login + "\n"
client.sendall(string_bytes1.encode(FORMAT))
data = client.recv(HEADER)
print(data.decode(FORMAT))

while data.decode(FORMAT) == "IN-USE\n":

    client.close()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_port))
    print("Nickname in use, try again\n")
    login = input()
    string_bytes1 = "HELLO-FROM " + login + "\n"
    client.sendall(string_bytes1.encode(FORMAT))
    data = client.recv(HEADER)

print("Nickname choosen - connected to the chat\n")

while True:
    user_data = input("Me: ")

    user_data = client.recv(1024)
    user_data = user_data.decode()
    print(client, ':', user_data)

    if user_data == "!quit":
        client.close()
        print("Disconnected")
        break

    if user_data == "!who":
        user_request = "WHO\n"
        client.sendall(user_request.encode(FORMAT))
        data = client.recv(HEADER)
        print("Currently logged-in users: ")
        print(data.decode(FORMAT))

    if "@" in user_data and len(user_data) > 1:
        nickname = user_data.split(" ", 1)[0].split("@", 1)[1]
        user_message = user_data.split(" ", 1)[1]

        string_bytes2 = "SEND " + nickname + " " + user_message +  "\n"
        client.sendall(string_bytes2.encode(FORMAT))
        data = client.recv(HEADER)
        if data.decode(FORMAT) == "SEND-OK":
            print("Message sent succesfully")
        if data.decode(FORMAT) == "UNKNOWN":
            print("Destination user is not logged in")

