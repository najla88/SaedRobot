import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import string
import random
import smtplib

sender = '2130005582@uod.edu.sa'
receivers = ['2130005582@uod.edu.sa']

message = """From: From Person <2130005582@uod.edu.sa>
To: To Person <2130005582@uod.edu.sa>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    print(''.join(random.choice(chars) for _ in range(size)))

class Handler:

    def onDeleteWindow(self, *args): 
        Gtk.main_quit(*args)

    def onCreateNewTaskButtonPressed(self, button): 
        print("onCreateNewTaskButtonPressed")

    def onManageUsersAccountsButtonPressed(self, *args):
        id_generator()
        print("onManageUsersAccountsButtonPressed") 
        window = builder.get_object("window2")
        window.show()


    def onManageRacksButtonPressed(self, button):
        print("onManageRacksButtonPressed")

    def onAddUserButtonPressed(self, *args):
        print("onAddUserButtonPressed")
        window = builder.get_object("window3")
        window.show()
id_generator()
builder = Gtk.Builder()
builder.add_from_file("Saed.glade")
builder.connect_signals(Handler())
window = builder.get_object("window1")
window.show()
Gtk.main()

