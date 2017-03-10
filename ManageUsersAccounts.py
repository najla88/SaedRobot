import sqlite3
import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

con = sqlite3.connect('SaedRobot.db')
cur = con.cursor()
cur.execute("SELECT USERNAME, EMAIL from users")
software_list = cur.fetchall()
		
class ManageUsersAccounts():

    builder = None
    window = None
    box = None
    
    def __init__(self):
	self.builder = Gtk.Builder()
	self.builder.add_from_file("Saed.glade")
	self.window = self.builder.get_object("window2")	
	grid=self.builder.get_object("usersTable")
	addBtn=self.builder.get_object("addBtn")
	backBtn=self.builder.get_object("backBtn")	
	addBtn.connect("clicked",self.onAddUserButtonPressed)
	backBtn.connect("clicked",self.onBackToMainAdminMenuButtonPressed)

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
        grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.scrollable_treelist.add(self.treeview)

        self.window.show_all()


    def onAddUserButtonPressed(self, button):
        import AddNewUser
        self.window.destroy()
        self.window=AddNewUser.AddNewUser()
        
    def onBackToMainAdminMenuButtonPressed(self, button):
	import MainAdminMenu
        self.window.destroy()
        self.window=MainAdminMenu.MainAdminMenu()

#window = ManageUsersAccounts()
#Gtk.main()
