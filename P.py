import serial # import the serial library
import time # import the time library
from Tkinter import * #import Tkinter GUI library 

def red():
	arduino.write('r')

def green():
	arduino.write('g')
	

def blue():
	arduino.write('b')
	

def yellow():
	arduino.write('w')
	

def purple():
	arduino.write('s')
	

def aqua():
	arduino.write('a')

print 'Connecting...'
arduino = serial.Serial(12, 9600)
time.sleep(3)
print 'Connection established successfully'
