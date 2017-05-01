#!/usr/bin/python

########################################################################
# 				  	 written by : Reem AlJunaid, CS,				   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#  	 This interface manages the admin interface where the admin  	   #
#    				can add new users to the database 		  		   #
#																	   #
########################################################################
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from common import id_generator,send_email
import string
import sqlite3
from validate_email import validate_email
import re
import login
import ManageUsersAccounts
import subprocess
        		
class AddNewUser():

    builder = None
    window = None
    box = None
    username = None
    email = None
    MyUsername = None
    userType=None
    
    #starting function
    def __init__(self, Username, kind):
		self.MyUsername = Username
		self.userType=kind
		self.builder = Gtk.Builder()
		self.builder.add_from_file("AdminHome.glade")
		self.window = self.builder.get_object("window3")
		self.username = self.builder.get_object("username")
		self.email = self.builder.get_object("email")	
		addBtn=self.builder.get_object("addBtn1")
		logoutBtn=self.builder.get_object("logoutBtn3")
		addBtn.connect("clicked",self.onAddNewUserButtonPressed)
		logoutBtn.connect("clicked",self.onLogoutButtonPressed)
		backbox=self.builder.get_object("backbox3")
		backbox.connect("button-release-event",self.onBackToManageUsersButtonPressed)
		image=self.builder.get_object("image3")
		image.set_visible(1)
		backbox.set_sensitive(1)
		self.window.show_all()

		self.username.connect("focus-in-event",self.focus_in)
		self.username.connect("focus-out-event",self.focus_out)
		self.email.connect("focus-in-event",self.focus_in)
		self.email.connect("focus-out-event",self.focus_out)

	#show keyboard when the field is in focus
    def focus_in(self, entry, event):
		subprocess.Popen(["onboard","20*10"])
	#show keyboard when the field is in focus
    def focus_out(self, entry, event):
		subprocess.Popen(["pkill","onboard"])
		
    def onAddNewUserButtonPressed(self, button):
        
        db = sqlite3.connect('SaedRobot.db')
        
        c = db.cursor()
        c1 = db.cursor()
        
        c.execute('SELECT * from users WHERE username= ? ' , (str(self.username.get_text()),))
        data=c.fetchall()
        
        c1.execute('SELECT * from users WHERE email= ? ' , (str(self.email.get_text()),))
        data1=c1.fetchall()
        
        if len(str(self.username.get_text())) == 0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No username entered, please enter a username")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()
           
        elif len(str(self.email.get_text())) == 0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No email entered, please enter an email")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()
           
        elif len(data)>0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This username is already exist!")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()
             
        elif len(data1)>0:
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This email is already exist!")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()
           
        elif not re.match("^[a-zA-Z0-9_]+$", str(self.username.get_text())):
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "Invalid username address, please enter a valid username.")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()      
                          
        elif not validate_email(str(self.email.get_text())):
           dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "Invalid email address, please enter a valid address.")
           dialog.set_title("Error message")
           dialog.run()
           dialog.close()
           
        else:
			 password = id_generator()
			 c.execute('INSERT INTO users(USERNAME,PASSWORD,EMAIL,ADMIN) VALUES (?,?,?,0)', (str(self.username.get_text()),str(password),str(self.email.get_text())))
			 db.commit()
			 send_email(password,"Saed Robot - Account Password",str(self.email.get_text()) )
			 dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "The user has been added")
			 dialog.set_title("Confirmation message")
			 dialog.run()
			 dialog.close()
			 self.window.destroy()
			 self.window=ManageUsersAccounts.ManageUsersAccounts(self.MyUsername, self.userType)
		
			 
    def onBackToManageUsersButtonPressed(self, button, a):
        self.window.destroy()
        self.window=ManageUsersAccounts.ManageUsersAccounts(self.MyUsername, self.userType)

    def onLogoutButtonPressed(self, button):
		self.window.destroy()
		self.window=login.loginClass()  
		        
#window = AddNewUser()
#Gtk.main()
