import peewee as pv
import os
from cryptography.fernet import Fernet
import shutil

try:
    os.mkdir("vault")
except:
    pass
os.chdir("vault")
try:
    key = Fernet.generate_key()
    with open('filekey.key', 'xb') as filekey:
        filekey.write(key)
except:
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
fernet = Fernet(key)

db = pv.SqliteDatabase('database.db')


class User():
    firstName = pv.CharField()
    lastName = pv.CharField()
    codename = pv.CharField(unique=True)
    accessLevel = pv.IntegerField()
    password = pv.CharField()

class Messege():
    sender = pv.ForeignKeyField(User,backref='sentMesseges')
    receiver = pv.ForeignKeyField(User,backref='receivedMesseges')
    content = pv.CharField()
    time = pv.DateTimeField()
    
    @staticmethod
    def sendMessege(sender,receiver,content):
        ...

class Broadcast():
    sender = pv.ForeignKeyField(User,backref='sentMesseges')
    content = pv.CharField()
    time = pv.DateTimeField()
    @staticmethod
    def broadcast(sender,content):
        ...

class File():
    @staticmethod
    def encrypt(filename):
        with open(filename, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    @staticmethod
    def decrypt(filename):
        with open(filename, 'rb') as enc_file:
            encrypted = enc_file.read()
        return fernet.decrypt(encrypted)
    @staticmethod
    def create(file,accessLevel):
        try:
            with open(os.path.join(os.getcwd() , file) , 'x') as _ :
                pass
        except:
            return 1
        # attrs = xattr(file)
        # attrs.set("accessLevel", b"{accessLevel}")
        #TODO


    @staticmethod
    def add(filewpath):
        destination = os.getcwd()
        shutil.copy2(filewpath, destination)

    @staticmethod
    def edit(filename,edited):
        with open (filename,'w') as f:
            f.write(edited)

    @staticmethod
    def remove(filename):
        os.remove(filename)