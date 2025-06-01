import socket
import threading
from classes import *

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = '!disc!!'
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def clientHandel(conn,addr):
    print(f'{addr} connected')
    while True:
        messege_len = conn.recv(HEADER).decode(FORMAT)
        if messege_len:
            messege_len = int(messege_len)
            messege = conn.recv(messege_len).decode(FORMAT)
            if messege == DISCONNECT:
                break
            else:
                ...
    conn.close()
def start():
    server.listen()
    print(SERVER)
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=clientHandel,args=(conn,addr))
        thread.start()


start()