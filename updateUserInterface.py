#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University

import sqlite3
import gi
import re
import UserInfoInterface
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from validate_email import validate_email

class UpdateUser():
	builder =None
	UN=None
	def __init__(self,un):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		window = self.builder.get_object("window2")
		
		#assigning the values of the text fields to those variables (username+Email)
		username=self.builder.get_object("UN1")
		email=self.builder.get_object("Email1")
		
		# coming as a global >> I think ?? 
		
		username.set_text(un)
		self.UN=un
		
		# making event listeners "Clicked"
		UpdateBtn=self.builder.get_object("Update")
		BackBtn=self.builder.get_object("Back1")
		UpdateBtn.connect("clicked",self.Update)
		BackBtn.connect("clicked",self.Back)
		
		window.show()
		
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		#bring the user's Email and paste it in the text field
		c.execute("SELECT email from users WHERE username=?",(self.UN,))
		getEmail=c.fetchone()
		print getEmail[0]
		if getEmail != None:
			email.set_text(getEmail[0])
		else: # if no Email was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"Something wrong .. Try Again")
			dialog.run()
			dialog.close()
			print "Warning dialog closed"
		# event listener for Update button
	def Update(self,button):
		# take all the data in the input fields
		email=self.builder.get_object("Email1")
		
		if not validate_email(str(email.get_text())):
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"entries should follow the right format ")
			dialog.run()
			dialog.close()
			print "INFO dialog closed"
		
		else:
			#update the database with the new info
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			c.execute("update users set email =? WHERE username=?", (email.get_text(),self.UN))
			db.commit()
			
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Information has been updated")
			dialog.run()
			dialog.close()
			print "INFO dialog closed"
			
		# event listener for Back button
	def Back(self,button): # go to the previous interface
		window3 = UserInfoInterface.UserInfo(self.UN)
		window3.show()
		
		
		

#window=UpdateUser()
#Gtk.main()
