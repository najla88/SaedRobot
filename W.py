#!/usr/bin/python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from common import id_generator,send_email
import string
import random
import smtplib
import sqlite3
from validate_email import validate_email
import re

def isValidUsername(username):
    return re.search("^[A-z][A-z|\.|\s]+$",username) != None

class Handler:

    def onDeleteWindow(self, *args): 
        Gtk.main_quit(*args)

    def onCreateNewTaskButtonPressed(self, button): 
        print("onCreateNewTaskButtonPressed")

    def onManageUsersAccountsButtonPressed(self, *args):
        id_generator()
        print("onManageUsersAccountsButtonPressed") 
        window = builder.get_object("window2")
        window.show()

    def onManageRacksButtonPressed(self, button):
        print("onManageRacksButtonPressed")

    def onAddNewUserButtonPressed(self, *args):
        print("onAddNewUserButtonPressed")
        username = builder.get_object("username")
        email = builder.get_object("email")
        
        db = sqlite3.connect('SaedRobot.db')
        
        c = db.cursor()
        c1 = db.cursor()
        
        c.execute('SELECT * from users WHERE username= ? ' , (str(username.get_text()),))
        data=c.fetchall()
        
        c1.execute('SELECT * from users WHERE email= ? ' , (str(email.get_text()),))
        data1=c1.fetchall()
        
        if len(str(username.get_text())) == 0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No username entered, please enter a username")
           dialog.run()
           dialog.close()
           
        elif len(str(email.get_text())) == 0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No email entered, please enter an email")
           dialog.run()
           dialog.close()
           
        elif len(data)>0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This username is already exist!")
           dialog.run()
           dialog.close()
             
        elif len(data1)>0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This email is already exist!")
           dialog.run()
           dialog.close()
           
        elif not re.match("^[a-zA-Z0-9_]+$", str(username.get_text())):
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "Invalid username address, please enter a valid username.")
           dialog.run()
           dialog.close()      
                          
        elif not validate_email(str(email.get_text())):
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "Invalid email address, please enter a valid address.")
           dialog.run()
           dialog.close()
           
        else:
			 password = id_generator()
			 c.execute('INSERT INTO users(USERNAME,PASSWORD,EMAIL,ADMIN) VALUES (?,?,?,0)', (str(username.get_text()),str(password),str(email.get_text())))
			 db.commit()
			 send_email(password,"Saed Robot - Account Password",str(email.get_text()) )
			 dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "The user has been added")
			 dialog.run()
			 dialog.close()

    def onAddUserButtonPressed(self, button):
        print("onAddUserButtonPressed")
        window = builder.get_object("window3")
        window.show()

builder = Gtk.Builder()
builder.add_from_file("Saed.glade")
builder.connect_signals(Handler())
window = builder.get_object("window3")
window.show()
Gtk.main()

