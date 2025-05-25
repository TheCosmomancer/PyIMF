import socket
import threading
from xattr import xattr
import database

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 2#TODO
FORMAT = 'utf-8'
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def func(conn,addr):
    while True:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            ...
    conn.close()
def start():
    server.listen()
    print(SERVER)
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=func,args=(conn,addr))
        thread.start()


start()
def signin(codename,password):
    ...
    return 

def addAgent():
    ...