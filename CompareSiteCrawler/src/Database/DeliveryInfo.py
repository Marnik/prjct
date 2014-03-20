from Database import Database

class DeliveryInfo():
    db = Database()
        
        #Set info needed to insert/select/update database
    def setInfo(self, availability, price, producturl, weburl, ean):
        self.availability = availability
        self.price = price
        self.producturl = producturl
        self.weburl = weburl #used for getting website id for foreign key in deliveryinfo table
        self.ean = ean #used for getting phone id for foreign key in deliveryinfo table
        
    def save(self):
        #First get the webID and PhoneID, they are needed to insert in the table.
        self.getWebID()
        self.getPhoneID()        
        com = "INSERT INTO deliveryinfo (price, availability, url, website_id, phone_id) VALUES ((%s), (%s), (%s), (%s), (%s))" 
        vals = [str(self.price),str(self.availability), str(self.producturl), self.webID, self.phoneID]
        self.db.insert(com, vals);
        
    def getWebID(self):
        com = "SELECT id FROM websites WHERE url = (%s)"
        vals = [self.weburl]
        result = self.db.select(com,vals)
        for row in result:
            self.webID =  row[0]
    
    def getPhoneID(self):
        com = "SELECT id FROM phones WHERE ean = (%s)"
        vals = self.ean
        result = self.db.select(com, vals)
        for row in result:
            self.phoneID = row[0]
            
    def getDeliveryInfo(self): #Procedure to get the delivery info from the database, used to check if anything changed.
        #Get the webID and phoneID first...
        self.getWebID()
        self.getPhoneID()

        com = "SELECT price, availability, url FROM deliveryinfo WHERE website_id = (%s) AND phone_id = (%s)"
        vals = [self.webID, self.phoneID]
        result = self.db.select(com, vals)
        li = []
        #Add both values to a list for easy comparison later on.
        for row in result:
            li.append(row[0])
            li.append(row[1])
            li.append(row[2])
        return li
    
    def update(self): #Procedure to update the info
        #Get the webID and phoneID first...
        self.getWebID()
        self.getPhoneID()
        
        com = "UPDATE deliveryinfo SET price = (%s), availability = (%s), url = (%s) WHERE website_id = (%s) AND phone_id = (%s)"
        vals = [self.price, self.availability, self.producturl, self.webID, self.phoneID]
        self.db.insert(com, vals)
    
    def getZanoxProgrammes(self): #Procedures to get the Zanox programmes to use for parsing data from the Zanox API
        com = "SELECT weburl, feedurl FROM zanox"
        result = self.db.select(com, None)
        return result
    
    def getProducts(self):#Procedure to get the eans from products
        com = "SELECT ean FROM phones"
        result = self.db.select(com, None)
        return result
    