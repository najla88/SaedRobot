#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University

import sqlite3
import gi
import re
import login
import ManageUsersAccounts
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from validate_email import validate_email
import subprocess

class UpdateUser():
	builder =None
	UN=None
	window=None
	userType = None
	MyUsername = None
	
	#starting function
	def __init__(self,myUsername, kind, un):
		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		self.window = self.builder.get_object("window2")
		
		#assigning the values of the text fields to those variables (username+Email)
		username=self.builder.get_object("UN1")
		email=self.builder.get_object("Email1")

		username.set_text(un)
		self.UN=un
		self.userType = kind
		self.MyUsername = myUsername
		# making event listeners "Clicked"
		UpdateBtn=self.builder.get_object("Update")
		UpdateBtn.connect("clicked",self.Update)

			#bring all the objects
		backbox=self.builder.get_object("backbox")
		logout=self.builder.get_object("logout")
		logout.set_label('Log Out')
		logout.connect("button-release-event",self.logout)
		backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(1)
		backbox.set_sensitive(1)
		logout.set_sensitive(1)
		
		self.window.show()
		
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		#bring the user's Email and paste it in the text field
		c.execute("SELECT email from users WHERE username=?",(self.UN,))
		getEmail=c.fetchone()
		if getEmail != None:
			email.set_text(getEmail[0])
		else: # if no Email was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Something wrong .. Try Again")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()
			
	
		email.connect("focus-in-event",self.focus_in)
		email.connect("focus-out-event",self.focus_out)

	#show keyboard when the field is in focus
	def focus_in(self, entry, event):
		subprocess.Popen(["onboard","20*10"])
	#show keyboard when the field is in focus
	def focus_out(self, entry, event):
		subprocess.Popen(["pkill","onboard"])
		# event listener for Update button
	def Update(self,button):
		# take all the data in the input fields
		email=self.builder.get_object("Email1")
		db = sqlite3.connect('SaedRobot.db')
		c1 = db.cursor()
		c1.execute('SELECT * from users WHERE email= ? ' , (str(email.get_text()),))
		data1=c1.fetchall()
        
		if not validate_email(str(email.get_text())):
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"entries should follow the right format ")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()
			
		elif len(str(email.get_text())) == 0:
		        dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No email entered, please enter an email")
		        dialog.set_title("Error message")
		        dialog.run()
		        dialog.close()
		     
		elif len(data1)>0:
		        dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This email is already exist!")
		        dialog.set_title("Error message")
		        dialog.run()
		        dialog.close()
		
		else:
			#update the database with the new info
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			c.execute("update users set email =? WHERE username=?", (email.get_text(),self.UN))
			db.commit()
			
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Information has been updated")
			dialog.set_title("Confirmation message")
			respond = dialog.run()
			if respond == Gtk.ResponseType.OK:
				
				dialog.close()
				self.window.destroy()
				self.window = ManageUsersAccounts.ManageUsersAccounts(self.UN, self.userType)
				
			
		# event listener for Back button
	def back(self, button,a):
		self.window.destroy()
		self.window = ManageUsersAccounts.ManageUsersAccounts(self.UN, self.userType)
		
		#Logout
	def logout(self,button, a):
		self.window.destroy()
		self.window=login.loginClass()	
		
		
