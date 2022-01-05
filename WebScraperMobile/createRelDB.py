# -*- coding: utf-8 -*-
"""
Created on Sat Jul  3 17:17:39 2021

@author: maxik
"""
import sqlite3

class RelationalDatabase:
    
    conn = None
    cur = None
    
    def __init__(self, database: str):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        self.cur.execute('''PRAGMA foreign_keys = ON;''')
    

    def createTableManufacturer(self):
        query = """
                CREATE TABLE Manufacturer (
                    ManufacturerID INTEGER PRIMARY KEY,
                    Manufacturer TEXT NOT NULL UNIQUE,
                    ManufacturerNumber INTEGER NOT NULL UNIQUE);
                """
        self.cur.execute(query)
    
    
    def createTableModel(self):
        query = """
                CREATE TABLE Model (
                    ModelID INTEGER PRIMARY KEY,
                    ManufacturerID INTEGER NOT NULL,
                    Model TEXT NOT NULL UNIQUE,
                    ModelNumber INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (ManufacturerID)
                        REFERENCES Manufacturer (ManufacturerID)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );
                """
        self.cur.execute(query)
    
    
    def createTableCar(self):
        query = """
                CREATE TABLE Car (
                    CarID INTEGER PRIMARY KEY,
                    ModelID INTEGER NOT NULL,
                    MobileID INTEGER NOT NULL,
                    Title TEXT NOT NULL,
                    Price INTEGER,
                    Mileage INTEGER,
                    RegisteringDate TEXT,
                    PowerKW INTERGER,
                    Accident BOOLEAN,
                    Driveable BOOLEAN,
                    Damaged BOOLEAN,
                    Gasoline BOOLEAN,
                    ManualTransmission BOOLEAN,
                    Dealer BOOLEAN,
                    ImageURL TEXT,
                    Timestamp TEXT NOT NULL,
                    FOREIGN KEY (ModelID)
                        REFERENCES Model (ModelID)
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );
                """
        print('table created')
        self.cur.execute(query)
        
        
    def cascadeQuery(self):
        sql = """
                select * from Car join (Model join Manufacturer using (ManufacturerID)) using (ModelID);
                """
        query_obj = self.cur.execute(sql)
        return query_obj


    def insertManufacturer(self, man: str, manNum: int):
        mytuple = (man, manNum)
        sql = """INSERT INTO Manufacturer (Manufacturer, ManufacturerNumber)
                    VALUES (?,?)"""
        self.cur.execute(sql, mytuple)
        print('manufacturer {},{} inserted'.format(man, manNum))
        
        
    def insertModel(self, manID: int, model: str, modelNum: int):
        mytuple = (manID, model, modelNum)
        sql = """INSERT INTO Model (ManufacturerID, Model, ModelNumber)
                    VALUES (?,?,?)"""
        self.cur.execute(sql, mytuple)
        print('model {},{},{} inserted'.format(manID, model, modelNum))
        
        
    def queryMake(self):
        sql = """select * from Manufacturer;"""
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        query = cur.execute(sql)
        query = query.fetchall()
        make_listdict = [dict(make) for make in query]
        return make_listdict
        
    def queryModel(self):
        #sql = """SELECT * FROM Model;"""
        sql = """select * from Model join Manufacturer using (ManufacturerID);"""
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        query = cur.execute(sql)
        query = query.fetchall()
        model_listdict = [dict(model) for model in query]
        return model_listdict
    
    
    def alterMake(self, make: str, makenum: str):
        sql = f"""UPDATE Manufacturer SET {make}={makenum} WHERE 'Manufacturer'={make} ;"""
        self.cur.execute(sql)
        print('entry updated')
        
    def insertCar(self, modelID: int, mobileID: int, title: str, timestamp: str, price=None, mileage=None, regdate=None, power=None, acc :bool=None, drive: bool=None, dam: bool=None, gas: bool=None, mantrans: bool=None, dealer: bool=None, img=None):
        mytuple = (modelID, 
                   mobileID, 
                   title, 
                   price, 
                   mileage, 
                   regdate, 
                   power, 
                   acc, 
                   drive, 
                   dam, 
                   gas, 
                   mantrans, 
                   dealer, 
                   img, 
                   timestamp)
        sql = """INSERT INTO Car (ModelID, MobileID, Title, Price, Mileage, RegisteringDate, PowerKW, Accident, Driveable, Damaged, Gasoline, ManualTransmission, Dealer, ImageURL, Timestamp)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.cur.execute(sql, mytuple)
    
    
    """expects a nested tuple like this:
    ((CarID: int,
      ModelID: int,
      MobileID: int,
      Title: str,
      Price: int=None,
      Mileage: int=None,
      RegisteringDate: str=None,
      PowerKW: int=None,
      Accident: bool=None,
      Driveable: bool=None,
      Damaged: bool=None,
      Gasoline: bool=None,
      ManualTransmission: bool=None,
      Dealer: bool=None,
      ImageURL: str=None,
      Timestamp: str),
     (...),
     (...))"""
    def __car_generator(self, car_tuple: tuple):
            for single_tuple in car_tuple:
                yield (single_tuple)
                
    def insertmanyCar(self, car_tuple: tuple):
        
        sql = """INSERT INTO Car (CarID, ModelID, MobileID, Title, Price, Mileage, RegisteringDate, PowerKW, Accident, Driveable, Damaged, Gasoline, ManualTransmission, Dealer, ImageURL, Timestamp)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        self.cur.executemany(sql, self.__car_generator(car_tuple))
        print('entry inserted')  
        
        
    def getMakeID(self, number: int):
        sql = """select ManufacturerID from Manufacturer where ManufacturerNumber = {}""".format(number)
        self.cur.execute(sql)
        query = self.cur.fetchone()
        return query
    

    def getModelID(self, mannumber: int, number: int):
        """
        returns the ModelID (index of table Model)
        
        Parameters
        ----------
        mannumber : int
            Index of Manufacturer.
        number : int
            Number of Model.
        
        Returns
        -------
        query : TYPE
            (int,), type=tuple. returns ModelID (index of table Model).
        """
        sql = """select ModelID from Model where ManufacturerID = {} and ModelNumber = {}""".format(mannumber, number)
        self.cur.execute(sql)
        query = self.cur.fetchone()
        return query
    def open(self):
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.cur.execute('''PRAGMA foreign_keys = ON;''')
        
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        print('db closed')

if __name__ == '__main__':
    
    db = RelationalDatabase('mobileRDB.db')
    #createTableManufacturer(cur)
    #createTableModel(cur)
    #createTableCar(cur)
    #print(cascadeQuery(cur))
    try:
        carbuffer = ((7,1, 546, 'Honda CRX KLIMA',None,None,None,None,None,None,None,None,None,True,None,'2021-04-07'),
                     (8,1, 78, 'Honda CRX EG9',10000,None,None,None,None,None,None,None,None,True,None,'2021-04-07'),
                     (9,1, 165, 'Honda CRX good cond',None,None,None,165,None,None,None,None,None,True,None,'2021-04-07'))
        db.insertmanyCar(carbuffer)
        db.commit()
        print('queries committed')
    finally:
        db.close()
        print('DB closed')