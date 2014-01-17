'''
Created on 17 jan. 2014

@author: Marnik
'''
from Database import DeliveryInfo

class Comparator():
    
    def __init__(self, availability, price, url, brand, type):
        self.availability = availability
        self.price = price
        self.url = url
        self.brand = brand
        self.type = type
        
    def compare(self):
        # Set the info for the database instance
        db = DeliveryInfo.DeliveryInfo()
        db.setInfo(self.availability, self.price, self.url, self.brand, self.type)
        deliveryInfo = db.getDeliveryInfo() #Get the current price and availability from the database first.
        
        #If the crawled info doesn't match the info from the database, update the database.
        if deliveryInfo[0] != self.price or deliveryInfo[1] != self.availability:
            db.update()
        