import os
import smtplib
from string import Template


def create_message(template_folder, **kwargs):
    with open(template_folder) as template_file:
        message = Template(template_file.read())

    message = message.substitute(kwargs)
    return message


def send_email(sender_email, to_email, message):
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
