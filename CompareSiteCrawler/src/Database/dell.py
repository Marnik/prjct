from Database import Database

class DeliveryInfo():
    db = Database()
        
        #Set info needed to insert/select/update database
    def setInfo(self, title, brand, price, availability, ean, producturl, weburl):
        self.title = title
        self.brand = brand
        self.price = price
        self.availability = availability
        self.producturl = producturl
        self.weburl = weburl #used for foreign key assignments
        self.ean = ean #used for foreign key assignments

    def saveProducts(self):#Save the product data to the database
        com = "INSERT INTO Products (ean, brand, title) VALUES ((%s), (%s), (%s))"
        vals = [self.ean, self.brand, self.title]
        self.db.insert(com,vals)

    def saveDeliveryInfo(self):#Save the deliveryinfo to the database     
        com = "INSERT INTO deliveryinfo (price, availability, url, website_url, product_ean) VALUES ((%s), (%s), (%s), (%s), (%s))" 
        vals = [str(self.price),str(self.availability), str(self.producturl), self.weburl, self.ean]
        self.db.insert(com, vals);
        
    def getDeliveryInfo(self): #Procedure to get the delivery info from the database, used to check if anything changed.
        com = "SELECT price, availability, url FROM deliveryinfo WHERE website_url = (%s) AND product_ean = (%s)"
        vals = [self.weburl, self.ean]
        result = self.db.select(com, vals)
        li = []
        #Add all values to a list for easy comparison later on in the Comparator module.
        try:
            for row in result:
                li.append(row[0])
                li.append(row[1])
                li.append(row[2])
        except: 
            pass
        '''
        aanpassen
        '''
        return li
    
    def update(self): #Procedure to update the info
        com = "UPDATE deliveryinfo SET price = (%s), availability = (%s), url = (%s) WHERE website_url = (%s) AND products_ean = (%s)"
        vals = [self.price, self.availability, self.producturl, self.weburl, self.ean]
        self.db.insert(com, vals)
        
    def getZanoxProgrammes(self): #Procedures to get the Zanox programmes to use for parsing data from the Zanox API
        com = "SELECT website_url, feedurl FROM zanox"
        result = self.db.select(com, None)
        return result
