import MySQLdb as mdb
import sys

class Database:
    con=""
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "" 
        self.database = "phonesdb"

    def select(self, com, vals):
        try:
            self.con = mdb.connect(self.host, self.user, self.password, self.database)
            cur = self.con.cursor()
            cur.execute(com,vals)
        
            ver = cur.fetchall()
            return ver
        except  mdb.Error as e:
            print e
        finally:
            if self.con:
                self.con.close()
    
    def insert(self, com, vals):
        try:
            self.con = mdb.connect(self.host, self.user, self.password, self.database)
            cur = self.con.cursor()
            cur.execute(com, vals)
            self.con.commit()
        except mdb.Error as e:
            print e
        finally:
            if self.con:
                self.con.close()