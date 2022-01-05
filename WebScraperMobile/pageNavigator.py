"""
sucht nach der nächsten seite und gibt den link an den web-scraper weiter.
Steuert auch die Navigation zu anderen Modellen/Herstellern mit evtl. gewünschten suchfiltern
"""
import filterConfig
import modelConfig
from searchFilter import SearchFilter
from createRelDB import RelationalDatabase as RDB
import random

base_url = 'https://suchen.mobile.de/fahrzeuge/search.html?'
search_req = 'isSearchRequest=true&'
end_url = '&sfmr=false&vc=Car'

MODEL_ID = modelConfig.MODEL_ID
MAN_ID = modelConfig.MAN_ID
    
class PageNavigator:
    def __init__(self):
        self.__man_index = 0
        self.__model_index = 0
        self.__first_entry = True
        self.__next_man = None
        self.config = filterConfig.config  # import filter config parameters
        self.sF = SearchFilter()

    def __nextModel(self, man_id: str):
        try:
            next_model_id = list(MODEL_ID[man_id].values())[self.__model_index]
            self.__model_index = self.__model_index + 1
            return next_model_id
        except:
            #print("Final model reached, returning None...")
            self.__model_index = 0
            return None

    def __nextManufacturer(self):
        try:
            next_man_id = list(MAN_ID.values())[self.__man_index]
            self.__man_index = self.__man_index + 1
            return next_man_id
        except Exception:
            #print("Final manufacturer reached, returning None...")
            self.__man_index = 0
            return None

    """return manufacturerID + modelID"""
    def __nextManAndModel(self):
        # get first manufacturer
        if self.__first_entry:
            self.__next_man = self.__nextManufacturer()
            self.__first_entry = False
        # model for the manufacturer
        next_model = self.__nextModel(self.__next_man)
        # if last model is reached, skip to next manufacturer and get model
        if next_model is None:
            self.__next_man = self.__nextManufacturer()
            # if last manufacturer is reached, return None.
            if self.__next_man is None:
                return None
            else:
                next_model = self.__nextModel(self.__next_man)
        return self.__next_man, next_model

    """return url with/without filter; fltr optional"""
    def __model_url(self, man_id: str, model_id: str, fltr_front="", fltr_back=""):
        url = base_url + fltr_front + search_req + 'ms=' + man_id + ';' + model_id + fltr_back + end_url
        return url

    """return model_url based on filter parameters of filterConfig.config"""
    def nextFilteredPage(self):
        mylist = self.__nextManAndModel()  # get next model id
        # if last model(None) is reached -> return None -> search finished
        if mylist is None:
            return None
        fltr_front = []  # declare and reset of buffer list
        fltr_back = []
        reg_start = None
        mil_start = None
        pw_start = None
        price_start = None
        for key in self.config.keys():  # to_ez, from_ez, ...
            if self.config[key] is not None:
                for value in self.config[key]:  # ((11000,3),2000)
                    if mylist == value[0]:  # (11000,3)
                        # filter everything that stand in FRONT of isSearchRequest
                        if key == 'no_dmg':
                            fltr_front.append(self.sF.fltr_damage())
                        if key == 'from_ez':
                            fltr_front.append(self.sF.fltr_reg(start=value[1]))
                            reg_start = value[1]
                        if key == 'to_ez':
                            if reg_start:
                                fltr_front.pop()
                                fltr_front.append(self.sF.fltr_reg(start=reg_start, end=value[1]))
                                reg_start = None
                            else:
                                fltr_front.append(self.sF.fltr_reg(end=value[1]))
                        if key == 'gas':
                            fltr_front.append(self.sF.fltr_gas())

                        # filter everything that stands in the BACK of isSearchRequest
                        if key == 'from_mil':
                            fltr_back.append(self.sF.fltr_mil(start=value[1]))
                            mil_start = value[1]
                        if key == 'to_mil':
                            if mil_start:
                                fltr_back.pop()
                                fltr_back.append(self.sF.fltr_mil(start=mil_start, end=value[1]))
                                mil_start = None
                            else:
                                fltr_back.append(self.sF.fltr_mil(end=value[1]))
                        if key == 'from_price':
                            fltr_back.append(self.sF.fltr_price(start=value[1]))
                            price_start = value[1]
                        if key == 'to_price':
                            if mil_start:
                                fltr_back.pop()
                                fltr_back.append(self.sF.fltr_price(start=price_start, end=value[1]))
                                price_start = None
                            else:
                                fltr_back.append(self.sF.fltr_price(end=value[1]))
                        if key == 'from_pw':
                            fltr_back.append(self.sF.fltr_pw(start=value[1]))
                            pw_start = value[1]
                        if key == 'to_pw':
                            if mil_start:
                                fltr_back.pop()
                                fltr_back.append(self.sF.fltr_pw(start=pw_start, end=value[1]))
                                pw_start = None
                            else:
                                fltr_back.append(self.sF.fltr_pw(end=value[1]))
                        if key == 'trans':
                            fltr_back.append(self.sF.fltr_trans())

        fltr_front_str = ''.join(fltr_front)
        fltr_back_str = ''.join(fltr_back)

        if fltr_front and fltr_back:
            url = self.__model_url(mylist[0], mylist[1], fltr_front=fltr_front_str, fltr_back=fltr_back_str)
        elif fltr_front:
            url = self.__model_url(mylist[0], mylist[1], fltr_front=fltr_front_str)
        elif fltr_back:
            url = self.__model_url(mylist[0], mylist[1], fltr_back=fltr_back_str)
        else:
            url = self.__model_url(mylist[0], mylist[1])
        rdb = RDB('mobileRDB.db')
        makeid = rdb.getMakeID(int(mylist[0]))
        modelid = rdb.getModelID(makeid[0], int(mylist[1]))
        rdb.close()
        return url, modelid[0]    
    
    def nextPageList(self):
        url_list = []
        while True:
            url = self.nextFilteredPage()
            if url == None:
                break
            url_list.append(url)
            random.shuffle(url_list)
        return url_list

if __name__ == '__main__':
    pn = PageNavigator()
    
    url_list = pn.nextPageList()
    print(url_list)