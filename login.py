#!/usr/bin/python

########################################################################
# 				   written by : Najla AlGhofaili, CS,				   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#   	This interface is the first interface the user will see    	   #
#   	The users can sign in using their usernae and password	 	   #
#																	   #
########################################################################
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import MainUserMenu
import MainAdminMenu
import forgotPass
import subprocess



class loginClass():
	
	builder =None
	window = None
	
	#starting function
	def __init__(self):
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Login.glade")
		self.window = self.builder.get_object("window1")
		
		#get all the objects
		loginBtn=self.builder.get_object("loginBtn")
		forgotPassBtn=self.builder.get_object("forgotBtn")
		loginBtn.connect("clicked",self.login)
		forgotPassBtn.connect("clicked",self.forgot)
		backbox=self.builder.get_object("backbox")
		logout=self.builder.get_object("logout")
		logout.set_label('')
		#logout.connect("button-release-event",self.logout)
		#backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(0)
		backbox.set_sensitive(0)
		logout.set_sensitive(0)
		
		# in/out focus keyboard connections
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")
		
		username.connect("focus-in-event",self.focus_in)
		#username.connect("focus-out-event",self.focus_out)
		password.connect("focus-in-event",self.focus_in)
		password.connect("focus-out-event",self.focus_out)
		
		#to style the screens using CSS code
		style_provider = Gtk.CssProvider()
		
		css = """
		
		GtkWindow{
		background: #ffffff;
		}
		GtkBox#logoMenu{
		background: #ffffff;
		}
		GtkLabel{
		font: sans-serif;
		}
		
		GtkEntry {
		
		
		outline: none;
		background: #fff;
		border: 1px solid #ccc;
		color: #555;
		font: sans-serif;
		padding-top:10px;
		padding-bottom:15px;

		border-radius: 1px;
		margin-bottom:150px;
		
		
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
		font: sans-serif;

		}
		
		GtkButton:active,GtkButton:hover  {
		background: #2EBC99;
		
		}
		
		
		GtkButton#forgotBtn,GtkButton#logout,  GtkButton#forgotBtn:selected,GtkButton#logout:selected {
		border-radius: 1px;
		padding: 8px 15px 8px 15px;
		border: none;
		color: #333;
		background: #fff;

		}
		
		GtkButton#forgotBtn:hover ,GtkButton#logout:hover {
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
		
		
	#show keyboard when the field is in focus
	def focus_in(self, entry, event):
		subprocess.Popen(["onboard","20*10"])
	#show keyboard when the field is in focus
	def focus_out(self, entry, event):
		subprocess.Popen(["pkill","onboard"])
	
	#login the user to the system
	def login(self,button):
		
		#get the username + password
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")

		#connect to the db
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute('SELECT * from users WHERE username= ? AND password= ?' , (str(username.get_text()), str(password.get_text())))
		data=c.fetchone()
		
		#entries are valid
		if data != None and len(data)>0:
		
			self.window.destroy()
			
			#regular user
			if data[3]==0:
				self.window=MainUserMenu.userHome(data[0],data[3])
			#admin user
			elif data[3]==1:
				self.window=MainAdminMenu.MainAdminMenu(data[0],data[3])

		#Invalid entries
		else:
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid username or password, please try again")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()
	#go to forgot password interface	
	def forgot(self,button):
		self.window.destroy()
		self.window =forgotPass.forgot()
	
	#go to the previous interface
	

