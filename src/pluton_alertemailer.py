#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Lyon <david.lyon@clixx.io>'
__version__ = '0.1'
__license__ = 'GPLv3'
__source__ = 'https://github.com/clixx-io/pluton-cryptobot/tree/master/src/pluton_alertemailer.py'

"""
Pluton - A python Trading-Bot.
Copyright (C) 2018 David Lyon <david.lyon@clixx.io>
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
.. note:: All requests and responses will be JSON
"""

import os, argparse, configparser
from appdirs import *
import sys, getopt, time, json, locale, re
import smtplib
import paho.mqtt.client as mqtt
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

appname = "Pluton"
appauthor = "Clixx.io Pty Limited"
appconfig = "pluton.ini"
apph5data = "pluton.h5"

appdatadir= user_data_dir(appname, appauthor)
if not os.path.exists(appdatadir):
    print("Creating directory %s for configuration file" % appdatadir)
    os.makedirs(appdatadir)

appfullconfig = os.path.join(appdatadir,appconfig)
apph5datafile = os.path.join(appdatadir,apph5data)

config = configparser.ConfigParser(allow_no_value=True)
config.read(appfullconfig)

def rot13(s):
    result = ""

    # Loop over characters.
    for v in s:
        # Convert to number with ord.
        c = ord(v)

        # Shift number back or forward.
        if c >= ord('a') and c <= ord('z'):
            if c > ord('m'):
                c -= 13
            else:
                c += 13
        elif c >= ord('A') and c <= ord('Z'):
            if c > ord('M'):
                c -= 13
            else:
                c += 13

        # Append to result.
        result += chr(c)

    # Return transformation.
    return result
    
def on_connect(client, userdata, flags, rc):
    print("Alert Emailer Connected to Broker. Waiting for Email Alerts")
    client.subscribe("pluton/alert/email")

def on_message(client, userdata, msg):

    global appdatadir
    global config
    originator = None
    recipient = None
    coincode = None
    alerttype = None

    alertdata = json.loads(str(msg.payload))
    
    if 'SMTP_Configuration' in config.sections():

        if config.has_option('SMTP_Configuration', 'originator'):
            originator = config.get('SMTP_Configuration','originator')
    else:
        print("ERROR: Cannot send emails. No SMTP Email Configuration.")
        return
            
    coincode = alertdata["Coin"]
    alerttype = alertdata["AlertType"]
    
    print("Sending Alert Email for %s" % coincode)
     
    msg = MIMEMultipart('alternative')
    msg['To'] = recipient
    msg['From'] = originator
    msg['Subject'] = "%s Alert for %s" % (alerttype,coincode)

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nThis is a Buy Alert for XRP. Here is the link :\n https://www.coinspot.com.au/buy/xrp"
    html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       This is a Buy Alert for XRP. Here is the link <a href="https://www.coinspot.com.au/buy/xrp">link</a>.
    </p>
  </body>
</html>
"""

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP(config.get('SMTP_Configuration','server'))
    s.login(config.get('SMTP_Configuration','uid'), config.get('SMTP_Configuration','acs'))
    s.sendmail(sndr, recipient, msg.as_string())
    s.quit()

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker", default='127.0.0.1', help="MQTT Broker Address")
    parser.add_argument("--config", default=appfullconfig, help="Specify the Configuration file to use")

    args = parser.parse_args()
	
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.broker, 1883)

    client.loop_forever()
