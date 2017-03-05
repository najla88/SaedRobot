#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class forgot():
	
	builder =None

    
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		window = self.builder.get_object("window2")
		backBtn=self.builder.get_object("backBtn")
		resetBtn=self.builder.get_object("resetBtn")
		backBtn.connect("clicked",self.back)
		resetBtn.connect("clicked",self.reset)

		window.show()


	def back(self,button):
		window=login()
	
	
	def reset(self,button):
		email = self.builder.get_object("email")
		db = sqlite3.connect('SaedRobot.db')
		
		c = db.cursor()
		c.execute('SELECT * from users WHERE email=?' , (email.get_text(),))
		row=c.fetchone()
		print row
		
		
		if row != None and len(row)>0:
			username = row[0]
			randPassword= id_generator()
			c = db.cursor()
			c.execute("update users set password=? where username=?" , (randPassword,username,))
			db.commit()
			send_email(randPassword,'Your New Password')
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Your new password has been sent to your email")
			dialog.run()
			dialog.close()
			window=login()

			
		else:
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid entry, please try again")
			dialog.run()
			dialog.close()
		c2 = db.cursor()			
		c2.execute('SELECT * from users WHERE email=?' , (email.get_text(),))
		row2=c2.fetchone()
		print row2



class login():
	
	builder =None
	window = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		window = self.builder.get_object("window1")
		loginBtn=self.builder.get_object("loginBtn")
		forgotPassBtn=self.builder.get_object("forgotBtn")
		loginBtn.connect("clicked",self.login)
		forgotPassBtn.connect("clicked",self.forgot)

		window.show()


	def login(self,button):
		
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")
		loginError = self.builder.get_object("loginError")

		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute('SELECT * from users WHERE username= ? AND password= ?' , (str(username.get_text()), str(password.get_text())))
		data=c.fetchall()
		
		if len(data)>0:
			print "Welcome"
			loginError.set_text('')

		else:
			#loginError.set_text('Invalid username or password, please try again')
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid username or password, please try again")
			dialog.run()
			dialog.close()
			
	def forgot(self,button):
		#self.window.hide()
		window2 =forgot()





class change_password():
	
	builder =None
	window = None
	oldPassEntry = None
	newPassEntry = None
	conPassEntry = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		window = self.builder.get_object("window3")
		
		clearBtn=self.builder.get_object("clearBtn")
		changeBtn =self.builder.get_object("changeBtn")
		backBtn = self.builder.get_object("backBtn2")
		
		self.oldPassEntry =self.builder.get_object("oldPass")
		self.newPassEntry =self.builder.get_object("newPass")
		self.conPassEntry =self.builder.get_object("conPass")
		
		
		clearBtn.connect("clicked",self.clear)
		changeBtn.connect("clicked",self.change)
		backBtn.connect("clicked",self.back)
		window.show()


	def clear(self,button):
		self.oldPassEntry.set_text('')
		self.newPassEntry.set_text('')
		self.conPassEntry.set_text('')


	def change(self,button):
		
		
		if  not (self.newPassEntry.get_text() and self.conPassEntry.get_text() and self.oldPassEntry.get_text()):
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Please fill all the fields")
			dialog.run()
			dialog.close()
		
		else:
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			c.execute('SELECT password from users WHERE username= ?' , ( 'test',))
			
			row=c.fetchone()
			print row[0]
			
			if row[0] != self.oldPassEntry.get_text():
				dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid old password")
				dialog.run()
				dialog.close()
			
			
			else:	
				
				
				if self.newPassEntry.get_text() != self.conPassEntry.get_text():
					dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"new passwords does not match")
					dialog.run()
					dialog.close()
			
				else:
					
					if len(self.newPassEntry.get_text())<6:
						dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid password format, password should be at least 6 charachters long")
						dialog.run()
						dialog.close()
						
					else:
						
						c = db.cursor()
						c.execute("update users set password=? where username=?" , (self.newPassEntry.get_text(),'test',))
						db.commit()
						dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"your password has been changed")
						dialog.run()
						dialog.close()
						self.back(button)
		
		
	def back(self,button):
		print 'hhhhhh'


window=login()
Gtk.main()
