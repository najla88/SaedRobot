import sqlite3
import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

con = sqlite3.connect('SaedRobot.db')
cur = con.cursor()
cur.execute("SELECT VOLSER from inventory")
software_list = cur.fetchall()


class ManageRack(Gtk.Window):
	
	builder =None
	window= None
	box = None
    
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("A.glade")
		self.window = self.builder.get_object("window1")
		grid=self.builder.get_object("grid3")
		AddBtn=self.builder.get_object("AddBtn")
		DelBtn=self.builder.get_object("DelBtn")
		backBtn=self.builder.get_object("backBtn")
		
		AddBtn.connect("clicked",self.Add)
		DelBtn.connect("clicked",self.Del)
		backBtn.connect("clicked",self.back)

	        #Creating the ListStore model
        	self.software_liststore = Gtk.ListStore(str)
        	for software_ref in software_list:
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
        	grid.attach(self.scrollable_treelist, 0, 0, 1, 1)
        	self.scrollable_treelist.add(self.treeview)

        	self.window.show_all()


	def Add(self,button):
		self.window.destroy()
		self.window=AddRack()

	def Del(self,button):
		self.window.destroy()
		#self.window=login()
	def back(self,button):
		self.window.destroy()
		#self.window=login()
	
	


class AddRack():
	
	builder =None
	window = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("A.glade")
		self.window = self.builder.get_object("window2")

		AddBtn=self.builder.get_object("AddBtn")
		backBtn=self.builder.get_object("backBtn")
		
		AddBtn.connect("clicked",self.Add)
		backBtn.connect("clicked",self.back)

		self.window.show()


	def back(self,button):
		self.window.destroy()
		self.window=ManageRack()

	def Add(self,button):
		self.window.destroy()
		#self.window=ManageRack()

window=ManageRack()
Gtk.main()
