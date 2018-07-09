import sys, getopt
import time, urllib2
from bs4 import BeautifulSoup

# specify the url
quote_page = "https://www.coinspot.com.au/buy/"

def main(argv):
	
    # query the website and return the html to the variable page
    hdr = {'User-Agent': 'Mozilla/5.0'}
    
    coincode = 'DGB'
    
    while True:
        try:

            coin_page = quote_page + coincode.lower()
            
            req = urllib2.Request(coin_page,headers=hdr)
            
            page = urllib2.urlopen(req)

            # parse the html using beautiful soup and store in variable `soup`
            soup = BeautifulSoup(page, "html.parser")

            # Take out the <div> of name and get its value
            name_box = soup.find('h1', attrs={'class': 'price-title'})

            # strip() is used to remove starting and trailing
            name = name_box.text.strip() 
            print name

        except urllib2.URLError:
            time.sleep(int(30))
	
        time.sleep(int(30))

if __name__ == "__main__":
	
    main(sys.argv[1:])
	
