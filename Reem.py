import sqlite3
import gi
import json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

con = sqlite3.connect('SaedRobot.db')
cur = con.cursor()
cur.execute("SELECT USERNAME, EMAIL from users")
software_list = cur.fetchall()


class TreeViewFilterWindow(Gtk.Window):

    builder = None
    window = None
    box = None
    def __init__(self):
	self.builder = Gtk.Builder()
	self.builder.add_from_file("Saed.glade")
	self.window = self.builder.get_object("window2")	
	box=self.builder.get_object("boxxx")


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
        self.scrollable_treelist.set_hexpand(False)
        box.attach(self.scrollable_treelist, 0,0,1,1)
        self.scrollable_treelist.add(self.treeview)

        self.window.show_all()

window = TreeViewFilterWindow()
Gtk.main()
