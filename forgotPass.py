#written by : Najla AlGhofaili, CS, Imam Abdulrahman AlFaisal University
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import MainUserMenu
import login
import subprocess

class forgot():
	
	builder =None
	window= None
    
    #starting function
	def __init__(self):
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Login.glade")
		self.window = self.builder.get_object("window2")
		resetBtn=self.builder.get_object("resetBtn")
		resetBtn.connect("clicked",self.reset)

		# get the objects to the screen
		backbox=self.builder.get_object("backbox1")
		logout=self.builder.get_object("logout1")
		logout.set_label('')
		backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(1)
		backbox.set_sensitive(1)
		logout.set_sensitive(0)
		
	
		self.window.show()
		email = self.builder.get_object("email") # get the value from the field
		email.connect("focus-in-event",self.focus_in)
		email.connect("focus-out-event",self.focus_out)

	#show keyboard when the field is in focus
	def focus_in(self, entry, event):
		subprocess.Popen(["onboard","20*10"])
	#show keyboard when the field is in focus
	def focus_out(self, entry, event):
		subprocess.Popen(["pkill","onboard"])
		
	#back to the previous screen
	def back(self,button,a):
		self.window.destroy()
		self.window=login.loginClass()
	
	# reset the password by taking the value in the entry field
	def reset(self,button):
		email = self.builder.get_object("email") # get the value from the field
		db = sqlite3.connect('SaedRobot.db')
		
		c = db.cursor()
		# query the DB if such an email exist
		c.execute('SELECT * from users WHERE email=?' , (email.get_text(),))
		row=c.fetchone()
		
		# check+send the new password
		if row != None and len(row)>0:
			username = row[0]
			randPassword= id_generator()
			c = db.cursor()
			c.execute("update users set password=? where username=?" , (randPassword,username,))
			db.commit()
			send_email(randPassword,'Your New Password',email.get_text())
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Your new password has been sent to your email")
			dialog.set_title("Confirmation message")
			dialog.run()
			dialog.close()
			self.window=login.loginClass()

		# show error message if no such email exists
		else:
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Invalid entry, please try again")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()

