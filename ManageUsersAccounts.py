#written by : Reem AlJunaid, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import updateUserInterface
import login
		
class ManageUsersAccounts():

    builder = None
    window = None
    box = None
    tree_selection = None
    deleteBtn = None
    editButton = None
    software_liststore = None
    grid = None
    MyUsername = None
    userType = None
    
    #starting function
    def __init__(self, Username, kind):
		
	#get the username+type
	self.MyUsername = Username
	self.userType = kind
	
	#connect to the desired window from glade file
	self.builder = Gtk.Builder()
	self.builder.add_from_file("AdminHome.glade")
	self.window = self.builder.get_object("window2")	
	
	#get all the objects
	self.grid=self.builder.get_object("usersTable")
	addBtn=self.builder.get_object("addBtn")
	self.editBtn=self.builder.get_object("editBtn")
	self.deleteBtn=self.builder.get_object("deleteBtn")
	logoutBtn=self.builder.get_object("logoutBtn2")
	addBtn.connect("clicked",self.onAddUserButtonPressed)
	
	#connect to the db+get users info
	con = sqlite3.connect('SaedRobot.db', timeout=4000)
	cur = con.cursor()
	cur.execute("SELECT USERNAME, EMAIL from users")
	software_list = cur.fetchall()
	logoutBtn.connect("clicked",self.onLogoutButtonPressed)
	backbox=self.builder.get_object("backbox2")
	backbox.connect("button-release-event",self.onBackToMainAdminMenuButtonPressed)
	image=self.builder.get_object("image2")
	image.set_visible(1)
	backbox.set_sensitive(1)

        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str,str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()


        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Username", "Email"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #setting up the layout, putting the treeview in a scrollwindow
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)
	
	self.tree_selection = self.treeview.get_selection()
	self.tree_selection.connect("changed", self.onSelectionChanged)
	
	self.deleteBtn.connect("clicked",self.onDeleteButtonPressed,self.tree_selection)
	self.editBtn.connect("clicked",self.onEditButtonPressed,self.tree_selection)
	
	#disable delete+edit buttons
	self.deleteBtn.set_sensitive(False)
	self.editBtn.set_sensitive(False)
	
	self.tree_selection.unselect_all()
	
	self.window.show_all()
        
	#go to add new user interface
    def onAddUserButtonPressed(self, button):
        import AddNewUser
        self.window.destroy()
        self.window=AddNewUser.AddNewUser(self.MyUsername,self.userType)
	
	#go to update user info interface
    def onEditButtonPressed(self, button, selection):
		model,list_iter = selection.get_selected () 
		valu = None
		if list_iter is not None:
		   value = model[list_iter][0]
        	self.window.destroy()
        	self.window=updateUserInterface.UpdateUser(self.MyUsername,self.userType,value)
	
	#delete the selected user
    def onDeleteButtonPressed(self,button, selection):
		#ask the user to be sure
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.QUESTION,Gtk.ButtonsType.YES_NO, "Are you sure you want to delete this user?")
		dialog.set_title("Confirmation message")
		response = dialog.run()
			#yes >>delete
        	if response == Gtk.ResponseType.YES:
		   model,list_iter = selection.get_selected () 
		   valu = None
		   if list_iter is not None:
                      value = model[list_iter][0]
		   con1 = sqlite3.connect('SaedRobot.db', timeout=4000)
                   c1 = con1.cursor()
		   c1.execute("Delete from users where username = ?" , (value,))
		   con1.commit()
		   c1.execute("SELECT USERNAME, EMAIL from users")
		   list3 = c1.fetchall()
		   self.software_liststore.clear()
		   #Creating the ListStore model
        	   for software_ref in list3:
            	    	self.software_liststore.append(list(software_ref))
        	   self.current_filter_language = None
                   #Creating the filter, feeding it with the liststore model
        	   self.language_filter = self.software_liststore.filter_new()


        	   #creating the treeview, making it use the filter as a model, and adding the columns
		   self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        	   for i, column_title in enumerate(["Username", "Email"]):
                       renderer = Gtk.CellRendererText()
                       column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                       self.treeview.append_column(column)

        	   #setting up the layout, putting the treeview in a scrollwindow
        	   self.scrollable_treelist = Gtk.ScrolledWindow()
        	   self.scrollable_treelist.set_vexpand(False)
                   self.scrollable_treelist.set_hexpand(False)
        	   self.grid.attach(self.scrollable_treelist, 0, 0, 1, 1)
        	   self.scrollable_treelist.add(self.treeview)	
        	   self.tree_selection.unselect_all()
        	   self.deleteBtn.set_sensitive(False)
        	   self.editBtn.set_sensitive(False)		
            
        	dialog.close()
     #back to home admin      
    def onBackToMainAdminMenuButtonPressed(self, button, a):
	import MainAdminMenu
        self.window.destroy()
        self.window=MainAdminMenu.MainAdminMenu(self.MyUsername,self.userType)
	
	#activate Edit+delete buttons for the selected user
    def onSelectionChanged(self, tree_selection) :
	(model, pathlist) = tree_selection.get_selected_rows()
	self.deleteBtn.set_sensitive(True)
	self.editBtn.set_sensitive(True)
	for path in pathlist :
	    tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter,0)

	#Logout
    def onLogoutButtonPressed(self, button):
	self.window.destroy()
	self.window=login.loginClass()   
