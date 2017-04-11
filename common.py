#written by : Reem AlJunaid, Najla AlGhofaili CS, Imam Abdulrahman AlFaisal University
import string
import random
import smtplib


#password generator
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return(''.join(random.choice(chars) for _ in range(size)))


#send email function
def send_email(Password,Subject,Email):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("reem.aljunaid.94@gmail.com", "Vdl 4206")
	msg = 'Your password is '+ Password
	message = 'Subject: {}\n\n{}'.format(Subject, msg)
	server.sendmail("reem.aljunaid.94@gmail.com", str(Email), message)
