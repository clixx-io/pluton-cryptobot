#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'David Lyon'

"""
Pluton CryptoBot Data Scraping Interface
"""

import os
import argparse
import configparser
from datetime import datetime,timedelta,date
from pandas import HDFStore, DataFrame, read_hdf
from appdirs import *
import dumper
from cryptocmd import CmcScraper

appname = "Pluton"
appauthor = "Clixx.io Pty Limited"
appconfig = "pluton.ini"
apph5data = "pluton.h5"

coin = "BTC"
appstore  = "pluton.h5"

appdatadir= user_data_dir(appname, appauthor)
if not os.path.exists(appdatadir):
    print("Creating directory %s for configuration file" % appdatadir)
    os.makedirs(appdatadir)

appfullconfig = os.path.join(appdatadir,appconfig)
apph5datafile = os.path.join(appdatadir,apph5data)

config = configparser.ConfigParser(allow_no_value=True)
config.read(appfullconfig)

def updateCoins(coinCodes):
    """Update the H5 Repository with Coin Data

    Keyword arguments:
    coinList - Set of CoinCodes
    """

    global apph5datafile
    
    coinList = []
    
    if coinCodes == '*':
        print("You asked to update all tracked coins")
        coinList = config.get('Active','Coins').split(' ')
    else:
        coinList = coinCodes
        print("You asked to list the last week for coins %s" % (coinList))
   
    print("You asked to update coins %s" % (coinList))

    for coin in coinList:

        havecointable = True
        
        if not os.path.exists(apph5datafile):
            print("Creating Datafile %s" % apph5datafile)
            havecointable = False

#        if not ('/'+coin.upper()) in storedcoins:
#            print("Coin %s not in dataset" % coin.upper())
#            havecointable = False

        if havecointable:

            try:
                hdf = read_hdf(apph5datafile,coin)

                hdf['date_ranked']=hdf['Date'].rank(ascending=1)
                print "Last element from %s is dated %s" % (coin,str(hdf.at[0,'Date'])[:10])
                lastdate = datetime.strptime(str(hdf.at[0,'Date'])[:10],"%Y-%m-%d")
                nextday = timedelta(1)
                nextday = lastdate + nextday
                delta = (datetime.today() - timedelta(1)) - nextday
                print("Difference from yesterday to last update ", delta)

            except KeyError:
                print("No data found for this Coin")
                nextday = (datetime.today() - timedelta(2*365))

            lastdate = datetime.today() - timedelta(1)

            print "Updating data from %s to %s" % (str(nextday),str(lastdate))

            startdate = '{:%d-%m-%Y}'.format(nextday)
            enddate = '{:%d-%m-%Y}'.format(lastdate)

            scraper = CmcScraper(coin,startdate,enddate)

        else:

            scraper = CmcScraper(coin.upper())

        # get data as list of list
        try:
            headers, data = scraper.get_data()

            # get dataframe for the data
            df = scraper.get_dataframe()

            print df

            # df.to_hdf('pluton.h5',coin,append=True,format='t')
            df.to_hdf(apph5datafile,coin.upper())

        except ValueError:
            print("No data found")


    return
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("coin", metavar='Coin', nargs='*',help="Coin Code",default='*')
	
    args = parser.parse_args()
	
    coincode = getattr(args, 'coin')
	
    updateCoins(coincode)
	
