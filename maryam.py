#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login

class userHome():
	
	builder =None
	window = None
	
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window1")
		createTaskBtn=self.builder.get_object("createTaskBtn")
		changePasswordBtn=self.builder.get_object("changePasswordBtn")
		createTaskBtn.connect("clicked",self.createTask)
		changePasswordBtn.connect("clicked",self.changePassword)

		self.window.show()


	def createTask(self,button):
		
		
		self.window.destroy()
		self.window =create_task()
		##we should have create task class
			
	def changePassword(self,button):
		self.window.destroy()
		window2 = login.change_password()


#window=userHome()
#Gtk.main()
