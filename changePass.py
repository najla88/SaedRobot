#written by : Najla AlGhofaili, CS, Imam Abdulrahman AlFaisal University
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import maryam
import login


class change_password():
	
	builder =None
	window = None
	oldPassEntry = None
	newPassEntry = None
	conPassEntry = None
	Username=None
	userType=None
	
	#starting function
	def __init__(self,username,kind):
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		self.window = self.builder.get_object("window3")
		
		#get username
		self.Username=username
		
		#connects all the contents with their corrospondance variables
		clearBtn=self.builder.get_object("clearBtn")
		changeBtn =self.builder.get_object("changeBtn")
		
		self.oldPassEntry =self.builder.get_object("oldPass")
		self.newPassEntry =self.builder.get_object("newPass")
		self.conPassEntry =self.builder.get_object("conPass")
		self.userType=kind
		
		clearBtn.connect("clicked",self.clear)
		changeBtn.connect("clicked",self.change)
		
		
		
		backbox=self.builder.get_object("backbox2")
		logout=self.builder.get_object("logout2")
		logout.set_label('Log Out')
		logout.connect("button-release-event",self.logout)
		backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(1)
		backbox.set_sensitive(1)
		logout.set_sensitive(1)
		
		
		self.window.show()

	#clear all the fields
	def clear(self,button):
		self.oldPassEntry.set_text('')
		self.newPassEntry.set_text('')
		self.conPassEntry.set_text('')

	#change the password
	def change(self,button):
		
		##validation 
		#all the fields should be filled
		if  not (self.newPassEntry.get_text() and self.conPassEntry.get_text() and self.oldPassEntry.get_text()):
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"Please fill all the fields")
			dialog.set_title("Warning message")
			dialog.run()
			dialog.close()
		
		else:
			#connect to the db and start checking the entries
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			c.execute('SELECT password from users WHERE username= ?' , ( self.Username,))
			
			row=c.fetchone()
			print row[0]
			
			#Invalid old password
			if row[0] != self.oldPassEntry.get_text():
				dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid old password")
				dialog.set_title("Error message")
				dialog.run()
				dialog.close()
			
			
			else:	
				#new passwords doesn't match
				if self.newPassEntry.get_text() != self.conPassEntry.get_text():
					dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"new passwords does not match")
					dialog.set_title("Error message")
					dialog.run()
					dialog.close()
			
				else:
					#Invalid password format
					if len(self.newPassEntry.get_text())<6:
						dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid password format, password should be at least 6 charachters long")
						dialog.set_title("Error message")
						dialog.run()
						dialog.close()
						
					else:
						#Right entries case+update query
						c = db.cursor()
						c.execute("update users set password=? where username=?" , (self.newPassEntry.get_text(),self.Username,))
						db.commit()
						dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"your password has been changed")
						dialog.set_title("Confirmation message")
						dialog.run()
						dialog.close()
						self.back(button)
		self.window.destroy()
		self.window=maryam.userHome(self.Username, self.userType)
		
	#back to the previous screen
	def back(self, button,a):
		self.window.destroy()
		self.window=maryam.userHome(self.Username, self.userType)
	#Logout
	def logout(self,button, a):
		self.window.destroy()
		self.window=login.loginClass()	
