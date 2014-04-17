
from Database import dell

'''
The comparator is used to compare the crawler product data to the data stored in the database. If the data is not
the same, the database needs to be updated
'''
class Comparator():
    
    def __init__(self, title, brand, price, availability, ean, producturl, weburl):
        self.title = title
        self.brand = brand
        self.price = price
        self.availability = availability
        self.ean = ean
        self.producturl = producturl
        self.weburl = weburl
        self.db = dell.DeliveryInfo()
        self.db.setInfo(title, brand, price, availability, ean, producturl, weburl)

    def main(self):
        self.saveProducts()
        self.compare()

    def saveProducts(self): #Procedure used to save the products gathered from the product data feeds
        #Set the info for the database instance and save the products
        try:
            self.db.saveProducts()
        except: 
            pass
        '''
        unicode aanpassen
        '''
        
    def compare(self):#Procedure used to compare gathered data with data from the database and save changes.
        deliveryInfo = self.db.getDeliveryInfo() #Get the current price and availability from the database first.
        
        if deliveryInfo == []: #If result is empty, product data is not inserted in db yet so do this
            print 'no record, saving for ' +self.weburl
            self.db.saveDeliveryInfo()
        else: #Else if the result is not empty, check if the result are the same as the just crawled data. If not, update the database
            print 'checking for updates for ' +self.weburl
            if str(deliveryInfo[0]) != self.price or deliveryInfo[1] != str(self.availability) or deliveryInfo[2] != self.producturl:
                print 'updating db for ' +self.weburl
                self.db.update()