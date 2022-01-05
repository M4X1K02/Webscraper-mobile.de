# -*- coding: utf-8 -*-
"""
Created on Sun JUL  27 16:20:08 2021

@author: maxik
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.keys import Keys
import time
import random

#debugging
import traceback



class SurfSeleniumShark:
    
    PATH = 'C:\\Users\\maxik\\Documents\\PythonProjects\\chromedriver'
    EXTENSION_ID = '<yourextensionid>'
    proxy_list = []
    rand_proxy_list = []
    
    def start_webdriver(self):
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"   # Do not wait for full page load
        chrome_options = Options()
        chrome_options.add_extension("surfshark.crx")
        chrome_options.add_extension("showIP.crx")
        self.driver = webdriver.Chrome(executable_path=self.PATH, options=chrome_options, desired_capabilities=caps)
        self.actions = ActionChains(self.driver)
    
        """!!!must be called before anything with */proxy/*"""
    def proxy_login(self):
        self.driver.get("https://duckduckgo.com")
        #time.sleep(10)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        #navigate to extension url and fill in forms
        self.driver.get(f"chrome-extension://{self.EXTENSION_ID}/index.html")
        email_field = self.driver.find_element_by_name('email')
        self.actions.send_keys_to_element(email_field, '<youremail@example.com>')
        pwd_field = self.driver.find_element_by_name('password')
        self.actions.send_keys_to_element(pwd_field, '<yourpassword>').perform()
        submit = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/section/form/button[2]')
        submit.click()
        
        # wait for form to be submitted and then locate all listed proxies
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//span[@class="_2rgfu"]')))  #list of proxies
        print('logged into surfshark')
        
    
    """!!!must be called before 'connect_to_rand_proxy_list()"""
    def get_proxies(self):
        self.navigate_tab(1)
        #self.driver.find_element_by_xpath()
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[83]/div[1]/div[1]/div[2]'))  #uk london
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[75]/div[1]/div[1]/div[2]'))  #schweiz
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[74]/div[1]/div[1]/div[2]'))  #schweden
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[73]/div[1]/div[1]/div[2]'))  #spanien barcelona
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[71]/div[1]/div[1]/div[2]'))  #spanine valencia
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[68]/div[1]/div[1]/div[2]'))  #slowenien
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[67]/div[1]/div[1]/div[2]'))  #slowakei
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[63]/div[1]/div[1]/div[2]'))  #rumänien
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[60]/div[1]/div[1]/div[2]'))  #polen warschau
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[59]/div[1]/div[1]/div[2]'))  #polen danzig
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[55]/div[1]/div[1]/div[2]'))  #norwegen
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[34]/div[1]/div[1]/div[2]'))  #ungarn
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[8]/div[1]/div[1]/div[2]'))   #oesterreich
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[10]/div[1]/div[1]/div[2]'))  #belgien 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[13]/div[1]/div[1]/div[2]'))  #bulgarien 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[20]/div[1]/div[1]/div[2]'))  #kroatien
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[22]/div[1]/div[1]/div[2]'))  #tschechien 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[23]/div[1]/div[1]/div[2]'))  #daenemark 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[28]/div[1]/div[1]/div[2]'))  #paris 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[29]/div[1]/div[1]/div[2]'))  #frankfurt 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[30]/div[1]/div[1]/div[2]'))  #berlin 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[31]/div[1]/div[1]/div[2]'))  #nuernberg 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[47]/div[1]/div[1]/div[2]'))  #luxemburg 
        self.proxy_list.append(self.driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div/div/div[2]/div[51]/div[1]/div[1]/div[2]'))  #niederlande 
        
        self.rand_proxy_list = random.sample(self.proxy_list, 5)
        
        return self.rand_proxy_list
        
    
    def connect_to_rand_proxy_list(self, index):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.rand_proxy_list[index].click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//span[@class="_2dx4M"]')))  #connectino establishment
        print('connection established')
    
    
    def request(self, url):
        response = self.driver.get(url)
        return response
    
    
    def set_driver(self, d):
        self.driver = d
        
        
    def get_driver(self):
        return self.driver
    
    
    def disconnect_proxy(self):
        self.driver.switch_to.window(driver.window_handles[1])
        disconnect = self.driver.find_element(By.XPATH, '//button[@class="_2giRN _2r1Q_ _2amg4"]')  #search for disconnect button
        disconnect.click()
        print('disconnected from proxy')
        
        
    def open_new_tab(self, tab):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[tab])
        print('new tab created')
        
        
    def close_tab(self):
        pass
    def navigate_tab(self, tab):
        self.driver.switch_to.window(self.driver.window_handles[tab])
        
        
    def quit(self):
        self.driver.quit()
        print('browser terminated')
        
#-----------------------------------------------------------------------------

if __name__ == '__main__':
    sss = SurfSeleniumShark()
    driver = sss.start_webdriver()
    try:
        sss.proxy_login()
        proxies = sss.get_proxies()
        for tab in range(len(proxies)):
            try:
                sss.connect_to_rand_proxy_list(tab)
                time.sleep(1)
            except Exception as e:  #connect to another proxy if something fails
                print(e)
                continue
            sss.open_new_tab(tab + 2)
            sss.request('https://whatismyipaddress.com/')
            
    except Exception as e:
        print(e)
        traceback.print_exc()
        #sss.quit()