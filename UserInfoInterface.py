#!/usr/bin/python2
import sqlite3
import gi
import updateUserInterface 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UserInfo():
	builder =None
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		window = self.builder.get_object("window1")
		username=self.builder.get_object("UN")
		password=self.builder.get_object("Password")
		username.set_text("test")
		EditBtn=self.builder.get_object("Edit")
		BackBtn=self.builder.get_object("Back")
		DeleteBtn=self.builder.get_object("Delete")
		EditBtn.connect("clicked",self.Edit)
		BackBtn.connect("clicked",self.Back)
		DeleteBtn.connect("clicked",self.Delete)
		window.show()
		
		db = sqlite3.connect('testDB.db')
		c = db.cursor()
		c.execute("SELECT password from users WHERE username='test' ")
		getPass=c.fetchone()
		print getPass[0]
		if getPass != None:
			password.set_text(getPass[0])
		
	def Edit(self,button):
		#move to UpdateUserInterface and pass the username
		window2 = updateUserInterface.UpdateUser('test')
		window2.show()
	def Delete(self,button): # I think its not working!
		db = sqlite3.connect('testDB.db')
		c = db.cursor()
		c.execute("delete from users where username='test'")
	def Back(self,button): #back to the previous interface
		window3 = self.builder.get_object("window2")
		window3.show()
		
		
		

window=UserInfo()
Gtk.main()
