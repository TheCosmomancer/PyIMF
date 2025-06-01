from classes import *
firstname = input('first name: ')
lastname = input('last name: ')
codename = 'Secretary'
accessLevel = 4
password = input ('password: ')
User.add(firstName=firstname,lastName=lastname,codename=codename,accessLevel=accessLevel,password=password)