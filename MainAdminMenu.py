#written by : Reem AlJunaid, CS, Imam Abdulrahman AlFaisal University
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 
import ScanTape
import ManageRacks
import ManageUsersAccounts
import login

class MainAdminMenu():
	
	builder =None
	window = None
	userType=None
	Username=None
	
	#starting function
	def __init__(self, username, kind):
		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("AdminHome.glade")
		self.window = self.builder.get_object("window1")
		
		#get the user name+type
		self.userType=kind
		self.Username=username		
		
		#get all the objects
		createBtn=self.builder.get_object("createBtn")
		logoutBtn=self.builder.get_object("logoutBtn1")
		manageUsersBtn=self.builder.get_object("manageUsersBtn")
		manageRacksBtn=self.builder.get_object("manageRacksBtn")	
		createBtn.connect("clicked",self.onCreateNewTaskButtonPressed)
		manageUsersBtn.connect("clicked",self.onManageUsersAccountsButtonPressed)
		manageRacksBtn.connect("clicked",self.onManageRacksButtonPressed)
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)	
		self.window.show()

		#go to Scan Tape interface
    	def onCreateNewTaskButtonPressed(self, button): 
        	self.window.destroy()
        	self.window=ScanTape.ScanTape(list(), self.Username	,self.userType)
        
        #go to Manage user accounts interface
    	def onManageUsersAccountsButtonPressed(self, button):        	
        	self.window.destroy()
        	self.window=ManageUsersAccounts.ManageUsersAccounts(self.Username, self.userType)

		#go to Manage Racks interface
    	def onManageRacksButtonPressed(self, button):
        	self.window.destroy()
        	self.window=ManageRacks.ManageRack(self.Username, self.userType)
        	
		#Logout
    	def onLogoutButtonPressedButtonPressed(self, button):
			self.window.destroy()
			self.window=login.loginClass()       	

