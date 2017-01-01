#!/usr/bin/python
# the application starts from here
import sqlite3
from common import id_generator,send_email
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import login
window=login.loginClass()
Gtk.main()
