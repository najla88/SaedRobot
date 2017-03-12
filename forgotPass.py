#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import maryam
import login

class forgot():
	
	builder =None
	window= None
    
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		self.window = self.builder.get_object("window2")
		#backBtn=self.builder.get_object("backBtn")
		resetBtn=self.builder.get_object("resetBtn")
		#backBtn.connect("clicked",self.back)
		resetBtn.connect("clicked",self.reset)


		backbox=self.builder.get_object("backbox1")
		logout=self.builder.get_object("logout1")
		logout.set_label('')
		#logout.connect("button-release-event",self.logout)
		backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(1)
		backbox.set_sensitive(1)
		logout.set_sensitive(0)
		
		



		self.window.show()


	def back(self,button,a):
		self.window.destroy()
		self.window=login.loginClass()
	
	
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
			send_email(randPassword,'Your New Password',email.get_text())
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Your new password has been sent to your email")
			dialog.run()
			dialog.close()
			self.window=loginClass()

			
		else:
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid entry, please try again")
			dialog.run()
			dialog.close()
		c2 = db.cursor()			
		c2.execute('SELECT * from users WHERE email=?' , (email.get_text(),))
		row2=c2.fetchone()
		print row2

