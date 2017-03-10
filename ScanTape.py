#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import maryam

class ScanTape():
	builder =None
	window = None
	barcode1=None
	tapesList = None
	userType = None
	Username=None
	def __init__(self, tl,username,kind ):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ScanMoreInterface.glade")
		self.window = self.builder.get_object("window1")
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
			checkBarcode=c.fetchone()
	
			if checkBarcode != None:
				#move to tapes info with the specific barcode
				print checkBarcode[0]
				self.window.destroy()
				self.window =maryam.tapeInfo(checkBarcode[0] , self.tapesList,self.Username,self.userType)
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



###back on scan will check if user or admin		

