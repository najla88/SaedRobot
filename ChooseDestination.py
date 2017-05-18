
########################################################################
# 				   written by : Zainab AlManea, CS,					   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#   	This interface will allow the user to choose the desired   	   #
#   				destination for the delivery task	  			   #
#																	   #
########################################################################

import sqlite3
import gi
import json
import login
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import MainAdminMenu
import login
import MainUserMenu
import time, sys, serial


# SERIAL INIT
defaultPort = "/dev/tty.ROBOTISBT-210-SPPDev" # change to suit your needs
ser = serial.Serial()
TIMEOUT = 5 # max number of sensor request attempts

#servo ID's 
BROADCASTID = 254


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
	
	#starting function
	def __init__(self, tl,username,kind):
		
		#set the list of racks, username, and user type
		self.list_tapes=tl
		self.userType=kind
		self.Username= username
		
		#connect to the db
		#db = sqlite3.connect('SaedRobot.db')
		#cur = db.cursor()
		#cur.execute("SELECT RACKNAME from movement where STATE=1")
			
		#list1 = cur.fetchall()
		#db.close()
		print self.list_tapes
		print (3-len(self.list_tapes))
		arwa = 3-len(self.list_tapes)
		db = sqlite3.connect('SaedRobot.db')
		cur = db.cursor()
		cur.execute("select rackname from (select rackstatus.rackname as rackname ,count(inventory.rack) as countt from  rackstatus  left join inventory on rackstatus.rackname= inventory.rack where rackstatus.status=1  group by rackstatus.rackname) where countt<= ?",(arwa,))
		list1 = cur.fetchall()
		db.close()
		
		print list1

		
		#connect to the desired window from glade file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ChooseDes.glade")
		self.window = self.builder.get_object("window1")
		
		#get all the objects
		self.grid=self.builder.get_object("grid3")
		self.GoBtn=self.builder.get_object("GoBtn")
		self.GoBtn.set_sensitive(False)
		logoutBtn=self.builder.get_object("logoutBtn1")
		logoutBtn.connect("clicked",self.onLogoutButtonPressedButtonPressed)
		
		
		backbox=self.builder.get_object("backBtn")
		backbox.connect("button-release-event",self.back)

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


	
	#go button
	def Go(self,button, s):
			index=len(self.list_tapes)
			model,list_iter = s.get_selected () 
			value = None
			if list_iter is not None:
				value = model[list_iter][0]
			
			newlist=self.list_tapes[0:]
			
			for VOLSER in self.list_tapes:
				#connect+query the db to get the right volser position
				db1 = sqlite3.connect('SaedRobot.db', timeout = 4000)
				c1 = db1.cursor()
				c1.execute("SELECT RACK from inventory where VOLSER=?" , (VOLSER,))
				Rack1 = c1.fetchone()
				
			    # if the rack is not compatible with our db then popup message will appear
				if not(Rack1[0] == value):
					dialog2 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"The selected destination: "+value +" for the tape: "+VOLSER+" is not compatable with our database. Proceed anyway?")
					dialog2.set_title("Confirmation message")
					respond=dialog2.run()
					if respond == Gtk.ResponseType.YES:
						dialog2.destroy()
					else: 
						newlist.remove(VOLSER)
						dialog2.destroy()
						
						
						
							
			sa=len(newlist)
			#no tapes
			if sa==0:
				dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"There is NO tape to deliver")
				dialog1.set_title("Error message")
				dialog1.run()
				dialog1.close()
				
				
			#successful delivery
			elif sa!=0:
				
				#value is the rack chosen  
				#newlist is the tapes list
				
				db = sqlite3.connect('SaedRobot.db')
				cur = db.cursor()
				cur.execute("select slot from inventory where RACK=?;",(value,))
				slotsList = cur.fetchall()
				print "slots in db"
				print slotsList
				DeliveryList =[1,2,3]

				for item in slotsList:
					if item[0] in DeliveryList:
						DeliveryList.remove(item[0])
					print item

				print "items in del lis"
				print DeliveryList
				
	
				db.close()
				racknumber=value
				slot1=0
				slot2=0
				slot3=0
				DeliveryList=DeliveryList[:len(newlist)]
				looping=len(newlist)
				for i in range (looping ,3):
					DeliveryList.append(0)
				
				slot1=DeliveryList[0]
				slot2=DeliveryList[1]
				slot3=DeliveryList[2]	
				
				
				print "final delivery list"

				print DeliveryList
				
				aa= self.preparePacket(value,slot1,slot2,slot3)
				print aa
				
				self.initCom(defaultPort);
				self.sendPacket(packet);
				self.closeCom();
				dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Delivery is in progress")
				dialog1.set_title("Confirmation message")
				dialog1.run()
				dialog1.close()
			
				
				
			
			
			self.window.destroy()
			self.window=login.loginClass()
	
	#back button		
	def back(self,button,a):
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"Do you want to cancel this task?")
		respond=dialog.run()
		if respond == Gtk.ResponseType.YES:

			if (self.userType==1):
				self.window.destroy()
				del self.list_tapes[:]
				self.window=MainAdminMenu.MainAdminMenu(self.Username,self.userType)
				dialog.close()
			else:
				self.window.destroy()
				del self.list_tapes[:]
				self.window=MainUserMenu.userHome(self.Username,self.userType)
				dialog.close()

		elif respond == Gtk.ResponseType.NO:
			dialog.close()
			
				
			
			



