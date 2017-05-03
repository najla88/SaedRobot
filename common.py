
########################################################################
# 			written by : Reem AlJunaid, Najla AlGhofaili, CS,		   #
# 				Imam Abdulrahman AlFaisal University				   #
#----------------------------------------------------------------------#
#																	   #
#   This files contains the common methods that will be used in many   #
#  							 other files			    			   #
#																	   #
########################################################################


import string
import random
import smtplib


#password generator
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return(''.join(random.choice(chars) for _ in range(size)))
	
#send email function
def send_email(Password,UN,Subject,Email):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("reem.aljunaid.94@gmail.com", "Vdl 4206")
	msg = 'Hello there, \n\nthis is Sa\'ed Robot System \nWe are happy to tell you that your registration process is successfully done\n\n Your Username is: '+ UN +'\n\n Your password is: '+ Password
	message = 'Subject: {}\n\n{}'.format(Subject, msg)
	server.sendmail("reem.aljunaid.94@gmail.com", str(Email), message)
