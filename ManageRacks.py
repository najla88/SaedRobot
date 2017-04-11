#written by : Zainab AlManea, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MainAdminMenu
import AddRacks
import login



class ManageRack():
	
	builder =None
	window= None
	treeview = None
	scrollable_treelist = None
	DelBtn = None
	grid = None
	tree_selection = None
	software_liststore = None
	current_filter_language = None
	language_filter = None
	userType= None
	Username= None
	
	#starting function
	def __init__(self, username, kind):
		
		#connect to the db
		db = sqlite3.connect('SaedRobot.db')
		cur = db.cursor()
		cur.execute("SELECT RACKNAME from movement where STATE=1")
		list1 = cur.fetchall()
		db.close()
		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ManageRack.glade")
		self.window = self.builder.get_object("window1")
		
		#get all the objects
		self.grid=self.builder.get_object("grid3")
		AddBtn=self.builder.get_object("AddBtn")
		self.DelBtn=self.builder.get_object("DelBtn")
		logoutBtn=self.builder.get_object("logoutBtn")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)
		backbox=self.builder.get_object("backBtn")
		backbox.connect("button-release-event",self.back)
		
		
		AddBtn.connect("clicked",self.Add)
		self.DelBtn.set_sensitive(False)
		self.userType=kind
		self.Username=username
	        #Creating the ListStore model
        	self.software_liststore = Gtk.ListStore(str)
        	for software_ref in list1:
            	    self.software_liststore.append(list(software_ref))
        	self.current_filter_language = None

        	#Creating the filter, feeding it with the liststore model
        	self.language_filter = self.software_liststore.filter_new()


        	#creating the treeview, making it use the filter as a model, and adding the columns
        	self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        	for i, column_title in enumerate(["Rack Name"]):
                    renderer = Gtk.CellRendererText()
                    column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                    self.treeview.append_column(column)

        	#setting up the layout, putting the treeview in a scrollwindow
        	self.scrollable_treelist = Gtk.ScrolledWindow()
        	self.scrollable_treelist.set_vexpand(True)
        	self.scrollable_treelist.set_hexpand(True)
        	self.grid.attach(self.scrollable_treelist, 0, 0, 1, 1)
        	self.scrollable_treelist.add(self.treeview)		
        		
		self.tree_selection = self.treeview.get_selection()
		self.tree_selection.connect("changed", self.onSelectionChanged)	
		self.DelBtn.connect("clicked",self.Del,self.tree_selection)
		self.window.show_all()

	#go to add rack interface
	def Add(self,button):
		self.window.destroy()
		self.window=AddRacks.AddRack(self.Username, self.userType)

	#delete the selected rack
	def Del(self,button, s):
		#show popup window
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"Are you sure, You want to delete this rack?")
		dialog.set_title("Confirmation message")
		respond=dialog.run()
		
		#yes >> delete
		if respond == Gtk.ResponseType.YES:
			dialog.close()
			model,list_iter = s.get_selected () 
			valu = None
			if list_iter is not None:
				value = model[list_iter][0]
			#connect to db+deactivate the rack
			db1 = sqlite3.connect('SaedRobot.db', timeout = 4000)
			c1 = db1.cursor()
			c1.execute("update movement set STATE=0 where RACKNAME=?" , (value,))
			db1.commit()
			c1.execute("SELECT RACKNAME from movement where STATE=1")
			list3 = c1.fetchall()
			db1.close()
		
				
			self.software_liststore.clear()
		#Creating the ListStore model
        		for software_ref in list3:
            	            self.software_liststore.append(list(software_ref))
        		self.current_filter_language = None

        	#Creating the filter, feeding it with the liststore model
        		self.language_filter = self.software_liststore.filter_new()


        	#creating the treeview, making it use the filter as a model, and adding the columns
        		self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        		for i, column_title in enumerate(["Rack Name"]):
                            renderer = Gtk.CellRendererText()
                            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                            self.treeview.append_column(column)

        	#setting up the layout, putting the treeview in a scrollwindow
        		self.scrollable_treelist = Gtk.ScrolledWindow()
        		self.scrollable_treelist.set_vexpand(True)
        		self.scrollable_treelist.set_hexpand(True)
        		self.grid.attach(self.scrollable_treelist, 0, 0, 1, 1)
        		self.scrollable_treelist.add(self.treeview)	
        		self.tree_selection.unselect_all()
        		self.DelBtn.set_sensitive(False)
        		dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"The Rack has been deleted successfully")
        		dialog.set_title("Confirmation message")
        		dialog1.run()
        		dialog1.close()
        		dialog.close()
		else: 
			
				dialog.close()
	#back to Home Admin
	def back(self,button,a):
		self.window.destroy()
		self.window=MainAdminMenu.MainAdminMenu(self.Username, self.userType)
	
	#activate delete button for the selected item
	def onSelectionChanged(self, tree_selection) :
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print value
			self.DelBtn.set_sensitive(True)
	
	#Logout
	def onLogoutButtonPressedButtonPressed(self, button):
		self.window.destroy()
		self.window=login.loginClass() 
		




