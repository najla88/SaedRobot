import sqlite3
import gi
import json
import ManageRacks
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

db = sqlite3.connect('SaedRobot.db')
cur = db.cursor()
cur.execute("SELECT RACKNAME from movement where STATE=1")
list1 = cur.fetchall()


cur.execute("SELECT RACKNAME from movement where STATE=0")
list0 = cur.fetchall()

class ManageRack(Gtk.Window):
	
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
	
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ManageRacks.glade")
		self.window = self.builder.get_object("window1")
		self.grid=self.builder.get_object("grid3")
		AddBtn=self.builder.get_object("AddBtn")
		self.DelBtn=self.builder.get_object("DelBtn")
		backBtn=self.builder.get_object("backBtn")
		
		AddBtn.connect("clicked",self.Add)
		backBtn.connect("clicked",self.back)
		self.DelBtn.set_sensitive(False)

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


	def Add(self,button):
		self.window.destroy()
		self.window=AddRack()

	def Del(self,button, s):
		model,list_iter = s.get_selected () 
		valu = None
		if list_iter is not None:
		   value = model[list_iter][0]
		db1 = sqlite3.connect('SaedRobot.db', timeout = 4000)
		c1 = db1.cursor()
		c1.execute("update movement set STATE=0 where RACKNAME=?" , (value,))
		db1.commit()
		c1.execute("SELECT RACKNAME from movement where STATE=1")
		list3 = c1.fetchall()
		#db1.commit()
		
		
				
		self.software_liststore.clear()
		#Creating the ListStore model
        	#self.software_liststore = Gtk.ListStore(str)
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
		
	def back(self,button):
		self.window.destroy()

		#self.window=login()
		
	def onSelectionChanged(self, tree_selection) :
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print value
			self.DelBtn.set_sensitive(True)

	def fillTable():		
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



class AddRack():
	
	builder =None
	window = None
	
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ManageRacks.glade")
		grid=self.builder.get_object("grid6")
		self.window = self.builder.get_object("window2")

		AddBtn=self.builder.get_object("AddBtn")
		backBtn=self.builder.get_object("backBtn")
		
		AddBtn.connect("clicked",self.Add)
		backBtn.connect("clicked",self.back)


	        #Creating the ListStore model
#Creating the ListStore model
        	self.software_liststore = Gtk.ListStore(str)
        	for software_ref in list0:
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
		s = self.treeview .get_selection ()
		s.connect ( "changed" , yourcallback)

        	#setting up the layout, putting the treeview in a scrollwindow
        	self.scrollable_treelist = Gtk.ScrolledWindow()
        	self.scrollable_treelist.set_vexpand(True)
        	self.scrollable_treelist.set_hexpand(True)
        	self.grid.attach(self.scrollable_treelist, 0, 0, 1, 1)
        	self.scrollable_treelist.add(self.treeview)

		self.window.show_all()


	def back(self,button):
		self.window.destroy()
		self.window=ManageRack()

	def Add(self,button):
		self.window.destroy()
		#self.window=ManageRack()
		

	def yourcallback ( selection ):
		model,list_iter = selection.get_selected ()
		if list_iter != None:
			print "row index = " + model[list_iter][0]


window=ManageRack()
Gtk.main()

