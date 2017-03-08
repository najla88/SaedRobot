#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import maryam



class loginClass():
	
	builder =None
	window = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		self.window = self.builder.get_object("window1")
		loginBtn=self.builder.get_object("loginBtn")
		forgotPassBtn=self.builder.get_object("forgotBtn")
		loginBtn.connect("clicked",self.login)
		forgotPassBtn.connect("clicked",self.forgot)
		
		style_provider = Gtk.CssProvider()
		css = """
		
		GtkWindow{
		background: #ffffff;
		}
		GtkBox#logoMenu{
		background: #999;
		}
		
		GtkEntry {
		
		
		outline: none;
		background: #fff;
		border: 1px solid #ccc;
		color: #555;
		font: Arial, Helvetica, sans-serif;
		padding-top:10px;
		padding-bottom:10px;

		border-radius: 1px;

		
		
		}
		
		GtkEntry:focus  {
		box-shadow: 0 0 5px #43D1AF;
		border: 1px solid #43D1AF;
 
		
		}
		
		
		GtkButton {
		background: #43D1AF;
		border-radius: 1px;
		padding: 15px 15px 15px 15px;
		border: none;
		color: #fff;
		}
		
		GtkButton:active,GtkButton:hover  {
		background: #2EBC99;
		
		}
		
		
		GtkButton#forgotBtn, GtkButton#forgotBtn:selected {
		border-radius: 1px;
		padding: 8px 15px 8px 15px;
		border: none;
		color: #333;
		background: #fff;

		}
		
		GtkButton#forgotBtn:hover {
		background: #fff;
		color: #43D1AF;
		
		}
		"""
		style_provider.load_from_data(css)
		Gtk.StyleContext.add_provider_for_screen(
		Gdk.Screen.get_default(), 
		style_provider,     
		Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


		self.window.show()
		
		


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
			self.window.destroy()
			self.window=maryam.userHome()

		else:
			#loginError.set_text('Invalid username or password, please try again')
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid username or password, please try again")
			dialog.run()
			dialog.close()
			
	def forgot(self,button):
		self.window.destroy()
		self.window =forgot()

