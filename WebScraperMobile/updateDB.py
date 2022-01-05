# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 20:23:40 2021

@author: maxik

!!!INFO DESCRIPTION: this script uses the models specified in 'modelConfig.py'
                    and checks whether the corresponding entries in the database
                    are present or do not match.
                    For database altering capabilities this script will rely on 
                    custom functions from 'createRelDB.py'.
                    
                    IF not present -> add Manufacturer/Model
                    IF not match -> alter entry
                    
                    The Manufacturer Name is absolute and has to be right
                    
this script is supposed to run once before every scraping session
"""

from modelConfig import MAN_ID, MODEL_ID
from createRelDB import RelationalDatabase as RDB

def get_key(my_dict: dict, value):
    for key, val in my_dict.items():
        if val == value:
            return key
    return "key doesnt exist"
    
    
def nested_dict2list(mydict: dict):
    mylist = []    
    for x in mydict:
        tmp = []
        tmp.append(x)
        for y in mydict[x]:
            t = []
            t.append(y)
            t.append(mydict[x][y])
            tmp.append(t)
        mylist.append(tmp)
    return mylist


def nested_list2set(mylist: list):
    myset = set()
    for x in mylist:
        for y in x:
            myset.add(y)
    return myset


class DBcheck:
    
    
    def __init__(self):
       self.rdb = RDB('mobileRDB.db') 
       
       
    #check if MAN_ID in model
    def checkMake(self, mydict: dict):
        man_set = set()
        for row in mydict:
            man_set.add(row['Manufacturer'])
        manid_set = set(MAN_ID)
        set_diff = manid_set.difference(man_set)
        return set_diff
    
    def insertMake(self, set_diff):
        for diff in set_diff:
            try:
                self.rdb.insertManufacturer(diff, int(MAN_ID[diff]))
            except Exception as e:
                print(e)
        return set_diff

    
    #check if MODEL_ID in model
    def checkModel(self, query_model: dict, query_makes: dict):
        query_set = set()
        for x in query_model:
            query_set.add(x['Model'])
        
        # get a full list of all models from MODEL_ID
        # manufacturers
        model_names = []
        for x in MODEL_ID:
            # models
            model_names.append(list(MODEL_ID[x].keys()))
    
        fullset = nested_list2set(model_names)
        
        difference = fullset.difference(query_set)
        return difference
    
    def insertModel(self, query_makes, difference):
        # if there are missing models -> add those to DB
        if difference:
            # one iteration represents one manufacturer
            for x in MODEL_ID.items():
                ManufacturerNum = int(x[0])  # 24100
                Models = x[1].keys()  # {'celica': '8', 'mr 2': '22', 'gt86': '31', 'supra': '33'}
                for Model in Models:  # 'celica', 'mr-2', 'gt86', 'supra'
                    if Model in difference:  # 'celica' in {'sunny', 'cappuccino', 'supra',...
                        flag = False
                        for Make in query_makes:  # [{'ManufacturerID': 1, 'Manufacturer': 'honda', 'ManufacturerNumber': 11000},{'ManufacturerID': 2, 'Manufacturer': 'subaru', 'ManufacturerNumber': 23500}]
                            make_num = Make['ManufacturerNumber']  # 11000
                            make_id = Make['ManufacturerID']  # 1
                            if make_num == ManufacturerNum:  # 11000 == 24100
                                flag = True
                                try:
                                    self.rdb.insertModel(make_id, Model, int(MODEL_ID[str(ManufacturerNum)][Model]))
                                except Exception as e:
                                    print(e)
                                break
                        if not flag:
                            print('manufacturer_id not recognizable: {}'.format(ManufacturerNum))
        return difference
    
    def update(self):
        makes = self.rdb.queryMake()
        models = self.rdb.queryModel()
        diff = self.checkMake(makes)
        if diff:
            print(f"new manufacturer(s) {diff} found, adding to DB...")
            self.insertMake(diff)
            self.rdb.commit()
            print(f"new manufacturer(s) {diff} added")
            makes = self.rdb.queryMake()
        else:
            print("makes already up to date")
        model_diff = self.checkModel(models, makes)
        if model_diff:
            print("new model(s) {model_diff} found, adding to DB...")
            self.insertModel(makes, model_diff)
            self.rdb.commit()
            print("new model(s) {model_diff} added")
        else:
            print("models already up to date")
        self.rdb.close()