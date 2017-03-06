import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from common import id_generator,send_email
import string
import sqlite3
from validate_email import validate_email
import re
import ManageUsersAccounts
		
class AddNewUser():

    builder = None
    window = None
    box = None
    username = None
    email = None
    
    def __init__(self):
	self.builder = Gtk.Builder()
	self.builder.add_from_file("Saed.glade")
	self.window = self.builder.get_object("window3")
	self.username = self.builder.get_object("username")
        self.email = self.builder.get_object("email")	
	addBtn=self.builder.get_object("addBtn1")
	backBtn=self.builder.get_object("backBtn1")	
	addBtn.connect("clicked",self.onAddNewUserButtonPressed)
	backBtn.connect("clicked",self.onBackToManageUsersButtonPressed)
	
        self.window.show_all()


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
           dialog.run()
           dialog.close()
           
        elif len(str(self.email.get_text())) == 0:
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
			 c.execute('INSERT INTO users(USERNAME,PASSWORD,EMAIL,ADMIN) VALUES (?,?,?,0)', (str(self.username.get_text()),str(password),str(self.email.get_text())))
			 db.commit()
			 send_email(password,"Saed Robot - Account Password",str(email.get_text()) )
			 dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "The user has been added")
			 dialog.run()
			 dialog.close()
			 
    def onBackToManageUsersButtonPressed(self, button):
        self.window.destroy()
        self.window=ManageUsersAccounts.ManageUsersAccounts()

        
#window = AddNewUser()
#Gtk.main()
