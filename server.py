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

# usermesseges = list(Messege.select().where(Messege.receiver == user))

def clientHandel(conn,addr):
    user = None
    openfile = None
    print(f'{addr} connected')
    while True:
        messege = reciveMessege(conn)
        if messege == DISCONNECT:
            print(f'{addr} disconnected')
            break
        elif messege == 'getmessages':
            messagelist = list(Messege.select().where(Messege.receiver == user))
            lenmessagelist = len(messagelist)
            messagelistvar = 0
            if lenmessagelist > 0:
                sendMessege(messagelist[messagelistvar].sender+'¶'+messagelist[messagelistvar].content,conn)
            else:
                sendMessege('¶',conn)
        elif messege == 'lastmessage':
            if messagelistvar -1 >= 0:
                messagelistvar -= 1
                sendMessege(messagelist[messagelistvar].sender+'¶'+messagelist[messagelistvar].content,conn)
            else:
                sendMessege('¶',conn)
        elif messege == 'nextmessage':
            if messagelistvar +1 < lenmessagelist:
                messagelistvar += 1
                sendMessege(messagelist[messagelistvar].sender+'¶'+messagelist[messagelistvar].content,conn)
            else:
                sendMessege('¶',conn)
        else:
            messege = messege.split('¶')
            if messege[0] == 'login':
                user = User.signin(messege[1],messege[2])
                if user != None:
                    if user.accessLevel > 3:
                        sendMessege('sec',conn)
                    else:
                        sendMessege('agent',conn)
                else:
                    sendMessege('failed',conn)
            elif messege[0] == 'newagent':
                try:
                    User.add(firstName=messege[1],lastName=messege[2],codename=messege[3],accessLevel=int(messege[4]),password=messege[5])
                    sendMessege('agent',conn)
                except:
                    sendMessege('failed',conn)
            elif messege[0] == 'deleteagent':
                try:
                    User.removeuser(messege[1])
                    sendMessege('agent',conn)
                except:
                    sendMessege('failed',conn)
            elif messege[0] == 'usermesseage':
                try:
                    Messege.sendMessege(user.codename,messege[1],messege[2])
                    sendMessege('agent',conn)
                except:
                    sendMessege('failed',conn)
            elif messege[0] == 'broadcastmesseage':
                try:
                    Messege.broadcast(user.codename,messege[1])
                    sendMessege('agent',conn)
                except:
                    sendMessege('failed',conn)
            elif messege[0] == 'openfile':
                try:
                    temp = File.get(File.name == messege[1])
                    assert int(temp.level) <= user.accessLevel
                    openfile = messege[1]
                    sendMessege(File.decrypt(openfile),conn)
                except:
                    sendMessege('¶',conn)
            elif messege[0] == 'saveopenfile':
                File.edit(openfile,messege[1])
            elif messege[0] == 'deleteopenfile':
                File.remove(openfile)
            elif messege[0] == 'newafile':
                try:
                    File.addOrCreate(messege[1],messege[2])
                    sendMessege('agent',conn)
                except:
                    sendMessege('failed',conn)

    conn.close()
def reciveMessege(conn):
    messege_len = conn.recv(HEADER).decode(FORMAT)
    if messege_len:
        messege_len = int(messege_len)
        messege = conn.recv(messege_len).decode(FORMAT)
        return messege
    return None
def sendMessege(msg,conn):
    messege = msg.encode(FORMAT)
    messege_len = len(messege)
    messege_len = str(messege_len).encode(FORMAT)
    messege_len += b' ' * (HEADER - len(messege_len))
    conn.send(messege_len)
    conn.send(messege)
def start():
    server.listen()
    print(SERVER)
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=clientHandel,args=(conn,addr))
        thread.start()


start()