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
		usernameBtn.connect("clicked",self.login)
		window.show()

	def login(self,button):
		
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")
		db = sqlite3.connect('testDB.db')
		c = db.cursor()
		c.execute('SELECT * from users WHERE username= ? AND password= ?' , (str(username.get_text()), str(password.get_text())))
		data=c.fetchall()
		if len(data)>0:
			print "Welcome"
		else:
			print "Login failed"
			
window=login()
Gtk.main()
