import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import string
import random

import smtplib

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return(''.join(random.choice(chars) for _ in range(size)))



server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login("reem.aljunaid.94@gmail.com", "Vdl 4206")
password = id_generator()
subject = "Sa'ed Robot"
msg = 'Your password is '+ password
message = 'Subject: {}\n\n{}'.format(subject, msg)
server.sendmail("reem.aljunaid.94@gmail.com", "reem.aljunaid@hotmail.com", message)


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

