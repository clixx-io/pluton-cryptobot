#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'David Lyon <david.lyon@clixx.io>'
__version__ = '0.1'
__license__ = 'GPLv3'
__source__ = 'https://github.com/clixx-io/pluton-cryptobot/tree/master/src/pluton_pricealerts.py'

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
import paho.mqtt.publish as publish
import sys, getopt
import time
import argparse, configparser, json, locale, re

broker = "127.0.0.1"

pricealerts = [
"{\"Coin\": \"XRP\", \"Price_Above\": 1, \"action\": \"mqtt_alert\",  \"topic\": \"pluton/alert/beeper\" }",
"{\"Coin\": \"XRP\", \"Price_Below\": 0.80, \"action\": \"mqtt_alert\",  \"topic\": \"pluton/alert/beeper\" }"
]

def on_connect(client, userdata, flags, rc):
    print("Price-Alerts Successfully Connected to Broker")

    client.subscribe("pluton/price")

def on_message(client, userdata, msg):
    global broker

    pricedata = json.loads(str(msg.payload))

    for alertstr in pricealerts:

        alert = json.loads(alertstr)
		
        print("Dumping the Alert", alert)

        if (alert["Coin"] == pricedata["Coin"]):
            print("Processing Alert for %s" % (pricedata["Coin"]))
            
            if ("Price_Above" in alert):
                alert_price = alert["Price_Above"]
                if (alert_price < pricedata["Price"]):
                    print("Yes Alert generated ",alert["Price_Above"])
                    publish.single("pluton/alert/beeper", "1", hostname=broker)

            if ("Price_Below" in alert):
                alert_price = alert["Price_Below"]
                if (alert_price > pricedata["Price"]):
                    print("Yes Alert generated ",alert["Price_Below"])
                    publish.single("pluton/alert/beeper", "1", hostname=broker)
			

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument("coin", metavar='Coin', nargs='*',default='*', help="Coin Code")
    parser.add_argument("--broker", default='127.0.0.1', help="MQTT Broker Address")

    args = parser.parse_args()

    broker = args.broker
	
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.broker, 1883)

    client.loop_forever()
