'''
Created on 22 jan. 2014

@author: Marnik
'''
from bs4 import BeautifulSoup
import requests
from CrawlerHelpScripts import Comparator

class Crawler():
    
    def main(self):
        # Get the HTML of the page using BeautifulSoup
        url = requests.get('http://www.pixmania.fr/smartphone/samsung-galaxy-s4-16-go-i9505-noir/21361758-a.html')
        self.soup = BeautifulSoup(url.text)
        
        #Call procedures to gather all info needed.
        self.getPrice()
        self.getAvailability()
        self.getPhoneBrand()
        self.getPhoneType()
        
        # Instantiate comparator to compare crawled data to database data and update the database if needed.
        comparator = Comparator.Comparator(self.availability_low, self.availability_high, self.price, 'www.pixmania.fr', self.brand, self.type)
        comparator.compare()
        
    def getAvailability(self): #Procedure to extract the availability of the product.
        #Get the right part of HTML and extract the aailability from it.
        try:
            availabilitySoup = self.soup.find('strong', attrs={'class' : 'available nowrap'}).text
            availabilitySoup = availabilitySoup.strip()
            
            #Numeric values are used for the availability. The number indicates the amount of days it will take for it to be available.
            #If it is available, availability must be set to 0'
            if availabilitySoup.lower() == 'en stock':
                self.availability_low = 0
                self.availability_high = 0
        except: #If the soup is not found, it is not on stock. Check in the not on stock class
            availabilitySoup = self.soup.find('p', attrs={'class' : 'availability'}).text
            availabilitySoup = availabilitySoup.strip()
            
            #Numeric values are used for the availability. The number indicates the amount of days it will take for it to be available.
            #If it is not available with no ETA, availability must be set to -1'
            if availabilitySoup.lower() == 'indisponible':
                self.availability_low = 0
                self.availability_high = 0 
        
    def getPrice(self): #Procedure to extract price and availability status from the web page.        
        #Get the relevant HTML to get the price from, then get the price
        priceSoup = self.soup.find('ins', attrs={'itemprop' : 'price'}).text
        priceSoup = priceSoup[:-2]
        
        #Replace , with a '.' to avoid truncated data
        self.price = priceSoup.replace(',', '.')
        
    def getPhoneBrand(self): #Procedure to find the phone brand and type
        #Search for the relevant HTML and extract phone brand
        self.brand = self.soup.find('span', attrs={'itemprop' : 'brand'}).text
        self.brand = self.brand[0:1] + self.brand[1:].lower()
        
    def getPhoneType(self): #Procedure to find the type of the current phone
        typeSoup = self.soup.find('span', attrs={'itemprop' : 'name'}).text
        typeSoup = str(typeSoup)
        print typeSoup.lower()
        #Adjust name so it fits the one in the db
        if 'galaxy s4 16 go i9505 noir' in typeSoup.lower():
            self.type = 'Galaxy S4 i9505 16GB Black'

c = Crawler()
c.main()