#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University

import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UpdateUser():
	builder =None
	def __init__(self,un):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		window = self.builder.get_object("window2")
		
		#assigning the values of the text fields to those variables (username+password)
		username=self.builder.get_object("UN1")
		password=self.builder.get_object("Password1")
		
		# coming as a global >> I think ?? 
		username.set_text(un)
		
		# making event listeners "Clicked"
		UpdateBtn=self.builder.get_object("Update")
		BackBtn=self.builder.get_object("Back")
		UpdateBtn.connect("clicked",self.Update)
		BackBtn.connect("clicked",self.Back)
		
		window.show()
		
		db = sqlite3.connect('testDB.db')
		c = db.cursor()
		#bring the user's password and paste it in the text field
		c.execute("SELECT password from users WHERE username=?",(un,))
		getPass=c.fetchone()
		print getPass[0]
		if getPass != None:
			password.set_text(getPass[0])
		
		# event listener for Update button
	def Update(self,button):
		# take all the data in the input fields
		username=self.builder.get_object("UN1")
		password=self.builder.get_object("Password1")
		
		if len(password.get_text())<6:
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Password should be more than 6 characters long")
			dialog.run()
			dialog.close()
			print "INFO dialog closed"
		
		else:
			#update the database with the new info
			db = sqlite3.connect('testDB.db')
			c = db.cursor()
			c.execute("update users set password =? WHERE username=?", (password.get_text(),(username.get_text())))
			db.commit()
			
			#should give a proper message or a pop up window as confirmation
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Information has been updated")
			dialog.run()
			dialog.close()
			print "INFO dialog closed"
			
		# event listener for Back button
	def Back(self,button): # go to the previous interface
		window3 = self.builder.get_object("window2")
		window3.show()
		
		
		

#window=UpdateUser()
#Gtk.main()
