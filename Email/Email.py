import smtplib
import os

sender = 'brownzach125@gmail.com'
receivers = ['asummers117@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

def send_email(to_name, to_email, sender_name, sender_email, subject):
   from_line = "From: {0} <{1}>".format(sender_name, sender_email)
   to_line = "To: {0} <{1}>".format(to_name, to_email)
   subject_line = "Subject: {0}".format(subject)

   message = """From: {0} <{1}>
To: {2} <{3}>
Subject: {4}

Dear {2}
I hope Alex has remembered to change this string to whatever it's supposed to be.
In fact It'd be even better if she changed this to a txt file she loaded in.

With the best wishes
{0}
""".format(sender_name, sender_email, to_name, to_email, subject)

   try:
      server = smtplib.SMTP(host='smtp.gmail.com', port=587)
      server.ehlo()
      server.starttls()

      env_variable = "EMAIL_KEY_FOR_CHARITY"
      key = os.environ.get(env_variable)
      if not key:
         print "Error: " + env_variable + " is not set in the environment read the code for help."
         return False

      server.login(sender_email, key)
      server.sendmail(sender_email, [to_email], message)
      server.close()
      return True
   except smtplib.SMTPException as err:
      print "Error: unable to send email"
      return False

send_email(to_name="Zach Brown", to_email="brownzach125@gmail.com",
           sender_email="brownzach125@gmail.com", sender_name="solevi", subject="FUCK YOU")





