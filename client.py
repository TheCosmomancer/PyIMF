import socket
from tkinter import *

from peewee import Window

PORT = 5000
FORMAT = 'utf-8'
SERVER = "127.0.0.2"
ADDR = (SERVER,PORT)
HEADER = 64
DISCONNECT = '!disc!!'
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def signin():
    ...

def send(msg):
    messege = msg.encode(FORMAT)
    messege_len = len(messege)
    messege_len = str(messege_len).encode(FORMAT)
    messege_len += b' ' * (HEADER - len(messege_len))
    client.send(messege_len)
    client.send(messege)

def connect():
    client.connect(ADDR)
def click():
    print(1)
def main():
    window = Tk()
    photo = PhotoImage(file='nix.png')
    window.geometry('1280x720')
    window.title('IMF')
    window.config(background='grey')
    label = Label(window,text='hello',font=('arial',40,'bold'),fg = 'blue',bg = 'grey',relief=RAISED,bd=10,padx=20,pady=20)
    label.place(x=0,y=0)
    button = Button(window,text='button',command=click,state=ACTIVE,image=photo,compound=LEFT,activebackground='blue',activeforeground='green',font=('comic sans',40,'bold'),fg = 'blue',bg = 'grey',relief=RAISED,bd=10,padx=20,pady=20)
    button.place(x=200,y=0)
    window.mainloop()
    

if __name__ == '__main__':
    main()
