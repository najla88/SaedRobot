#!/usr/bin/python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class login():
	builder =None
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Loin.glade")
		window = self.builder.get_object("window1")
		usernameBtn=self.builder.get_object("loginBtn")
		usernameBtn.connect("clicked",self.login)
		window.show()

	def login(self,button):
		
		username = self.builder.get_object("username")
		password = self.builder.get_object("password")
		print username.get_text() + password.get_text()

		
		
window=login()
Gtk.main()


"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import gi.repository

class adder:


	def __init__( self, number1, number2 ):
		self.result = int( number1 ) + int( number2 )

	def giveResult( self ):
		return str(self.result)

class leeroyjenkins:

	wTree = None
	def __init__( self ):
		self.wTree = Gtk.Builder()
		self.wTree.add_from_file("Loin.glade")
		#self.wTree = builder.XML( "Loin.glade" )
		
		dic = { "on_button1_clicked" : self.add,}
		self.wTree.connect_signals( dic )
		window = self.wTree.get_object("window1")
		button=self.wTree.get_object("button1")
		a=self.wTree.get_object("entry1")
		window.show()
		Gtk.main()


	def add(self, widget):
#thistime = adder( self.wTree.get_widget("entryNumber1").get_text(), self.wTree.get_widget("entryNumber2").get_text() )
		st=self.wTree.get_widget("entry1").get_text()
		print st
		self.wTree.get_widget("entry").set_text("new")


letsdothis = leeroyjenkins()
"""
