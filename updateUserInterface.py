#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University

import sqlite3
import gi
import re
import login
import ManageUsersAccounts
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from validate_email import validate_email

class UpdateUser():
	builder =None
	UN=None
	window=None
	def __init__(self,un):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		self.window = self.builder.get_object("window2")
		
		#assigning the values of the text fields to those variables (username+Email)
		username=self.builder.get_object("UN1")
		email=self.builder.get_object("Email1")
		
		username.set_text(un)
		self.UN=un
		
		# making event listeners "Clicked"
		UpdateBtn=self.builder.get_object("Update")
		UpdateBtn.connect("clicked",self.Update)
		
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
		print getEmail[0]
		if getEmail != None:
			email.set_text(getEmail[0])
		else: # if no Email was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Something wrong .. Try Again")
			dialog.run()
			dialog.close()
			print "Warning dialog closed"
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
			dialog.run()
			dialog.close()
			
		elif len(str(email.get_text())) == 0:
		        dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "No email entered, please enter an email")
		        dialog.run()
		        dialog.close()
		     
		elif len(data1)>0:
		        dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, "This email is already exist!")
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
			respond = dialog.run()
			if respond == Gtk.ResponseType.OK:
				
				dialog.close()
				self.window.destroy()
				self.window = ManageUsersAccounts.ManageUsersAccounts()
				self.window.show()
				
			
		# event listener for Back button
	def back(self, button,a):
		self.window.destroy()
		self.window = ManageUsersAccounts.ManageUsersAccounts()
		self.window.show()
		
	def logout(self,button, a):
		self.window.destroy()
		self.window=login.loginClass()	
		
		
		
		

#window=UpdateUser()
#Gtk.main()
