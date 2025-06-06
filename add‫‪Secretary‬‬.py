from classes import *
db.connect()
db.create_tables([User, Messege, File])
firstname = input('first name: ')
lastname = input('last name: ')
codename = 'd'
accessLevel = 4
password = input ('password: ')
User.add(firstName=firstname,lastName=lastname,codename=codename,accessLevel=accessLevel,password=password)