###back on scan will check if user or admin	
		
	def onSelectionChanged(self, tree_selection) :
		(model, pathlist) = tree_selection.get_selected_rows()
		for path in pathlist :
			tree_iter = model.get_iter(path)
			value = model.get_value(tree_iter,0)
			self.GoBtn.set_sensitive(True)

	
	#Logout
	def onLogoutButtonPressedButtonPressed(self, button):
		self.window.destroy()
		self.window=login.loginClass() 
		
	def convertHexa(self,hexaRack):
		if len(hexaRack) == 4:
			return hexaRack
	
		elif len(hexaRack)<4:
			lengthHexaRack = len(hexaRack)
			for i in range(lengthHexaRack,4):	
				hexaRack= "0" +hexaRack
			return hexaRack
		
	
	def convertInverse(self,hexaRackInverse):
		if len(hexaRackInverse) == 4:
			return hexaRackInverse
	
		elif len(hexaRackInverse)<4:
			lengthHexaRack = len(hexaRackInverse)
			for i in range(lengthHexaRack,4):	
				hexaRackInverse= "F" +hexaRackInverse
			return hexaRackInverse
	

	def preparePacket(self, rack, slot1, slot2, slot3):
	
		dataLow=0
		dataLowInverse=0

		dataHigh=0
		dataHighInverse=0
		dic = {'A':1 ,'B':2, 'C':3 ,'D':4 ,'E':5 ,'F':6 ,'G':7 ,'H':8 ,'I':9}
		rack = dic[rack]
		combineLine=str(rack)+str(slot1)+str(slot2)+str(slot3)
		print combineLine
	
		hexaRack = hex(int(combineLine))
		hexaInverseRack = hex( int (hexaRack, base=16) ^ 0xFFFF)

		hexaRack = self.convertHexa(hexaRack[2:])
		hexaInverseRack = self.convertInverse(hexaInverseRack[2:])
		dataLow= hexaRack[2:4]
		dataLowInverse= hexaInverseRack[2:4]
		dataHigh= hexaRack[0:2]
		dataHighInverse= hexaInverseRack[0:2]
		packet= "\\xFF\\x55\\x"+str(dataLow).upper() +"\\x"+str(dataLowInverse).upper() +"\\x"+str(dataHigh).upper() +"\\x"+str(dataHighInverse).upper()
		return packet
	
		
	def initCom(self,port):
	    ser.baudrate = 38400
	    ser.port = port
	    ser.timeout = 0.5
	    ser.open()
	
	def closeCom(self):
	    ser.close() # close serial connection so it is available in future
	# end SERIAL INIT
	
	# PACKET HANDLING
	def readPacket(self):
	    frameIncomplete = True
	    frameByteIndex = -1
	    checkSum = 0
	    packet = [0, 0, 0, 0, 0, 0]
	    #print('reading packet...')
	    while ser.inWaiting() > 0 and frameIncomplete:
	        byteValue = repr(ser.read()).lstrip('b').strip('\'')
	    #print repr(byteValue)
	        if len(byteValue) != 4: # python uses Unicode in some cases instead of hex
	            if byteValue == '\\\\': # python hex value is converted to char
	                value = 92 # correct value
	            elif byteValue == '\\t':
	                value = 9
	            elif byteValue == '\\n':
	                value = 10
	            else:
	                value = ord(byteValue)
	        else:
	            value = int(byteValue.lstrip('\\').lstrip('x'), 16)
	        #print('read: ' + byteValue + '...')
	        if frameByteIndex == -1:
	            if value == 255: # encountered frame beginning
	                frameByteIndex = 0
	                #print('frame start...')
	        elif frameByteIndex == 6: # frame is complete
	            packetCheckSum = ser.read()
	            frameIncomplete = False
	            # TODO: verify checkSum here
	        else: # get values in frame
	            packet[frameByteIndex] = value
	            checkSum = checkSum + value
	            frameByteIndex = frameByteIndex + 1
	    #print('packet complete...')
	    return packet
	
	def sendPacket(self,packet):
	    
	  
	    #ser.write(chr(255 - ((packet[0] + packet[1] + packet[2] + packet[3] + packet[4] + packet[5]) % 256))) # checksum
	    ser.write(packet)
	    time.sleep(0.030303030303030303) # this very roughly sends commands at 33Hz
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
