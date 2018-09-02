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
            data = { coincode: price, 'ts' : time.time() }
            publish.single("pluton/price", json.dumps(data), hostname=broker)

    except urllib2.URLError:
        time.sleep(int(percoin_interval))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("coin", metavar='Coin', nargs='*',default='*', help="Coin Code")
    parser.add_argument("--broker", default='127.0.0.1', help="MQTT Broker Address")

    args = parser.parse_args()

    coinList = getattr(args, 'coin')

    if args.broker:
        mqtt_host = args.broker
        print 'Publishing Price Data to MQTT Broker ', args.broker
        
    exit    

    # query the website and return the html to the variable page
    hdr = {'User-Agent': 'Mozilla/5.0'}

    percoin_interval = 30

    print("You asked to monitor coins %s" % (coinList))

    while True:

        try:

            for coin in coinList:

                scrapeCoin(coin,args.broker)

                time.sleep(int(percoin_interval))

        except Exception as e: 
            print(e)

