#!/usr/bin/python2
import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class login():
	builder =None
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		window = self.builder.get_object("window1")
		usernameBtn=self.builder.get_object("loginBtn")
		forgotPassBtn=self.builder.get_object("forgotBtn")
		usernameBtn.connect("clicked",self.login)
		forgotPassBtn.mousePressEvent = self.forgot

		window.show()

	def login(self,button):
		
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")
		loginError = self.builder.get_object("loginError")
		loginError.connect("activate-current-link",self.forgot)

		db = sqlite3.connect('testDB.db')
		c = db.cursor()
		c.execute('SELECT * from users WHERE username= ? AND password= ?' , (str(username.get_text()), str(password.get_text())))
		data=c.fetchall()
		if len(data)>0:
			print "Welcome"
			loginError.set_text('')

		else:
			loginError.set_text('Wronge username or password')
			
	def forgot(self,event):
		
		window2 = self.builder.get_object("window2")
		window2.show()			
			
window=login()
Gtk.main()
