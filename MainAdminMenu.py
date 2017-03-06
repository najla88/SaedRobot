import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk 
import ManageUsersAccounts
class MainAdminMenu():
	
	builder =None
	window = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Saed.glade")
		self.window = self.builder.get_object("window1")		
		createBtn=self.builder.get_object("createBtn")
		manageUsersBtn=self.builder.get_object("manageUsersBtn")
		manageRacksBtn=self.builder.get_object("manageRacksBtn")	
		createBtn.connect("clicked",self.onCreateNewTaskButtonPressed)
		manageUsersBtn.connect("clicked",self.onManageUsersAccountsButtonPressed)
		manageRacksBtn.connect("clicked",self.onManageRacksButtonPressed)		
		self.window.show()

    	def onCreateNewTaskButtonPressed(self, button): 
        	self.window.destroy()
        	#self.window=ManageUsersAccounts.ManageUsersAccounts()
        
    	def onManageUsersAccountsButtonPressed(self, button):
        	self.window.destroy()
        	self.window=ManageUsersAccounts.ManageUsersAccounts()

    	def onManageRacksButtonPressed(self, button):
        	self.window.destroy()
        	#self.window=ManageUsersAccounts.ManageUsersAccounts()
        	
window=MainAdminMenu()
Gtk.main()
