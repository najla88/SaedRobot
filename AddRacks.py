import sqlite3
import gi
import json
import ManageRacks
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login


class AddRack():

	builder =None
	window= None
	treeview = None
	scrollable_treelist = None
	Add1Btn = None
	grid = None
	tree_selection = None
	software_liststore = None
	current_filter_language = None
	language_filter = None
	userType= None
	Username= None
	
	
	
	def __init__(self, username, kind):
		
		dbA = sqlite3.connect('SaedRobot.db')
		curA = dbA.cursor()
		curA.execute("SELECT RACKNAME from movement where STATE=0")
		list2 = curA.fetchall()
		dbA.close()
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ManageRack.glade")
		self.grid=self.builder.get_object("grid6")
		self.window = self.builder.get_object("window2")
		self.Add1Btn=self.builder.get_object("Add1Btn")
		back1Btn=self.builder.get_object("back1Btn")
		back1Btn.connect("clicked",self.back1)
		self.userType=kind
		self.Username=username
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)
		
	        #Creating the ListStore model
        	self.software_liststore = Gtk.ListStore(str)
        	for software_ref in list2:
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
		self.Add1Btn.connect("clicked",self.Add1,self.tree_selection)

        	
		
		self.window.show_all()



	def back1(self,button):
		self.window.destroy()
		self.window=ManageRacks.ManageRack(self.Username, self.userType)

	def Add1(self,button,s):
		#self.window.destroy()
		model,list_iter = s.get_selected () 
		valu = None
		if list_iter is not None:
		   value = model[list_iter][0]
		dbA1 = sqlite3.connect('SaedRobot.db', timeout = 4000)
		cA1 = dbA1.cursor()
		cA1.execute("update movement set STATE=1 where RACKNAME=?" , (value,))
		dbA1.commit()
		cA1.execute("SELECT RACKNAME from movement where STATE=0")
		list3A = cA1.fetchall()
		dbA1.close()
		#cA1.colse()
		
				
		self.software_liststore.clear()
		#Creating the ListStore model
        	#self.software_liststore = Gtk.ListStore(str)
        	for software_ref in list3A:
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
        	self.Add1Btn.set_sensitive(False)
        	dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"The Rack has been added successfully")
        	dialog1.run()
        	dialog1.close()
        			
        	
		#self.window=ManageRack()

			
	def onSelectionChanged(self, tree_selection) :
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print value
			self.Add1Btn.set_sensitive(True)
			

    def onLogoutButtonPressedButtonPressed(self, button):
		self.window.destroy()
		self.window=login.loginClass() 
			
	
