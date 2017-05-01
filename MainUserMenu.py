#written by : Arwa AlKhunine, Maryam Al-Abdullatif, CS, Imam Abdulrahman AlFaisal University
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
	
	#staring function
	def __init__(self,username,kind):
		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window1")
		
		#get username+type
		self.Username=username
		self.userType=kind
		
		#get all objects
		createTaskBtn=self.builder.get_object("createTaskBtn")
		changePasswordBtn=self.builder.get_object("changePasswordBtn")
		createTaskBtn.connect("clicked",self.createTask)
		changePasswordBtn.connect("clicked",self.changePassword)
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)	
  
		self.window.show()
		

	#go to Scan Tape interface
	def createTask(self,button):
		
		self.window.destroy()
		self.window=ScanTape.ScanTape(list(),self.Username,self.userType)
		
		
	#go to change password interface		
	def changePassword(self,button):
		self.window.destroy()
		window2 = changePass.change_password(self.Username,self.userType)
	#Logout
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
	
	#starting function
	def __init__(self,volser, tl,username, kind): # tl = tape list
		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window2")
		
		#get the username+type
		self.userType=kind
		self.Username=username
		
		#get all the objects
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
		
		#if tapeslist.count() == 3 disable scann btn and hover or hint maxmam 3 tape
		if self.tapesList!= None and len(self.tapesList) == 2:
			scanBtn.set_sensitive(False)
			self.hint.set_text("You reached the maximmum number of tapes")
			
			
			#connect to db+bring the volser info
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute('SELECT * from inventory WHERE volser= ?' , (volser,))
		data=c.fetchone()
		
		#valid volser
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
	
	
	def cancel(self,button): #Go to ScanTape interface with the TapeList with no further changes
		self.window.destroy()
		index = len(self.tapesList)
		del self.tapesList[index - 1]
		self.window=ScanTape.ScanTape(self.tapesList,self.Username,self.userType)
		
	#Logout
	def onLogoutButtonPressedButtonPressed(self, button):
			self.window.destroy()
			self.window=login.loginClass()       	
		


