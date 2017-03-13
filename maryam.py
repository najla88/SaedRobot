#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login
import changePass
import ScanTape
import ChooseDestination
class userHome():
	
	builder =None
	window = None
	Username=None
	userType=None
	
	def __init__(self,username,kind):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window1")
		self.Username=username
		self.userType=kind
		createTaskBtn=self.builder.get_object("createTaskBtn")
		changePasswordBtn=self.builder.get_object("changePasswordBtn")
		createTaskBtn.connect("clicked",self.createTask)
		changePasswordBtn.connect("clicked",self.changePassword)
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)	
  
		self.window.show()
		


	def createTask(self,button):
		
		self.window.destroy()
		self.window=ScanTape.ScanTape(list(),self.Username,self.userType)
		##we should have scane class
			
	def changePassword(self,button):
		self.window.destroy()
		window2 = changePass.change_password(self.Username,self.userType)
		
	def onLogoutButtonPressedButtonPressed(self, button):
			self.window.destroy()
			self.window=login.loginClass()       	
 
		
class tapeInfo():
	
	builder =None
	window = None
	projectName = None
	tapeName = None
	rackName = None
	slotNumber = None
	tapesList = None
	barcode = None
	hint = None
	userType=None
	Username=None
	
	def __init__(self,volser, tl,username, kind): # tl = tape list
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window2")
		self.userType=kind
		self.Username=username
		scanBtn=self.builder.get_object("scanBtn")
		logoutBtn=self.builder.get_object("logoutBtn2")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)	
		proceedBtn=self.builder.get_object("proceedBtn")
		cancelBtn=self.builder.get_object("cancelBtn")
		self.projectName=self.builder.get_object("projectName")
		self.tapeName=self.builder.get_object("tapeName")
		self.rackName=self.builder.get_object("rackName")
		self.slotNumber=self.builder.get_object("slotNumber")
		self.hint=self.builder.get_object("hint")
		scanBtn.connect("clicked",self.scan)
		proceedBtn.connect("clicked",self.proceed)
		cancelBtn.connect("clicked",self.cancel)
		
		
		self.tapesList= tl
		self.barcode = volser
		
		#if tapeslist.count() == 3 disable scann btn and hover or hint maxmam 3 tap
		if self.tapesList!= None and len(self.tapesList) == 2:
			scanBtn.set_sensitive(False)
			self.hint.set_text("You reached the maximmum number of tapes")
			
			
			
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute('SELECT * from inventory WHERE volser= ?' , (volser,))
		data=c.fetchone()
		
		if data !=None and len(data)>0:
			self.projectName.set_text(data[1])
			self.tapeName.set_text(data[0])
			self.rackName.set_text(data[2])
			self.slotNumber.set_text(str(data[3]))
			self.tapesList.append(self.barcode)

		self.window.show()

	def scan(self,button):
		# this method will append the barcode to the list and send the list back to ScanTape Interface
		
		self.window.destroy()
		self.window=ScanTape.ScanTape(self.tapesList,self.Username,self.userType)
		
		
	def proceed(self,button):
		self.window.destroy() # Go ahead to next interface with the tapelist >> Zainab's interface Choose distnation
		self.window=ChooseDestination.ChooseDes(self.tapesList,self.Username,self.userType)
		###########################################
		#here is zainab ++++++paaaaas theee usertyyyyyyype
		######################################################
	
	
	def cancel(self,button): #Go to ScanTape interface with the TapeList with no further changes
		self.window.destroy()
		index = len(self.tapesList)
		print self.tapesList
		del self.tapesList[index - 1]
		print self.tapesList
		self.window=ScanTape.ScanTape(self.tapesList,self.Username,self.userType)
		
	
	def onLogoutButtonPressedButtonPressed(self, button):
			self.window.destroy()
			self.window=login.loginClass()       	
		

		
# put thim coment chang the window in the first class to window1
#window=create_task()
#Gtk.main()
