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
			send_email(randPassword,'testingggggggggggggggggg')

			
			
		else:
			print 'there is no email' 	
		
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
			loginError.set_text('Wronge username or password')
		
			
	def forgot(self,button):
		#self.window.hide()
		window2 =forgot()
		
			
window=login()
Gtk.main()
