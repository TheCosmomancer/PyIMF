from peewee import *
import os
from cryptography.fernet import Fernet
import shutil
import datetime
import hashlib

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

db = SqliteDatabase('database.db')
class User(Model):
    firstName = CharField()
    lastName = CharField()
    codename = CharField(unique=True)
    accessLevel = IntegerField()
    password = CharField()

    @staticmethod
    def add(firstName,lastName,codename,accessLevel,password):
        try:
            h = hashlib.sha256()
            h.update(password.encode())
            User.create(firstName=firstName,lastName=lastName,codename=codename,accessLevel=accessLevel,password=h.hexdigest())
            return True
        except:
            return False

    @staticmethod
    def signin(codename,password):
        try:
            h = hashlib.sha256()
            h.update(password.encode())
            user = User.get(User.codename == codename)
            assert  user.password == h.hexdigest()
            return user
        except:
            return None
    @staticmethod
    def removeuser (codename):
        user = User.get(User.codename == codename)
        messegaes = list(Messege.select().where(Messege.receiver == user))
        for _ in messegaes:
            _.delete_instance()
        user.delete_instance()
    def __ge__(self,file):
        return self.accessLevel >= File.checkLevel(file)
    class Meta:
        database = db


class Messege(Model):
    sender = CharField()
    receiver = ForeignKeyField(User,backref='receivedMesseges')
    content = CharField()
    time = DateTimeField()
    
    @staticmethod
    def sendMessege(sender,receiver,content):
        receiver = User.get(User.codename == receiver)
        Messege.create(sender=sender,receiver=receiver,content=content,time=datetime.datetime.now())

    @staticmethod
    def broadcast(sender,content):
        for eachuser in list(User.select()):
            Messege.create(sender=sender,receiver=eachuser,content=content,time=datetime.datetime.now())
    class Meta:
        database = db
class File(Model):
    name = CharField(unique=True)
    level = CharField()
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
        return fernet.decrypt(encrypted).decode('utf-8')
    @staticmethod
    def addOrCreate(name,level):
        if '/' not in name:
            try:
                with open(os.path.join(os.getcwd() , name) , 'x') as _ :
                    pass
                File.create(name=name,level=level)
            except:
                raise ReferenceError
        else:
            try:
                destination = os.getcwd()
                shutil.copy2(name, destination)
                name = name.split('/')
                name = name[len(name)-1]
                File.create(name=name,level=level)
            except:
                raise ReferenceError
        File.encrypt(name)

    @staticmethod
    def checkLevel(file):
        try:
            target = File.get(File.name == file)
            return target.level
        except:
            return False 

    @staticmethod
    def edit(filename,edited):
        with open (filename,'w') as f:
            f.write(edited)
        File.encrypt(filename)

    @staticmethod
    def remove(file):
        try:
            target = File.get(File.name == file)
            target.delete_instance()
            os.remove(file)
        except:
            return False
    class Meta:
        database = db