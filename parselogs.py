#!/usr/bin/python3

import os
import subprocess
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

mailpwd = ''
send_email = ''
recv_email = ''
default_log_path = '/home/niftynei/.lightning/logs/log'

logfile = sys.argv[1] if len(sys.argv) > 1 else default_log_path

f = open(logfile, 'r')
counter = 0
errs = ''
for line in f:
    counter += 1
    if 'BROKEN' in line:
        errs += '{}|\t{}'.format(counter, line)

f.close()

# If there's an error, mail the logfile somewhere!
if len(errs):
    email_msg = MIMEMultipart()
    email_msg['From'] = recv_email
    email_msg['To'] = recv_email
    email_msg['Subject'] = "BROKEN: core-lightning logfail"

    email_msg.attach(MIMEText(errs, 'plain'))

    logfile_part = MIMEBase('application', 'lzma')

    cmd = 'lzma -k --threads=2 {}'.format(logfile)
    comp_file = '{}.lzma'.format(logfile)
    subprocess.run(cmd.split(), check=True)

    with open(comp_file, 'rb') as zipped:
        logfile_part.set_payload(zipped.read())

    os.remove(comp_file)
    encoders.encode_base64(logfile_part)
    logfile_part.add_header('Content-Disposition', 'attachment; filename= lightning-log.lzma')
    email_msg.attach(logfile_part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(send_email, mailpwd)
    server.sendmail(send_email, recv_email, email_msg.as_string())
    server.quit()
