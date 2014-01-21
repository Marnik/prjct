from Database import Database
from warnings import catch_warnings
from unittest.main import CATCHBREAK

class DeliveryInfo():
    db = Database()
        
        #Set info needed to insert/select/update database
    def setInfo(self, availability_low, availability_high, price, url, phoneBrand, phoneType):
        self.availability_low = availability_low
        self.availability_high = availability_high
        self.price = price
        self.url = url
        self.phoneBrand = phoneBrand
        self.phoneType = phoneType
        
    def save(self):
        #First get the webID and PhoneID, they are needed to insert in the table.
        self.getWebID()
        self.getPhoneID()        
        com = "INSERT INTO deliveryinfo (price, availability, website_id, phone_id) VALUES ((%s), (%s), (%s), (%s))" 
        vals = [str(self.price),str(self.availability), self.webID, self.phoneID]
        self.db.insert(com, vals);
        
    def getWebID(self):
        com = "SELECT id FROM websites WHERE url = (%s)"
        vals = [self.url]
        result = self.db.select(com,vals)
        for row in result:
            self.webID =  row[0]
    
    def getPhoneID(self):
        com = "SELECT id FROM phones WHERE brand = (%s) AND type = (%s)"
        vals = [self.phoneBrand, self.phoneType]
        result = self.db.select(com, vals)
        for row in result:
            self.phoneID = row[0]
            
    def getDeliveryInfo(self): #Procedure to get the delivery info from the database, used to check if anything changed.
        #Get the webID and phoneID first...
        self.getWebID()
        self.getPhoneID()

        com = "SELECT price, availability_low, availability_high FROM deliveryinfo WHERE website_id = (%s) AND phone_id = (%s)"
        vals = [self.webID, self.phoneID]
        result = self.db.select(com, vals)
        li = []
        #Add both values to a list for easy comparison later on.
        for row in result:
            li.append(row[0])
            li.append(row[1])
            li.append(row[2])
        return li
    
    def update(self):
        #Get the webID and phoneID first...
        self.getWebID()
        self.getPhoneID()
        
        com = "UPDATE deliveryinfo SET price = (%s), availability_low = (%s), availability_high = (%s) WHERE website_id = (%s) AND phone_id = (%s)"
        vals = [self.price, self.availability_low, self.availability_high, self.webID, self.phoneID]
        self.db.insert(com, vals)
        