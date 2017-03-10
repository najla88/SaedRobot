#!/usr/bin/python2
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login
import changePass

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
		self.window =tapeInfo('C00001')
		##we should have scane class
			
	def changePassword(self,button):
		self.window.destroy()
		window2 = changePass.change_password()
		
class tapeInfo():
	
	builder =None
	window = None
	projectName = None
	tapeName = None
	rackName = None
	slotNumber = None
	
	def __init__(self,a):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("HomeUser.glade")
		self.window = self.builder.get_object("window2")
		proceedBtn=self.builder.get_object("proceedBtn")
		cancelBtn=self.builder.get_object("cancelBtn")
		backBtn=self.builder.get_object("backBtn")
		self.projectName=self.builder.get_object("projectName")
		self.tapeName=self.builder.get_object("tapeName")
		self.rackName=self.builder.get_object("rackName")
		self.slotNumber=self.builder.get_object("slotNumber")
		proceedBtn.connect("clicked",self.back)
		cancelBtn.connect("clicked",self.back)
		backBtn.connect("clicked",self.back)

		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute('SELECT * from inventory WHERE volser= ?' , (a,))
		data=c.fetchone()
		
		if data !=None and len(data)>0:
			self.projectName.set_text(data[1])
			self.tapeName.set_text(data[0])
			self.rackName.set_text(data[2])
			self.slotNumber.set_text(str(data[3]))

		else:
			#loginError.set_text('Invalid username or password, please try again')
			## this sould be in the scan page class
			dialog=Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Could not detect the barcode, please scane again")
			dialog.run()
			dialog.close()
			

		self.window.show()

	def back(self,button):
		self.window.destroy()
		self.window=userHome()
	#def proceed(self,button):
		#self.window.destroy()
		#self.window=scaneMore()
    #def cancel(self,button):
		#self.window.destroy()
		#self.window=scaneTape()

		
# put thim coment chang the window in the first class to window1
#window=create_task()
#Gtk.main()
