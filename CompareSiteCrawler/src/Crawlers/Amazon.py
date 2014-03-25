'''
Created on 20 mrt. 2014

@author: Marnik
'''

from amazonproduct import API
from Database import DeliveryInfo
from CrawlerHelpScripts import Comparator, CurrencyConverter

class Crawler():
    
    def main(self):
        self.api = API(locale='uk') #Set the right country code
        
        #Get the product data
        db = DeliveryInfo.DeliveryInfo()
        products = db.getProducts()
        
        for product in products: #For each product retrieved from the db, gather data
            self.getInfo(product[1])
            comparator = Comparator.Comparator(self.availability, self.price, self.producturl, 'www.amazon.co.uk', product[0])
            comparator.compare()
            
    def getInfo(self, product): #Procedure to gather the data for the product
        result = self.api.item_lookup(product, ResponseGroup="Offers") #Get xml for product
        
        #Extract relevant data from retrieved xml file
        price = result.Items.Item.OfferSummary.LowestNewPrice.Amount
        self.availability = result.Items.Item.Offers.Offer.OfferListing.Availability
        self.producturl = result.Items.Item.Offers.MoreOffersUrl  
        
        #Convert the currency to euros
        currencyConverter = CurrencyConverter.Converter()
        self.price = currencyConverter.convert('GBP', price/100) #divide by 100 because price is in smallest coins (e.g. pennys)
        
        
c = Crawler()
c.main()
