#!/usr/bin/env python
import string
import random
import smtplib



def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return(''.join(random.choice(chars) for _ in range(size)))



def send_email(Password,Subject):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("reem.aljunaid.94@gmail.com", "Vdl 4206")
	password = Password
	subject = Subject
	msg = 'Your password is '+ password
	message = 'Subject: {}\n\n{}'.format(subject, msg)
	server.sendmail("reem.aljunaid.94@gmail.com", "reem.aljunaid@hotmail.com", message)
