import urllib2
from CrawlerHelpScripts import Comparator
from Database import Database
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re
import time
from CrawlerHelpScripts import logger

log = logger.createLogger("zanoxLogger", "zanox")

class Crawler():
    '''
    Create the lists that will be passed trough to the comparator. 
    This is so the data will be saved in batches
    '''
    titles = []
    brands = []
    prices = []
    availabilitys = []
    stocks = []
    eans = []
    producturls = []
    weburls = []
    images = []
    
    def main(self):
        start_time = time.time()
        log.info('starting crawler')
        #First get the programmes with download links from the database and the ean numbers of products to search for
        db = Database.Queries()
        db.openConnection()
        programmes = db.getZanoxProgrammes()
        db.closeConnection()
        
        #Download xml file for each programme       
        for programme in programmes:
            self.weburl = programme[0] #Used later for database to find website id
            log.info(str(time.asctime( time.localtime(time.time()) ))+ ' busy with'  +programme[0])
            
            xmlfile = urllib2.urlopen(programme[1])
            #convert to string:
            data = xmlfile.read()
            xmlfile.close()
            #create the root from data
            root = ET.fromstring(data)
            #find all records
            self.records = root.findall("data/record")
            
            self.getInfo()
        log.info(str(time.asctime( time.localtime(time.time()) ))+ ' completed in: ' , time.time() - start_time)
    
    def getInfo(self):
        
        #For each item in the list, go trough the child elements, which is the product data.   
        for index in self.records:
            #Gather all the product data
            for child in index.iterfind('column[@name="ean"]'):
                try:
                    ean = str(child.text)
                except:#If unicode error appears, assign 'Error' to ean so it will nog pass validation
                    ean = 'Error'
                    
            #Validate ean
            match = re.match('[0-9]{10,13}', ean)
            if match:#If the ean code is not valid, don't execute remaining code
                match =  None #reset match so not every ean will validate
                self.eans.append(ean)
                
                for child in index.iterfind('column[@name="title"]'):
                    try:
                        self.titles.append(str(child.text))
                    except:
                        log.error(str(time.asctime( time.localtime(time.time()) ))+ ' title produces a unicode error')
                        self.titles.append('unicode error')
                        '''
                        unicode aan passen: UnicodeEncodeError: 'charmap' codec can't encode character
                        '''
                for child in index.iterfind('column[@name="vendor"]'):
                    self.brands.append(child.text)
                    
                for child in index.iterfind('column[@name="price"]'):
                    #Replace , with a '.' to avoid truncated data
                    self.prices.append(child.text.replace(',', '.'))
        
                    decimalFinder = self.prices[-1].find('.') 
                    if decimalFinder == -1: #If it is a round number, add decimals so the db won't be updated unnecessary
                        self.prices[-1] = self.prices[-1] + '.00'
                        
                for child in index.iterfind('column[@name="timetoship"]'):
                    self.availabilitys.append(child.text)
                    
                for child in index.iterfind('column[@name="stock"]'):
                    self.stocks.append(child.text)
                    
                for child in index.iterfind('column[@name="url"]'):
                    self.producturls.append(child.text)
                    
                for child in index.iterfind('column[@name="image"]'):
                    self.images.append(child.text)
                
                self.weburls.append(self.weburl)

                if len(self.titles) == 1000:#Start comparing when 1000 products have been crawled
                    log.info(str(time.asctime( time.localtime(time.time()) ))+ ' starting comparison')
                    comparator = Comparator.Comparator(self.titles, self.brands, self.prices, self.availabilitys, self.stocks, self.eans, self.producturls, self.weburls, self.images)
                    comparator.main()
                    
                    #Reset lists
                    self.titles = []
                    self.brands = []
                    self.prices = []
                    self.availabilitys = []
                    self.stocks = []
                    self.eans = []
                    self.producturls = []
                    self.weburls = []
                    self.images = []
            
c = Crawler()    
c.main()