#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 16 19:29:38 2021

@author: luxorbis
"""
import time
from time import perf_counter
from datetime import datetime
import random
from scipy.stats import truncnorm
from selenium.webdriver.common.keys import Keys

from pageNavigator import PageNavigator
import prepareSession
from prepareSession import SeleniumChrome
from scraper import Scraper
from createRelDB import RelationalDatabase as RDB

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

################################################################################
class WebScraper:
    def __init__(self):
        self.rdb = RDB('mobileRDB.db')
        pn = PageNavigator()
        self.url_list = pn.nextPageList()
        self.url_list_iter = iter(self.url_list)  # iterator with all urls
        self.proxy_gen = prepareSession.get_new_proxy()
    
    
    """`prepares` the session, return webdriver object"""
    def preparingSession(self):
        schr = SeleniumChrome()
        schr.start_webdriver()  # launch chrome instance
        
        schr.connect_proxy(next(self.proxy_gen))
        return schr
    
    def retryWithNewSession(self):
        return self.preparingSession()
        
    def duringSession(self, schr):
        data_total = []
        schr.open_new_tab(2)
        url, modelID = next(self.url_list_iter)   # url_list -> [((data), modelID)]
        print("opening modelID:", modelID)
        print("url:", url)
        schr.request(url)  # initial site
        page_num = 1
        while True:
            scrape = Scraper(schr.get_driver())
            data = scrape.collect_data()
            print("data collected from page:", page_num)
            data_total.append(data)  # store scraped data into buffer list
            next_url = scrape.next_page()
            if next_url == None:
                break
            elif next_url == 1:
                self.afterSession(modelID, data_total)
                schr = self.retryWithNewSession()
                continue                
            norm = get_truncated_normal(10, 5, 5, 25) # generate value from normal distribution
            time.sleep(norm.rvs())  # sleep for a random amount of time
            schr.request(next_url)
            page_num = page_num + 1
        return data_total, modelID
        
    
    def afterSession(self, modelID, data_total):
        self.rdb.open()
        for pages in data_total:
            for inserat in pages:
                self.rdb.insertCar(modelID, inserat[0], inserat[1], inserat[-1],inserat[2], inserat[3], inserat[4],inserat[5],inserat[6],inserat[7],inserat[8],inserat[9],inserat[10],inserat[11],inserat[12])
        print(f"data inserted ({sum([len(y) for y in data_total])})")
        self.rdb.commit()
        self.rdb.close()
                
    def quit(self, schr):
        schr.quit()
#=========================================MAIN=================================
if __name__ == "__main__":
    t1 = perf_counter()
    ws = WebScraper()
    for _ in ws.url_list:
        t11 = perf_counter()
        schr = ws.preparingSession()
        data, modelID = ws.duringSession(schr)
        ws.afterSession(modelID, data)
        ws.quit(schr)
        print(f"time for modelID: {modelID}", perf_counter() - t11)
    print("total time", perf_counter() - t1)
    