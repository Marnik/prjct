'''
Created on 18 feb. 2014

@author: Marnik
'''
import urllib2
from Database import DeliveryInfo
from CrawlerHelpScripts import Comparator
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import time
import sys

class Crawler():
    
    def main(self):
        print 'starting...'
        start_time = time.time()
        #First get the programmes with download links from the database and the ean numbers of products to search for
        db = DeliveryInfo.DeliveryInfo()
        programmes = db.getZanoxProgrammes()
        self.products = db.getProducts()

        #Download xml file for each programme       
        for programme in programmes:
            self.weburl = programme[0] #Used later for database to find website id
            print 'busy with'  +programme[0]
            xmlfile = urllib2.urlopen(programme[1])
            #convert to string:
            data = xmlfile.read()
            xmlfile.close()
            #create the root from data
            root = ET.fromstring(data)
            #find all records
            self.records = root.findall("data/record")
            
            #Find data for each product
            for product in self.products:
                self.getInfo(product[0]) #pass ean number of current product as parameter
        print 'completed in: ' , time.time() - start_time
        
    def getInfo(self, product):
        #For each item in the list, go trough the child elements, which is the product data.    
        for index in self.records:
            #First find the correct product by ean number
            for child in index.iterfind('column[@name="ean"]'):
                try: #Not all ean fields are ean numbers, if this is the case; don't execute remaining code. Also don't execute if it is not the right ean
                    ean = int(child.text)
                    if ean == product: #Only gather and process data if the correct product is found.
                        for child in index.iterfind('column[@name="price"]'):
                            self.price = child.text
                            #Replace , with a '.' to avoid truncated data
                            self.price = self.price.replace(',', '.')
                            
                            decimalFinder = self.price.find('.') 
                            if decimalFinder == -1: #If it is a round number, add decimals so the db won't be updated unnecessary
                                self.price = self.price + '.00'
                        for child in index.iterfind('column[@name="availability"]'):
                            self.availability = child.text
                            if self.availability == None:
                                self.availability = 0
                        for child in index.iterfind('column[@name="url"]'):
                            self.producturl = child.text
                        comparator = Comparator.Comparator(self.availability, self.price, self.producturl, self.weburl, ean)
                        comparator.compare()
                except:
                    print sys.exc_info()[0]

        
c = Crawler()
c.main()