import sys, getopt
import time, urllib2
import argparse, configparser
from bs4 import BeautifulSoup
import paho.mqtt.publish as publish

# specify the url
quote_page = "https://www.coinspot.com.au/buy/"

# specify the mqtt host
mqtt_host = "192.168.1.105"

def scrapeCoin(coincode):
	
    try:
		
        coin_page = quote_page + coincode.lower()
            
        req = urllib2.Request(coin_page,headers=hdr)
            
        page = urllib2.urlopen(req)

        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, "html.parser")

        # Take out the <div> of name and get its value
        name_box = soup.find('h1', attrs={'class': 'price-title'})

        # strip() is used to remove starting and trailing
        price = name_box.text.strip() 
        print price
        
        if len(mqtt_host):
            publish.single("pluton/test", price, hostname=mqtt_host)

    except urllib2.URLError:
        time.sleep(int(percoin_interval))

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument("coin", metavar='Coin', nargs='*',help="Coin Code",default='*')
    parser.add_argument("--host", help="MQTT Broker Address")
	
    args = parser.parse_args()
	
    coinList = getattr(args, 'coin')

    if len(args.host):
        mqtt_host = mqtt_host
  	
    # query the website and return the html to the variable page
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    # coinList = ['DGB',]
    
    percoin_interval = 30
    
    print("You asked to monitor coins %s" % (coinList))

    while True:
		
        try:

            for coin in coinList:

                scrapeCoin(coin)
	
                time.sleep(int(percoin_interval))

        except Exception as e: 
            print(e)
            
