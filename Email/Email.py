import smtplib
import os

sender = 'brownzach125@gmail.com'
receivers = ['asummers117@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""




#####
## GET YOUR SECRET SPEICAL PASSWORD FROM HERE
## security.google.com/settings/security/apppasswords
#####

############
# Setting up environment variables
# go to run->editconfigurations
# click on the program whose variables you want to edit (the script you want to run this code from some maybe main or email.py
# look for environment variables
# click the ... to the right
# add EMAIL_KEY_FOR_CHARITY=<your key whatever it is>
###


try:
   server = smtplib.SMTP(host='smtp.gmail.com', port=587)
   server.ehlo()
   server.starttls()

   key = os.envirion('EMAIL_KEY_FOR_CHARITY')

   server.login("the account you want to send emails from", key)
   server.sendmail(sender, receivers, message)
   server.close()
   print "Successfully sent email"
except smtplib.SMTPException as err:
   print "Error: unable to send email"