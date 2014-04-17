'''
Created on 16 apr. 2014

@author: Marnik
'''
import urllib2
from CrawlerHelpScripts import Comparator
from Database import dell
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import time

class Crawler():
    
    def main(self):
        start_time = time.time()
        print 'starting...'
        #First get the programmes with download links from the database and the ean numbers of products to search for
        db = dell.DeliveryInfo()
        programmes = db.getZanoxProgrammes()
        
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
            print len(self.records)
            self.getInfo()
    
        print 'completed in: ' , time.time() - start_time
    
    def getInfo(self):
        #For each item in the list, go trough the child elements, which is the product data.    
        for index in self.records:
            #Gather all the product data
            for child in index.iterfind('column[@name="ean"]'):
                self.ean = child.text
                
            if self.ean != None:#If the ean code is empty, don't execute remaining code
                
                for child in index.iterfind('column[@name="title"]'):
                    self.title = child.text
                for child in index.iterfind('column[@name="vendor"]'):
                    self.brand = child.text
                for child in index.iterfind('column[@name="price"]'):
                    price = child.text
                    #Replace , with a '.' to avoid truncated data
                    self.price = price.replace(',', '.')
        
                    decimalFinder = self.price.find('.') 
                    if decimalFinder == -1: #If it is a round number, add decimals so the db won't be updated unnecessary
                        self.price = price + '.00'
                for child in index.iterfind('column[@name="timetoship"]'):
                    self.availability = child.text
                for child in index.iterfind('column[@name="url"]'):
                    self.producturl = child.text

                comparator = Comparator.Comparator(self.title, self.brand, self.price, self.availability, self.ean, self.producturl, self.weburl)
                comparator.main()
                
            
c = Crawler()    
c.main()