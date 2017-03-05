#!/usr/bin/python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from common import id_generator,send_email
import string
import random
import smtplib
import sqlite3

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
           print("username is empty")
           
        elif len(str(email.get_text())) == 0:
           print("email is empty")
           
        elif len(data)>0:
             print "This username already exist!"
             
        elif len(data1)>0:
             print "This email is already exist!"            
        else:
			 password = id_generator()
			 c.execute('INSERT INTO users(USERNAME,PASSWORD,EMAIL,ADMIN) VALUES (?,?,?,0)', (str(username.get_text()),str(password),str(email.get_text())))
			 db.commit()
			 send_email(password,"Saed Robot - Account Password",str(email.get_text()) )
			 window = builder.get_object("window4")
			 window.show()

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

