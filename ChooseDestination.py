import sqlite3
import gi
import json
import login
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MainAdminMenu
import login






class ChooseDes():
	
	builder =None
	window= None
	treeview = None
	scrollable_treelist = None
	GoBtn = None
	grid = None
	tree_selection = None
	software_liststore = None
	current_filter_language = None
	language_filter = None
	userType=None
	Username=None
	list_tapes=None
	
	
	def __init__(self, tl,username,kind):
	#def __init__(self):
		db = sqlite3.connect('SaedRobot.db')
		cur = db.cursor()
		cur.execute("SELECT RACKNAME from movement where STATE=1")
		list1 = cur.fetchall()
		db.close()
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ChooseDes.glade")
		self.window = self.builder.get_object("window1")
		self.grid=self.builder.get_object("grid3")
		self.GoBtn=self.builder.get_object("GoBtn")
		backBtn=self.builder.get_object("backBtn")
		backBtn.connect("clicked",self.back)
		self.GoBtn.set_sensitive(False)
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)
		self.list_tapes=tl
		self.userType=kind
		self.Username= username

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
		self.GoBtn.connect("clicked",self.Go,self.tree_selection)
		self.window.show_all()


	

	def Go(self,button, s):
			self.list_tapes = list()
			#self.list_tapes.append("C00001")
			#self.list_tapes.append("C00002")
			#self.list_tapes.append("C00003")
			index=len(self.list_tapes)
			print index
			model,list_iter = s.get_selected () 
			value = None
			if list_iter is not None:
				value = model[list_iter][0]
			
			newlist=self.list_tapes[0:]
			
			for VOLSER in self.list_tapes:
				db1 = sqlite3.connect('SaedRobot.db', timeout = 4000)
				c1 = db1.cursor()
				c1.execute("SELECT RACK from inventory where VOLSER=?" , (VOLSER,))
				Rack1 = c1.fetchone()
				print "here + "+"VOLSER :"+VOLSER+" the rack:"+Rack1[0]
				
			
				if Rack1[0] == value:
					print "tammam"
 
					
				else:
					print "error"
					dialog2 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"The selected destination: "+value +" for the tape: "+VOLSER+" is not compatable with our database. Proceed anyway?")
					respond=dialog2.run()
					if respond == Gtk.ResponseType.YES:
						print "respond is yes"
						dialog2.destroy()
					else: 
						print newlist						
						newlist.remove(VOLSER)
						print newlist
						dialog2.destroy()
						
						
						
							
			sa=len(newlist)
			print sa
			if sa==0:
				dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"There is NO tape to deliver")
				dialog1.run()
				dialog1.close()
				
			
			elif sa!=0:
				dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"Delivery is in progress")
				dialog1.run()
				dialog1.close()
			
				
				
			
			
			self.window.destroy()
			self.window=login.login()
			
	def back(self,button):
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"Do you want to cancel this task?")
		respond=dialog.run()
		if respond == Gtk.ResponseType.YES:
			print "Yes"
			if (self.userType==1):
				self.window.destroy()
				del self.tapesList[:]
				self.window=MainAdminMenu.MainAdminMenu(self.Username,self.userType)
				#self.window=MainAdminMenu.MainAdminMenu()
				dialog.close()
			else:
				self.window.destroy()
				del self.tapesList[:]
				self.window=maryam.userHome(self.Username,self.userType)
				print self.tapesList
				dialog.close()

		elif respond == Gtk.ResponseType.NO:
			print "No"
			dialog.close()
			
				
			
			



###back on scan will check if user or admin	
		
	def onSelectionChanged(self, tree_selection) :
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			print value
			self.GoBtn.set_sensitive(True)

	

    def onLogoutButtonPressedButtonPressed(self, button):
		self.window.destroy()
		self.window=login.loginClass() 

