#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Lyon <david.lyon@clixx.io>'
__version__ = '0.1'
__license__ = 'GPLv3'
__source__ = 'https://github.com/clixx-io/pluton-cryptobot/tree/master/src/pluton_alertbeeper.py'

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

import paho.mqtt.client as mqtt
import sys, getopt
import time
import argparse, configparser, json, locale, re

def on_connect(client, userdata, flags, rc):
    print("Alert Beeper Connected to Broker. Waiting for Beep Alerts")
    client.subscribe("pluton/alert/beeper")

def on_message(client, userdata, msg):

    payload = str(msg.payload)
    if len(payload) > 0:
		beepcount = int(msg.payload)
		for b in range(beepcount):
			print('\a')
			time.sleep(1)
    else:
        print('\a')

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker", default='127.0.0.1', help="MQTT Broker Address")

    args = parser.parse_args()
	
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.broker, 1883)

    client.loop_forever()
