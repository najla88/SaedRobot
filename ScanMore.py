#written by : Arwa AlKhunine, CS, Imam Abdulrahman AlFaisal University
import sqlite3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ScanMore():
	builder =None
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ScanMoreInterface.glade")
		window = self.builder.get_object("window1")
		
		# connect the buttons and make their event listener
		ScanBtn=self.builder.get_object("Scan")
		BackBtn=self.builder.get_object("Back")
		NextBtn=self.builder.get_object("Next")
		ScanBtn.connect("clicked",self.Scan)
		BackBtn.connect("clicked",self.Back)
		NextBtn.connect("clicked",self.Next)
		
		#show
		window.show()
		
	def Back(self,button):
		#move to the previous Interface
		print "hi"
		
	def Next(self,button):
		#move to Next Interface to start the delivery process
		print "hi"
	def Scan(self,button):
		#Get the Barcode and move to tape info interface
		while True:
			barcode=raw_input("Scan Barcode: ")
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
		
window=ScanMore()
Gtk.main()
