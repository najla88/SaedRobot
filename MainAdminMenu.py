import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 
import ScanTape
import ManageRacks

class MainAdminMenu():
	
	builder =None
	window = None
	userType=None
	Username=None
	def __init__(self, username, kind):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Saed.glade")
		self.window = self.builder.get_object("window1")
		self.userType=kind
		self.Username=username		
		createBtn=self.builder.get_object("createBtn")
		manageUsersBtn=self.builder.get_object("manageUsersBtn")
		manageRacksBtn=self.builder.get_object("manageRacksBtn")	
		createBtn.connect("clicked",self.onCreateNewTaskButtonPressed)
		manageUsersBtn.connect("clicked",self.onManageUsersAccountsButtonPressed)
		manageRacksBtn.connect("clicked",self.onManageRacksButtonPressed)		
		self.window.show()

    	def onCreateNewTaskButtonPressed(self, button): 
        	self.window.destroy()
        	self.window=ScanTape.ScanTape(list(), self.Username	,self.userType)
        
    	def onManageUsersAccountsButtonPressed(self, button):
        	import ManageUsersAccounts
        	self.window.destroy()
        	self.window=ManageUsersAccounts.ManageUsersAccounts()

    	def onManageRacksButtonPressed(self, button):
        	self.window.destroy()
        	self.window=ManageRacks.ManageRack()
        	
#window=MainAdminMenu()
#Gtk.main()
