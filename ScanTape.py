#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import maryam
import MainAdminMenu

class ScanTape():
	builder =None
	window = None
	barcode1=None
	tapesList = None
	userType = None
	Username=None
	checkBarcode = None
	
	def __init__(self, tl,username,kind ):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ScanMoreInterface.glade")
		self.window = self.builder.get_object("window1")
		backBtn=self.builder.get_object("backBtn")
		backBtn.connect("clicked",self.back)
		#######################################################
		self.userType=kind
		self.Username= username
		########################################################
		
		
		# connect the buttons and make their event listener
		ScanBtn=self.builder.get_object("Scan")
		self.barcode1 = self.builder.get_object("barcode")
		ScanBtn.connect("clicked",self.Scan)
		self.tapesList= tl
		if self.tapesList != None:
			print self.tapesList
		#show
		self.window.show()
	
	def Scan(self,button):
		#Get the Barcode and move to tape info interface
		barcode=self.barcode1.get_text()
		if barcode != None:
			print "Scanned Barcode is: "+barcode
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			#check if the barcode belongs to the database
			c.execute("SELECT * from inventory WHERE volser=?",(barcode,))
			self.checkBarcode=c.fetchone()
	
			if self.checkBarcode != None:
				#move to tapes info with the specific barcode
				if self.checkBarcode[0] in self.tapesList :
					dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"You have already scanned this tap")
					dialog.run()
					dialog.close()
					self.barcode1.set_text("")
					
				else :
					print self.checkBarcode[0]
					self.window.destroy()
					self.window =maryam.tapeInfo(self.checkBarcode[0] , self.tapesList,self.Username,self.userType)
			else:
				 # if Barcode is not in the DB alert with warning message 
				dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"Scanned barcode does not belong to our database .. try another one")
				dialog.run()
				dialog.close()
				print "Warning dialog closed"
		else:
			 # if no Barcode was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.WARNING,Gtk.ButtonsType.OK,"Barcode is not detected .. Try Again")
			dialog.run()
			dialog.close()
			print "Warning dialog closed"
			
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

