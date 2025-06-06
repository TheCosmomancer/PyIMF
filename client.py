import socket
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from peewee import *
import Levenshtein
import nltk
PORT = 5000
FORMAT = 'utf-8'
SERVER = "127.0.0.2"
ADDR = (SERVER,PORT)
HEADER = 64
DISCONNECT = '!disc!!'
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
nltk.download('words')
from nltk.corpus import words
engVocab = set(words.words())
def spellcheckLevenshtein(word):
    if word in engVocab:
        return word
    else:
        distances = [(vocab_word,Levenshtein.distance(word,vocab_word))for vocab_word in engVocab]
        closestMatch = min(distances,key = lambda x: x[1])
        if closestMatch[1] < 3:
            return closestMatch[0]
        else:
            return word
def autocorrect(string):
    backup = string
    for char in string:
        if char != ' ' and char != '\n' and char.isalpha() != True:
            backup = backup.replace(char,'')
    string,backup = backup,string
    string = string.split('\n')
    ret = ''
    for line in string: 
        line = line.split(' ')
        temp = ''
        for word in line:
            temp += spellcheckLevenshtein(word) + ' '
        ret += temp.strip() + '\n'
    ret = ret.strip()
    return ret

def sendMessege(msg):
    messege = msg.encode(FORMAT)
    messege_len = len(messege)
    messege_len = str(messege_len).encode(FORMAT)
    messege_len += b' ' * (HEADER - len(messege_len))
    client.send(messege_len)
    client.send(messege)
def reciveMessege():
    messege = None
    while messege == None:
        messege_len = client.recv(HEADER).decode(FORMAT)
        if messege_len:
            messege_len = int(messege_len)
            messege = client.recv(messege_len).decode(FORMAT)
            return messege
def click():
    with open(filedialog.askopenfilename(filetypes=(('text files','*.txt'),('all files','*.*'))),'r') as f:
        print(f.read())
