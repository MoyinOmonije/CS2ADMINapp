from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import schedule
import time

def mail(msg_to_send):  # this method handles the sending of summary emails to the convenor. Credit to GeeksforGeeks

    # setting up a connection to our email server.
    # we used a gmail account for this application's address
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    # Login with our email and password
    smtp.login('cs2.conApp@gmail.com', 'tuwiehqyaiplwsap')

    # the content of the message
    msg = MIMEMultipart()  # the content of the message
    msg['Subject'] = 'Summary from CS2 Admin app'  # the email subject
    msg.attach(MIMEText(msg_to_send))  # the text contents

    # send the email
    to = ["mrlore001@myuct.ac.za"]  # recepient email
    smtp.sendmail(from_addr="cs2.conApp@gmail.com",
    			to_addrs=to, msg=msg.as_string())
    smtp.quit()  # close the connection
