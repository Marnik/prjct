import requests
from bs4 import BeautifulSoup
from Database import DeliveryInfo
from CrawlerHelpScripts import TimeCalculator, Comparator
import time


class Crawler():
    
    def main(self):
        # Get the HTML of the page using BeautifulSoup
        url = requests.get('http://www.pdashop.nl/product/294645/samsung-galaxy-s4.html?efas=a&__utma=1.97495333.1389036227.1389119630.1389124331.3&__utmb=1.12.8.1389124360997&__utmc=1&__utmx=-&__utmz=1.1389036227.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)&__utmv=-&__utmk=161692988')
        self.soup = BeautifulSoup(url.text)
        
        #Call procedures to gather all info needed.
        self.getPrice()
        self.getAvailability()
        self.getPhoneBrand()
        self.getPhoneType()
        
        # Instantiate comparator to compare crawled data to database data and update the database if needed.
        comparator = Comparator.Comparator(self.availability_low, self.availability_high, self.price, 'www.coolblue.nl', self.brand, self.type)
        comparator.compare()

    def getPrice(self): #Procedure to extract price and availability status from the web page.        
        #Get the relevant HTML to get the price from, then get the price
        priceSoup = self.soup.find('div', attrs={'class' : 'price'}).text
        self.price = priceSoup[3:].strip()
        
        #If price contains a '-', like '450,-', replace it with '00' to avoid truncated data.
        if (str(self.price.find('-')) != -1):
            self.price = self.price.replace('-', '00')
        #Replace , with a '.' to avoid truncated data
        self.price = self.price.replace(',', '.')
        
    def getAvailability(self): #Procedure to extract the availability of the product.
        #Get the right part of HTML and extract the aailability from it.
        availabilitySoup = str(self.soup.find('span', attrs={'class' : 'value-title'}))
        beginQuote = availabilitySoup.find('title="') + 7
        endQuote = availabilitySoup[beginQuote:].find('"') + beginQuote
        self.availability = availabilitySoup[beginQuote:endQuote]
        
        #Numeric values are used for the availability. The number indicates the amount of days it will take for it to be available.
        #If it is available, availability must be set to 0'
        if self.availability == 'op voorraad':
            self.availability_low = 0
            self.availability_high = 0
        else: #If it's not in stock, availability must be set to the expected arrival time of the product.
            availabilitySoup = str(self.soup.find('div', attrs="productInformationHeaderCollection"))
            begin = availabilitySoup[availabilitySoup.find('Verwacht:'):].find('state3') + 8 + availabilitySoup.find('Verwacht')
            end = availabilitySoup[begin:].find('<') + begin
            self.availability = availabilitySoup[begin:end]
            
            if self.availability == 'leverdatum onbekend': #If availability date is unknown, give it a -1 value. 
                self.availability_low = -1
                self.availability_high = -1
            elif self.availability[:4] == 'week':
                #Extract only the date (day, month)
                date = self.availability[self.availability.find('-')+2:]
                #Instantiate module to calculate the difference between today and availability date.
                timecalculator = TimeCalculator.TimeCalculator(date)
                self.availability_high = timecalculator.caluclateTime()
                self.availability_low = self.availability_low -5
    
    def getPhoneBrand(self): #Procedure to find the phone brand and type
        #Search for the relevant HTML and extract phone brand
        brandSoup = self.soup.findAll('span', attrs={'itemprop' : 'title'})
        for record in brandSoup:
            self.brand = record.text
        
        if self.brand.lower() == 'samsung mobile': #This sites refers to 'Samsung Mobile' instead of 'Samsung', change this.
            self.brand = 'Samsung'
            
    def getPhoneType(self): #Procedure to find the type of the current phone
        typeSoup = self.soup.find('title').text
        end = typeSoup.find('-') # Find the '-' that indicates the end of the type name
        
        #If the typeSoup contains the brand name, make sure it doesn't get saved with the type. Else just get whole name
        if self.brand in typeSoup:
            self.type = typeSoup[self.brand.__len__()+2:end]
        else:
            self.type = typeSoup[1:end]
        
        #Adjust name so it fits the one in the db
        if 'galaxy s4' in self.type.lower():
            self.type = 'Galaxy S4 i9505 16GB Black'
        elif 'galaxy s4 wit' in self.type.lower():
            self.type = 'Galaxy S4 i9505 16GB White'
        
crawler = Crawler()
crawler.main()