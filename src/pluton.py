#!/usr/bin/python
import argparse
from appdirs import *
import configparser
import os

appname = "Pluton"
appauthor = "Clixx.io Pty Limited"
appconfig = "pluton.ini"

appdatadir= user_data_dir(appname, appauthor)
if not os.path.exists(appdatadir):
    print("Creating directory %s for configuration file" % appdatadir)
    os.makedirs(appdatadir)
    
appfullconfig = os.path.join(appdatadir,appconfig)
config = configparser.ConfigParser(allow_no_value=True)
config.read(appfullconfig)

def coinList(coincodes):
    """Display a List of Tracked Coins.

    Keyword arguments:
    coincodes -- '*' (Default) or a set of CoinCode strings.
    """
        
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
    	
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="The Action to take")
    parser.add_argument("coin", metavar='Coin', nargs='*',help="Coin Code",default='*')
	
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
    elif args.action == "config":
        print("Using configuration file %s" % (appfullconfig))
    else:
        print("You asked for something that isnt supported.")
        
	
