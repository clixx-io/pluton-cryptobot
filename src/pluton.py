#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'David Lyon'

"""
Pluton CryptoBot cmdline Interface
"""

import os, argparse, configparser
from appdirs import *
from datetime import datetime,timedelta,date
from pandas import read_hdf

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

def coinList(coincodes):
    """Display a List of Tracked Coins.

    Keyword arguments:
    coincodes -- '*' (Default) or a set of CoinCode strings.
    """
    
    global config
    
    if coincodes == '*':
        print("You asked to list all tracked coins")
    else:
        print("You asked to list tracked coins like %s" % (coincode))
        
    try:
        print config['Active']['Coins']
    except KeyError:
        print "There are currently No Coins recorded in the Configuration for Tracking"
        
    return
    
def addCoins(coincodes):
    """Add a Coin or set of Coins to the List of Tracked Coins.
    
    Keyword arguments:
    coincodes -- '*' (Default) or a set of CoinCode strings.
    """
        
    global appdatadir
    global config
    activecoins = ""
	
    print("You asked to add a coin %s" % (coincode))
    
    if not 'Active' in config.sections():
		config.add_section('Active')
		
    if config.has_option('Active', 'Coins'):
        activecoins = config.get('Active','Coins') + " "

    newcoins = ' '.join(coincodes)
    
    config.set('Active','Coins', activecoins + newcoins.upper())
    
    with open(appfullconfig, 'w') as configfile:
        config.write(configfile)
    
    return

def deleteCoins(coincodes):
    """Delete a Coin or set of Coins from the List of Tracked Coins.
    
    Keyword arguments:
    coincodes -- '*' (Default) or a set of CoinCode strings.
    """
    
    global appdatadir
    global config
    activecoins = ""
	
    print("You asked to delete coin(s) %s" % (coincode))
    
    if not 'Active' in config.sections():
		print "No coins currently exist in configuration."
		return
		
    if config.has_option('Active', 'Coins'):
        activecoins = config.get('Active','Coins')

    for c in coincodes:
        activecoins = activecoins.replace(c.upper()+' ',' ')
        activecoins = activecoins.replace(c.upper(),' ')
    
    config.set('Active','Coins', activecoins)
    
    with open(appfullconfig, 'w') as configfile:
        config.write(configfile)
    
    return
    	
def coinWeek(coincodes):
    """Display the last week of a set of Coins

    Keyword arguments:
    coincodes -- '*' (Default) or a set of CoinCode strings.
    """
        
    global config
    
    coinlist = []
    
    if coincodes == '*':
        print("You asked to list the last week for all tracked coins")
        coinlist = config.get('Active','Coins').split(' ')
    else:
        coinlist = coincodes
        print("You asked to list the last week for coins %s" % (coinlist))
        
    try:
		
        for coin in coinlist:
			
             hdf = read_hdf(apph5datafile,coin.upper())
             
             hdf['date_ranked'] = hdf['Date'].rank(ascending=1)
             
             print("-------------------------------------------------------\n"
                   "%s\n"
                   "-------------------------------------------------------\n"
                   % coin.upper())
                
             print hdf.head(7)
             print
		
    except KeyError:
        print "There are currently No Coins recorded in the Configuration for Tracking"
        
    return

def showConfig():
    """Display the configuration

    Keyword arguments:
    """

    global appfullconfig, apph5datafile

    cfgfound = "[exists]" if os.path.exists(appfullconfig) else "[not found]"    	    
    print("Using configuration file : %s %s" % (appfullconfig,cfgfound))

    h5found = "[exists]" if os.path.exists(apph5datafile) else "[not found]"
    print("Pandas H5 Data store     : %s %s" % (apph5datafile,h5found))

    return        
    	
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="Actions: list, add [coins], delete [coins], week, config")
    parser.add_argument("coin", metavar='Coin', nargs='*',help="Coin Code",default='*')
    parser.add_argument("--config", default=appfullconfig, help="Specify the Configuration file to use")
	
    args = parser.parse_args()
	
    coincode = getattr(args, 'coin')
	
    if args.action == "add":
        addCoins(coincode)
    elif args.action == "delete":
        deleteCoins(coincode)
    elif args.action == "buysell":
        print("You asked to buysell a coin %s" % (coincode))
        print("Error: Not implemented")
    elif args.action == "graph":
        print("You asked to graph a coin %s" % (coincode))
        print("Error: Not implemented")
    elif args.action == "scan":
        print("You asked to scan a coin %s" % (coincode))
        print("Error: Not implemented")
    elif args.action == "log":
        print("You asked to view the log for coin %s" % (coincode))
        print("Error: Not implemented")
    elif args.action == "update":
        print("You asked to update data for coin %s" % (coincode))
        print("Error: Not implemented")
    elif args.action == "list":
        coinList(coincode)
    elif args.action == "week":
        coinWeek(coincode)
    elif args.action == "config":
		showConfig()
    else:
        print("""You asked for something that isnt supported.
        
Commands:        
    add <coincode> [coincode] ..      - Add one or more Coincodes
    delete <coincode> [coincode] ..   - Delete one or more Coincodes
    analyse <coincode> [coincode] ..  - Analyse one or more Coincodes
    graph <coincode> [coincode] ..    - Graph one or more Coincodes
    scan <coincode> [coincode] ..     - Scan one or more Coincodes
    log <coincode> [coincode] ..      - Display the log of one or more Coincodes
    update <coincode> [coincode] ..   - Update data of one or more Coincodes
    list                              - List tracked Coincodes 
    week <coincode> [coincode]        - Display the last weeks activity
    config                            - Display the configuration
        
        """)
        
	
