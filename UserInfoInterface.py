
########################################################################
# 					written by : Arwa AlKhunine, CS,				   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#  This interface will show the admin all the user's account from the  #
# 	 db. The admin can manage these account by editing/deleting them   #
#																	   #
########################################################################

import sqlite3
import gi
import updateUserInterface 
import ManageUsersAccounts
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class UserInfo():
	builder =None
	UN =None
	def __init__(self,un):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("UserInfoInterface.glade")
		window = self.builder.get_object("window1")
		# get the objects
		username=self.builder.get_object("UN")
		email=self.builder.get_object("Email")
		# sets the username in the field
		username.set_text(un)
		self.UN = un
		
		# connect the buttons and make their event listener
		EditBtn=self.builder.get_object("Edit")
		BackBtn=self.builder.get_object("Back")
		DeleteBtn=self.builder.get_object("Delete")
		EditBtn.connect("clicked",self.Edit)
		BackBtn.connect("clicked",self.Back)
		DeleteBtn.connect("clicked",self.Delete)
		
		#show
		window.show()
		
		#get the email for the username + display it
		db = sqlite3.connect('SaedRobot.db')
		c = db.cursor()
		c.execute("SELECT email from users WHERE username=? ",(self.UN,))
		getEmail=c.fetchone()
		if getEmail != None:
			email.set_text(getEmail[0])
		else: # if no email was there alert with warning message 
			dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.ERROR,Gtk.ButtonsType.OK,"Something wrong .. Try Again")
			dialog.set_title("Error message")
			dialog.run()
			dialog.close()
		
	def Edit(self,button):
		#move to UpdateUserInterface and pass the username
		window2 = updateUserInterface.UpdateUser(self.UN)
		window2.show()
	def Delete(self,button): # I think its not working!
		
		#should give a proper message or a pop up window as confirmation
		dialog = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.YES_NO,"Information has been updated")
		dialog.set_title("Confirmation message")
		respond=dialog.run()
		if respond == Gtk.ResponseType.YES:
			# connect to the DB + perform the query
			db = sqlite3.connect('SaedRobot.db')
			c = db.cursor()
			c.execute("DELETE FROM users WHERE username=?", (self.UN,))
			db.commit()
			
			#should give a proper message or a pop up window as confirmation
			dialog1 = Gtk.MessageDialog(None,0,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,"Account has been deleted")
			dialog1.set_title("Confirmation message")
			dialog1.run()
			dialog1.close()
			dialog.close()
			#move to the previous interface after deleteing the account and giving the proper Confirmation
			window2 = updateUserInterface.UpdateUser(username.get_text())
			window2.show()
		elif respond == Gtk.ResponseType.NO:
			dialog.close()
		
			
	def Back(self,button): #back to the previous interface
		window3 = ManageUsersAccounts.ManageUsersAccounts()
		window3.show()
		
		
		
