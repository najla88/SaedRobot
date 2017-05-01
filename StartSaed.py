#!/usr/bin/python

########################################################################
# 				   written by : Najla AlGhofaili, CS,				   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#   	This is the file where the application will start from    	   #
#   			It is linked with the login interface			 	   #
#																	   #
########################################################################

import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login
window=login.loginClass()
Gtk.main()
