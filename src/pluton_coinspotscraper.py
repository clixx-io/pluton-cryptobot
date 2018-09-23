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

import sys, getopt
import time, urllib2
import argparse, configparser, json, locale, re
from bs4 import BeautifulSoup
import paho.mqtt.publish as publish

# specify the url
quote_page = "https://www.coinspot.com.au/buy/"

def scrapeCoin(coincode,broker):
	
    try:
		
        coin_page = quote_page + coincode.lower()
            
        req = urllib2.Request(coin_page,headers=hdr)
            
        page = urllib2.urlopen(req)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, "html.parser")

        # Take out the <div> of name and get its value
        name_box = soup.find('h1', attrs={'class': 'price-title'})

        # Clean up the price, removing currency codes and spaces
        decimal_point_char = locale.localeconv()['decimal_point']
        clean = re.sub(r'[^0-9'+decimal_point_char+r']+', '', str(name_box.text.strip()))
        price = float(clean)
        
        print coincode + ":" + str(price)
        
        if len(broker):
            data = { 'Coin' : coincode, 'Price' : price, 'ts' : time.time() }
            publish.single("pluton/price", json.dumps(data), hostname=broker)

    except urllib2.URLError:
        time.sleep(int(percoin_interval))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("coin", metavar='Coin', nargs='*',default='*', help="Coin Code")
    parser.add_argument("--broker", default='127.0.0.1', help="MQTT Broker Address")
    parser.add_argument("--interval", default=30, help="Interval between Scraping Attempts (secs)")

    args = parser.parse_args()

    coinList = getattr(args, 'coin')

    if args.broker:
        mqtt_host = args.broker
        print 'Publishing Price Data to MQTT Broker ', args.broker
        
    # query the website and return the html to the variable page
    hdr = {'User-Agent': 'Mozilla/5.0'}

    percoin_interval = 30

    print("You asked to monitor coins %s" % (coinList))

    while True:

        try:

            for coin in coinList:

                scrapeCoin(coin,args.broker)

                time.sleep(args.interval)

        except Exception as e: 
            print(e)

