'''
Created on 21 jan. 2014

@author: Marnik
'''
from bs4 import BeautifulSoup
import requests
from CrawlerHelpScripts import Comparator

class Crawler():
    
    def main(self):
        # Get the HTML of the page using BeautifulSoup
        url = requests.get('http://www.getgoods.de/smartphones-handys-und-festnetz/handys-und-smartphones/hersteller/samsung/749901/samsung-galaxy-s4-i9505-16gb-black#')
        #url = requests.get('http://www.getgoods.de/10181761/lg-g2-d802-16-gb-black-vodafone')
        self.soup = BeautifulSoup(url.text)
        
        #Call procedures to gather all info needed.
        self.getPrice()
        self.getAvailability()
        self.getPhoneBrand()
        self.getPhoneType()
        
        # Instantiate comparator to compare crawled data to database data and update the database if needed.
        comparator = Comparator.Comparator(self.availability_low, self.availability_high, self.price, 'www.getgoods.de', self.brand, self.type)
        comparator.compare()
        
    def getAvailability(self): #Procedure to extract the availability of the product.
        #Get the right part of HTML and extract the aailability from it.
        availabilitySoup = self.soup.find('p', attrs={'class' : 'deliverable_1'}).text
        availabilitySoup = str(availabilitySoup)
        availabilitySoup = availabilitySoup.strip()

        #Numeric values are used for the availability. The number indicates the amount of days it will take for it to be available.
        #If it is available, availability must be set to 0'
        if availabilitySoup.lower() == 'sofort lieferbar':
            self.availability_low = 0
            self.availability_high = 0
        elif availabilitySoup[:9].lower() == 'lieferbar': #If the availability is: 'Lieferbar in x-y Werktagen', get the x and y (low, high)
            stripe = availabilitySoup.find('-')
            self.availability_low = int(availabilitySoup[stripe-1:stripe])
            self.availability_high = int(availabilitySoup[stripe+1:stripe+2])
        
    def getPrice(self): #Procedure to extract price and availability status from the web page.        
        #Get the relevant HTML to get the price from, then get the price
        priceSoup = self.soup.find('div', attrs={'class' : 'specialCategoryTextColor article_details_price'}).text
        self.price = priceSoup.strip()
        self.price = self.price[0:-3]
        
        #If price contains a '-', like '450,-', replace it with '00' to avoid truncated data.
        if (str(self.price.find('-')) != -1):
            self.price = self.price.replace('-', '00')
        #Replace , with a '.' to avoid truncated data
        self.price = self.price.replace(',', '.')
        
    def getPhoneBrand(self): #Procedure to find the phone brand and type
        #Search for the relevant HTML and extract phone brand
        self.brand = self.soup.find('div', attrs={'class' : 'PageHeader'}).text
        
        
    def getPhoneType(self): #Procedure to find the type of the current phone
        typeSoup = self.soup.find('div', attrs={'id' : 'detailbox_middle'})
        typeSoup = str(typeSoup.find('h1').text)
        
        #If the typeSoup contains the brand name, make sure it doesn't get saved with the type. Else just get whole name
        if self.brand in typeSoup:
            self.type = typeSoup[self.brand.__len__()+1:]
        else:
            self.type = typeSoup 
        
c  = Crawler()
c.main()