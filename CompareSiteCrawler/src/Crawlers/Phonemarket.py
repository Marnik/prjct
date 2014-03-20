'''
Created on 1 feb. 2014

@author: Marnik
'''
import requests
from bs4 import BeautifulSoup

class Crawler():
    
    def main(self):
        # Get the HTML of the page using BeautifulSoup
        #url = requests.get('http://www.phonemarket.nl/apple-iphone-5c-16gb-white-me499dn-a-1?filter_name=samsung%20galaxy%20s4')
        url = requests.get('http://www.phonemarket.nl/samsung-galaxy-siii-i9300-16gb-black?filter_name=samsung')
        self.soup = BeautifulSoup(url.text)
        
        self.getPrice()
        print self.price
        
    def getAvailability(self): #Procedure to extract the availability of the product.
        #Get the right part of HTML and extract the availability from it.
        availabilitySoup = str(self.soup('div', attrs={'class' : 'description'}))
        beginQuote = availabilitySoup.find(';">') + 3
        endQuote = availabilitySoup[beginQuote:].find('<') + beginQuote
        availability = availabilitySoup[beginQuote:endQuote]
        
        #Numeric values are used for the availability. The number indicates the amount of days it will take for it to be available.
        #If it is available, availability must be set to 0'
        if availability.lower() == 'op voorraad':
            self.availability_low = 0
            self.availability_high = 0
        elif availability.lower() == 'tijdelijk uitverkocht': #If availability date is unknown, give it a -1 value.
            self.availability_low = -1
            self.availability_high = -1
            
    def getPrice(self): #Procedure to extract price and availability status from the web page.        
        #Get the relevant HTML to get the price from, then get the price
        priceSoup = str(self.soup.find('div', attrs={'class' : 'right'}).text)
        priceSoup = priceSoup[priceSoup.find('Prijs:')+7:].strip()
        euroCount = priceSoup.count(u"\u20AC")
        
        #If there are 3 euro signs in the string, it means that it is on sale so get the 2nd price.
        if euroCount == 3:
            begin = priceSoup.find(',') + 4
            priceSoup = priceSoup[begin:]
        
        self.price = priceSoup[2:priceSoup.find(',')+3]
        #Replace ',' with a '.' to avoid truncated data
        self.price = self.price.replace(',', '.')
        
    def getPhoneBrand(self): #Procedure to find the phone brand and type
        #Search for the relevant HTML and extract phone brand
        self.brand = self.soup.find('div', attrs={'class' : 'PageHeader'}).text

c = Crawler()
c.main()