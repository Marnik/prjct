'''
Created on 17 jan. 2014

@author: Marnik
'''
from Database import DeliveryInfo

class Comparator():
    
    def __init__(self, availability, price, producturl, weburl, ean):
        self.availability = availability
        self.price = price
        self.producturl = producturl 
        self.weburl = weburl #used for getting website id for foreign key in deliveryinfo table
        self.ean = ean #used for getting phone id for foreign key in deliveryinfo table
        
    def compare(self):
        # Set the info for the database instance
        db = DeliveryInfo.DeliveryInfo()
        db.setInfo(self.availability, self.price, self.producturl, self.weburl, self.ean)
        deliveryInfo = db.getDeliveryInfo() #Get the current price and availability from the database first.

        if deliveryInfo == []: #If result is empty, product data is not inserted in db yet so do this
            print 'no record, saving for ' +self.weburl
            db.save()
        else: #Else if the result is not empty, check if the result are the same as the just crawled data. If not, update the database
            print 'checking for updates for ' +self.weburl
            if str(deliveryInfo[0]) != str(self.price) or deliveryInfo[1] != str(self.availability) or deliveryInfo[2] != self.producturl:
                print 'updating db for ' +self.weburl
                db.update()
        