def main():
    def loginAttempt():
        sendMessege('login¶'+loginUsername.get()+'¶'+loginPassword.get())
        answer = reciveMessege()
        if answer == 'agent':
            sendMessege('getmessages')
            firstmessage = reciveMessege()
            if firstmessage == '¶':
                firstmessage = 'you dont have any messaages'
            else:
                firstmessage.split('¶')
                print(firstmessage[0],firstmessage[1])
            def sendusermessege():
                sendMessege('usermesseage¶'+reciver.get()+'¶'+textmessege.get('1.0',END))
                messegesendanswer = reciveMessege()
                if messegesendanswer == 'agent':
                    Label(sendTab,text='messege sent').pack()
                else:
                    Label(sendTab,text='unable to send messege please try again').pack()
            def broadcastmessege():
                sendMessege('broadcastmesseage¶'+broadcasttext.get('1.0',END))
                broadcastanswer = reciveMessege()
                if broadcastanswer == 'agent':
                    Label(broadcastTab,text='broadcast sent').pack()
                else:
                    Label(broadcastTab,text='unable to broadcast messege please try again').pack()

            def searchfile():
                sendMessege('openfile¶'+filename.get())
                openfileanswer = reciveMessege()
                if openfileanswer != '¶':
                    def savefileandexit():
                        sendMessege('saveopenfile¶'+text.get('1.0',END))
                        topLevel.destroy()
                    def discardfileandexit():
                        topLevel.destroy()
                    fileContent = openfileanswer
                    topLevel = Toplevel(mainwindow)
                    text = Text(topLevel)
                    text.pack()
                    text.insert('1.0',fileContent)
                    savebutton = Button(topLevel,text='save and exit',command=savefileandexit)
                    savebutton.pack()
                    discardbutton = Button(topLevel,text='discard and exit',command=discardfileandexit)
                    discardbutton.pack()
                else:
                    Label(filesTab,text='unable to open file').pack()
            def correctmessege():
                todo = textmessege.get('1.0',END).strip()
                todo = autocorrect(todo)
                textmessege.delete('1.0',END)
                textmessege.insert('1.0',todo)
            def correctbraodcast():
                todo = broadcasttext.get('1.0',END).strip()
                todo = autocorrect(todo)
                broadcasttext.delete('1.0',END)
                broadcasttext.insert('1.0',todo)
            def gotolastmessage():
                sendMessege('lastmessage')
                answer = reciveMessege()
                if answer != '¶':
                    answer.split('¶')
                    print(firstmessage[0],firstmessage[1])
                    messagetextsender.config(text=answer[0])
                    messagetext.config(text=answer[1])
            def gotonextmessage():
                sendMessege('nextmessage')
                answer = reciveMessege()
                if answer != '¶':
                    answer.split('¶')
                    print(firstmessage[0],firstmessage[1])
                    messagetextsender.config(text=answer[0])
                    messagetext.config(text=answer[1])
            mainwindow = Tk()
            loginWindow.destroy()
            tabman = ttk.Notebook(mainwindow)
            messagesTab = Frame(tabman)
            filesTab = Frame(tabman)
            tabman.add(messagesTab,text='messages')
            tabman.add(filesTab,text='veiw files')
            tabman.pack()
            #veiw files
            Label(filesTab,text='search for a file').pack()
            filename = Entry(filesTab,font = ('Arial',15))
            filename.pack()
            searchfilebutton = Button(filesTab,text='search for file',command=searchfile)
            searchfilebutton.pack()
            #messeges
            messman = ttk.Notebook(messagesTab)
            inboxTab = Frame(messman)
            sendTab = Frame(messman)
            broadcastTab = Frame(messman)
            messman.add(inboxTab,text='see messages')
            messman.add(sendTab,text='send messages')
            messman.add(broadcastTab,text='broadcast a message')
            messman.pack()
            #see messeges
            lastmessagebutton = Button(inboxTab,text='<',command=gotolastmessage)
            lastmessagebutton.pack()
            messagetextsender = Label(inboxTab,text=firstmessage[0])
            messagetextsender.pack()
            messagetext = Label(inboxTab,text=firstmessage[1])
            messagetext.pack()
            nextmessagebutton = Button(inboxTab,text='>',command=gotonextmessage)
            nextmessagebutton.pack()
            #send messeges
            Label(sendTab,text='select a recepiant').pack()
            reciver = Entry(sendTab,font = ('Arial',15))
            reciver.pack()
            textmessege = Text(sendTab,font = ('Arial',15))
            textmessege.pack()
            sendMessegeButton = Button(sendTab,text='send messege',command = sendusermessege)
            sendMessegeButton.pack()
            correctMessegeButton = Button(sendTab,text='autocorrect messege',command = correctmessege)
            correctMessegeButton.pack()
            #send broadcasts
            broadcasttext = Text(broadcastTab,font = ('Arial',15))
            broadcasttext.pack()
            braodcastButton = Button(broadcastTab,text='broadcast messege',command = broadcastmessege)
            braodcastButton.pack()
            correctcastButton = Button(broadcastTab,text='autocorrect messege',command = correctbraodcast)
            correctcastButton.pack()




            mainwindow.mainloop()
        elif answer == 'sec':
            def selectfile():
                filepath = filedialog.askopenfilename(initialdir=os.getcwd(),filetypes=(('text file','*.txt'),('all files','*')))
                filewpath.delete(0,END)
                filewpath.insert(0,filepath)
            def newfile():
                sendMessege('newafile¶'+filewpath.get()+'¶'+str(filelevel.get()+1))
                answer = reciveMessege()
                if answer == 'agent':
                    Label(addfilesTab,text='file created/added').pack()
                else:
                    Label(addfilesTab,text='unable to create/add file please try again').pack()
            def searchfile():
                sendMessege('openfile¶'+filename.get())
                openfileanswer = reciveMessege()
                if openfileanswer != '¶':
                    def savefileandexit():
                        sendMessege('saveopenfile¶'+text.get())
                        topLevel.destroy()
                    def discardfileandexit():
                        topLevel.destroy()
                    def  deletefile():
                        sendMessege('deleteopenfile¶.')
                        topLevel.destroy()
                    fileContent = openfileanswer
                    topLevel = Toplevel(mainwindow)
                    text = Text(topLevel)
                    text.pack()
                    text.insert('1.0',fileContent)
                    savebutton = Button(topLevel,text='save and exit',command=savefileandexit)
                    savebutton.pack()
                    discardbutton = Button(topLevel,text='discard and exit',command=discardfileandexit)
                    discardbutton.pack()
                    deletebutton = Button(topLevel,text='delete file',command=deletefile)
                    deletebutton.pack()
            def makenewagent():
                sendMessege('newagent¶'+firstname.get()+'¶'+lastname.get()+'¶'+newagentcodename.get()+'¶'+str(agentlevel.get()+1)+'¶'+agentpassowrd.get())
                answer = reciveMessege()
                if answer == 'agent':
                    Label(agentTab,text='aget created').pack()
                else:
                    Label(agentTab,text='unable to create agent please try again').pack()
            def deleteagent():
                sendMessege('deleteagent¶'+codename2kill.get())
                answer = reciveMessege()
                if answer == 'agent':
                    Label(deleteagenttab,text='agent deleted').pack()
                else:
                    Label(deleteagenttab,text='unable to delete agent please try again').pack()
            mainwindow = Tk()
            loginWindow.destroy()
            tabman = ttk.Notebook(mainwindow)
            agentTab = Frame(tabman)
            addfilesTab = Frame(tabman)
            filesTab = Frame(tabman)
            deleteagenttab = Frame(tabman)
            tabman.add(deleteagenttab,text='delete agents')
            tabman.add(agentTab,text='add agents')
            tabman.add(addfilesTab,text='add files')
            tabman.add(filesTab,text='veiw files')
            tabman.pack()
            #add files
            Label(addfilesTab,text='select or create a file').pack()
            filewpath = Entry(addfilesTab,font = ('Arial',15))
            filewpath.pack()
            openfile = Button(addfilesTab,text='select file',command=selectfile)
            openfile.pack()
            Label(addfilesTab,text='set the level').pack()
            filelevel = IntVar(addfilesTab)
            for _ in range(3):
                radiobutton = Radiobutton(addfilesTab,text = f'{_+1}',variable=filelevel,value=_)
                radiobutton.pack()
            addfilebutton = Button(addfilesTab,text='add file',command=newfile)
            addfilebutton.pack()
            #veiw files
            Label(filesTab,text='search for a file').pack()
            filename = Entry(filesTab,font = ('Arial',15))
            filename.pack()
            searchfilebutton = Button(filesTab,text='search for file',command=searchfile)
            searchfilebutton.pack()
            #add agents
            Label(agentTab,text="agent's first name:").pack()
            firstname = Entry(agentTab,font = ('Arial',15))
            firstname.pack()
            Label(agentTab,text="agent's last name:").pack()
            lastname = Entry(agentTab,font = ('Arial',15))
            lastname.pack()
            Label(agentTab,text="agent's code name:").pack()
            newagentcodename = Entry(agentTab,font = ('Arial',15))
            newagentcodename.pack()
            Label(agentTab,text="agent's password:").pack()
            agentpassowrd = Entry(agentTab,font = ('Arial',15))
            agentpassowrd.pack()
            Label(agentTab,text='select agent access level').pack()
            agentlevel = IntVar(agentTab)
            for _ in range(3):
                radiobutton = Radiobutton(agentTab,text = f'{_+1}',variable=agentlevel,value=_)
                radiobutton.pack()
            makeagentbutton = Button(agentTab,text='create agent',command=makenewagent)
            makeagentbutton.pack()
            #delete agents
            Label(deleteagenttab,text="agent's code name:").pack()
            codename2kill = Entry(deleteagenttab,font = ('Arial',15))
            codename2kill.pack()
            deleteagentbutton = Button(deleteagenttab,text='delete agent',command=deleteagent)
            deleteagentbutton.pack()






            mainwindow.mainloop()
        else:
            Label(loginWindow,text='login failed, please try again').pack()
    loginWindow = Tk()
    loginUsername = Entry(loginWindow,font = ('Arial',15))
    loginUsername.pack()
    loginPassword = Entry(loginWindow,font = ('Arial',15))
    loginPassword.pack()
    loginButton = Button(loginWindow,text='Log in',command=loginAttempt)
    loginButton.pack()
    
    loginWindow.mainloop()
    

if __name__ == '__main__':
    main()
    sendMessege(DISCONNECT)