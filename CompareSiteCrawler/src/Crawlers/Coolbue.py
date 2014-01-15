import requests
from bs4 import BeautifulSoup
from Database import DeliveryInfo

class Crawler():
    
    def main(self):
        # Get the HTML of the page using BeautifulSoup
        url = requests.get('http://www.pdashop.nl/product/294645/samsung-galaxy-s4.html?efas=a&__utma=1.97495333.1389036227.1389119630.1389124331.3&__utmb=1.12.8.1389124360997&__utmc=1&__utmx=-&__utmz=1.1389036227.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)&__utmv=-&__utmk=161692988')
        #url = requests.get('http://www.pdashop.nl/product/395325/category-4214-smartphone-keuzehulp/nexus-5-wit.html')
        self.soup = BeautifulSoup(url.text)

        #Call procedures to gather all info needed.
        self.getPrice()
        self.getAvailability()
        self.getPhoneBrand()
        self.getPhoneType()
        self.compare()
        
    def getPrice(self): #Procedure to extract price and availability status from the web page.        
        #Get the relevant HTML to get the price from, then get the price
        priceSoup = self.soup.find('div', attrs={'class' : 'price'}).text
        self.price = priceSoup[3:].strip()
        
    def getAvailability(self): #Procedure to extract the availability of the product.
        #Get the right part of HTML and extract the aailability from it.
        availabilitySoup = str(self.soup.find('span', attrs={'class' : 'value-title'}))
        beginQuote = availabilitySoup.find('title="') + 7
        endQuote = availabilitySoup[beginQuote:].find('"') + beginQuote
        self.availability = availabilitySoup[beginQuote:endQuote]
        
        #If it is available, availability must be set to 'Direct!'
        if self.availability == 'op voorraad':
            self.availability = 'Direct!'
        else: #If it's not in stock, availability must be set to the expected arrival time of the product.
            availabilitySoup = str(self.soup.find('div', attrs="productInformationHeaderCollection"))
            begin = availabilitySoup[availabilitySoup.find('Verwacht:'):].find('state3') + 8 + availabilitySoup.find('Verwacht')
            end = availabilitySoup[begin:].find('<') + begin
            self.availability = availabilitySoup[begin:end]
    
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
            
    def compare(self):
        # Set the info for the database instance
        db = DeliveryInfo.DeliveryInfo()
        db.setInfo(self.availability, self.price, 'www.coolblue.nl', self.brand, self.type)
        deliveryInfo = db.getDeliveryInfo() #Get the current price and availability from the database first.
        
        #If the crawled info doesn't match the info from the database, update the database.
        if deliveryInfo[0] != self.price or deliveryInfo[1] != self.availability:
            db.update()
    
crawler = Crawler()
crawler.main()