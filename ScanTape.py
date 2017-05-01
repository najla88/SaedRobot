#written by : Arwa AlKhunine, Maryam Al-Abdullatif, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MainUserMenu
import MainAdminMenu
import login
import subprocess
import signal

class ScanTape():
	builder =None
	window = None
	barcode1=None
	tapesList = None
	userType = None
	Username=None
	checkBarcode = None
	
	#starting function
	def __init__(self, tl,username,kind ):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ScanMoreInterface.glade")
		self.window = self.builder.get_object("window1")
		#######################################################
		#get user type+ name
		self.userType=kind
		self.Username= username
		########################################################
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)	
		
		
		#bring the objects to the screen
		backbox=self.builder.get_object("backbox2")
		backbox.connect("button-release-event",self.back)
		image=self.builder.get_object("image1")
		image.set_visible(1)
		backbox.set_sensitive(1)
		
		
		
		# connect the buttons and make their event listener
		ScanBtn=self.builder.get_object("Scan")
		self.barcode1 = self.builder.get_object("barcode")
		self.barcode1.set_text("")
	#	self.barcode1.connect("focus-in-event",self.focus_in)
	#	self.barcode1.connect("focus-out-event",self.focus_out)
		
		ScanBtn.connect("clicked",self.Scan)
		self.tapesList= tl
		if self.tapesList != None:
		#show
		self.window.show()
	
	#show keyboard when the field is in focus
	#def focus_in(self, entry, event):
	#	subprocess.Popen(["onboard","20*10"])
	#show keyboard when the field is in focus
	#def focus_out(self, entry, event):
	#	subprocess.Popen(["pkill","onboard"])
	#start scanning
	def Scan(self,button):
		#Get the Barcode and move to tape info interface
		barcode=self.barcode1.get_text()
		if barcode != "":
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			#check if the barcode belongs to the database
			c.execute("SELECT * from inventory WHERE volser=?",(barcode,))
			self.checkBarcode=c.fetchone()
	
			if self.checkBarcode != None:
				#tape alreade scanned
				if self.checkBarcode[0] in self.tapesList :
					dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"You have already scanned this tape")
					dialog.set_title("Error message")
					dialog.run()
					dialog.close()
					self.barcode1.set_text("")
					
				#valid tape
				else :
					self.window.destroy()
					self.window =MainUserMenu.tapeInfo(self.checkBarcode[0] , self.tapesList,self.Username,self.userType)
			else:
				 # if Barcode is not in the DB alert with warning message 
				dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Scanned barcode does not belong to our database .. try another one")
				dialog.set_title("Error message")
				dialog.run()
				dialog.close()
				self.barcode1.set_text("")
		else:
			 # if no Barcode was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Barcode is not detected .. Try Again")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()
	
	#back		
	def back(self,button,a):
		
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.QUESTION,Gtk.ButtonsType.YES_NO,"Do you want to cancel this task?")
		dialog.set_title("Confirmation message")
		respond=dialog.run()
		
		#cancel the task
		if respond == Gtk.ResponseType.YES:
			#go to Home Admin
			if (self.userType==1):
				self.window.destroy()
				del self.tapesList[:]
				self.window=MainAdminMenu.MainAdminMenu(self.Username,self.userType)
				dialog.close()
			#go to Home User
			else:
				self.window.destroy()
				del self.tapesList[:]
				self.window=MainUserMenu.userHome(self.Username,self.userType)
				dialog.close()
		#do not cancel the task
		elif respond == Gtk.ResponseType.NO:
			dialog.close()
			
	#Logout
	def onLogoutButtonPressedButtonPressed(self, button):
			self.window.destroy()
			self.window=login.loginClass()       	

			
				
			
			



###back on scan will check if user or admin		

