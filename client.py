import socket

PORT = 5000
FORMAT = 'utf-8'
SERVER = "127.0.0.2"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def signin():
    ...

def send(msg):
    messege = msg.encode(FORMAT)
    client.send(messege)